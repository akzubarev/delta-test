from dataclasses import dataclass
from uuid import UUID

from django.core.validators import MinValueValidator
from django.db import models

from common.mixins import UUIDMixin


class Parcel(UUIDMixin):
    name = models.CharField(
        verbose_name="Name",
        max_length=100,
    )

    # в ТЗ точно не указано, что вес не может быть нулевым, но логика
    # подсказывает, что такое условие должно быть, поэтому выставлено
    # ограничение 1мг
    weight = models.FloatField(
        verbose_name="Weight",
        default=0.01, validators=[MinValueValidator(0.001)]
    )

    # а вот цена, технически, может быть нулевой, на почте акция какая-нибудь
    # поэтому здесь оставлю только валидацию так
    # применение common sense я уже показал выше, а в ТЗ, опять же, не было
    price = models.FloatField(
        verbose_name="Price $",
        validators=[MinValueValidator(0.0)]
    )

    # то же самое тут
    delivery_price = models.FloatField(
        verbose_name="Delivery Price $",
        null=True, blank=True,
        validators=[MinValueValidator(0.0)]
    )

    # механизм on_delete в ТЗ не описан, мне показалось логичным
    # при удалении категории проставлять категорию "Разное",
    # но возможно подразумевался CASCADE
    type = models.ForeignKey(
        to="parcels.ParcelType",
        related_name="parcels", verbose_name="Type",
        default=1, on_delete=models.SET_DEFAULT
    )

    # "любое положительное число" технически это float, но имелся в виду
    # скорее всего все таки int, поэтому BigInteger (любое), все таки
    # международная компания
    company_id = models.PositiveBigIntegerField(
        verbose_name="Company ID",
        blank=True, null=True,
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = "Parcel"
        verbose_name_plural = "Parcels"

    def __str__(self):
        return str(self.name)

    def count_delivery_price(self, dollar_price: float):
        if dollar_price is None:
            raise ValueError("Нет курса доллара")
        self.delivery_price = (
                                      self.weight * 0.5 + self.price * 0.01
                              ) * dollar_price
        self.save()


@dataclass(slots=True)
class ParcelCandidate:
    name: str
    weight: float
    price: float
    uuid: UUID
    type: int
