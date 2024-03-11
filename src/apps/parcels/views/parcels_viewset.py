import logging

from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from apps.parcels.views.filters import ParcelFilter
from common.global_vars import PARCELS_KEY
from apps.parcels.models import Parcel, ParcelType, ParcelCandidate
from apps.parcels.serializers import ParcelSerializer, ParcelTypeSerializer, \
    ParcelCreateSerializer, ParcelClaimSerializer
from apps.parcels.tasks import register_parcel
from common.mixins.uuid_mixin import generate_uuid

logger = logging.getLogger(__name__)


class ParcelsViewSet(viewsets.GenericViewSet):
    queryset = Parcel.objects
    lookup_field = "uuid"
    serializer_class = ParcelSerializer
    filterset_class = ParcelFilter

    # filter_backends = [filters.DjangoFilterBackend]
    # pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'POST':
            if self.action == "claim":
                serializer_class = ParcelClaimSerializer
            else:
                serializer_class = ParcelCreateSerializer
        return serializer_class

    def retrieve(self, request, *args, **kwargs):
        parcel = self.get_object()
        if parcel is None:
            return ValidationError("There is no parcel with this UUID")
        if parcel.uuid not in user_parcels(request):
            raise PermissionDenied("Parcel belongs to another user")

        serializer = self.serializer_class(
            parcel, context={'request': request}
        )
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        qs = self.paginate_queryset(
            self.filter_queryset(
                self.get_queryset().filter(uuid__in=user_parcels(request))
            )
        )
        serializer = self.serializer_class(
            qs, context={'request': request}, many=True
        )
        return Response(serializer.data)

    # В версии с очередью возвращение UUID может привести к неверному
    # поведению, если по каким-либо причинам воркер не сохранит посылку
    # или будет сохранять ее слишком долго, мне кажется здесь лучше подошла
    # бы запись в базу сразу с расчетом стоимости воркером либо в принципе
    # возвращать только успех/ошибки, а UUID пользователь может получить
    # из /list когда посылка успешно добавится в базу, либо сохранять в базу
    # заявки на создание посылок и уже потом их место заполнять настоящими
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            raise ValidationError({"errors": serializer.errors})
        # parcel = serializer.save()
        data = serializer.validated_data
        parcel = ParcelCandidate(
            name=data["name"], price=data["price"],
            weight=data["weight"], type=data["type"].id,
            uuid=generate_uuid()
        )
        put_in_handling_queue(parcel=parcel)
        available_parcels = user_parcels(request)
        available_parcels.add(parcel.uuid)
        request.session[PARCELS_KEY] = available_parcels
        return Response({"uuid": parcel.uuid})
        # return Response({"success": True)

    @action(detail=False, methods=["get"])
    def types(self, request, *args, **kwargs):
        serializer = ParcelTypeSerializer(
            ParcelType.objects.all(), context={'request': request}, many=True
        )
        return Response(serializer.data)

    # Про то, откуда у компании uuid посылки, ничего не сказано, поэтому
    # проверки на безопасность тут особо не провести
    @action(detail=False, methods=["post"])
    def claim(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            raise ValidationError({"errors": serializer.errors})
        data = serializer.validated_data

        # Возможно имелось ввиду, что это тоже нужно класть в очередь RabbitMQ,
        # но насколько я знаю, atomic и select_for_update позволяют добиться
        # нужного результата проще, а использование очередей я уже показал в create()
        with transaction.atomic():
            parcel = Parcel.objects.select_for_update().filter(
                uuid=data["uuid"]
            ).first()
            if parcel is None:
                raise ValidationError(
                    {"errors": ["There is no parcel with this UUID"]}
                )
            if parcel.company_id is not None:
                raise PermissionDenied("This parcel was already claimed")
            parcel.company_id = data["company_id"]
            parcel.save()
        return Response({"success": True})


def user_parcels(request):
    return set(request.session.get(PARCELS_KEY, None) or set())


def put_in_handling_queue(parcel: ParcelCandidate):
    # Если сериализовать json'ом, то вот, таск под json закомменчен рядом
    # register_parcel.delay(
    #     parcel.name, parcel.uuid, parcel.weight, parcel.price, parcel.type
    # )
    register_parcel.delay(parcel)
    logger.info(f"Delivery price count task for {parcel.uuid} added to queue")
