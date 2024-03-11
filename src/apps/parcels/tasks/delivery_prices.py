from celery.utils.log import get_task_logger
from apps.parcels.models import Parcel, ParcelCandidate
from celeryconf import app
from utils.text_utils import readable_exception
from .cache_usd import get_usd_exchange_rate

logger = get_task_logger(__name__)


@app.task(name="count_delivery_prices")
def count_delivery_prices():
    successes, errors = 0, 0
    parcels = Parcel.objects.filter(delivery_price__isnull=True)
    for parcel in parcels:
        try:
            parcel.count_delivery_price(get_usd_exchange_rate())
            successes += 1
        except ValueError as e:
            errors += 1
            logger.error("\n".join([
                f"Error counting delivery price for {parcel.uuid}: {parcel}",
                readable_exception(e)
            ]))
    log_text = f"{parcels.count()} parcels delivery price counted: {successes} successes {errors} errors"
    if errors == 0:
        logger.info(log_text)
    else:
        logger.warning(log_text)


# @app.task(name="register_parcel", serializer="json")
# def register_parcel(name: str, uuid: str, price: float, weight: float,
#                     type_id: int):
#     parcel = None
#     try:
#         parcel = Parcel.objects.create(
#             name=name, price=price, uuid=uuid,
#             weight=weight, type_id=type_id
#         )
#         parcel.count_delivery_price(get_usd_exchange_rate())
#         logger.info(f"Parcel {uuid} registered successfully")
#     except ValueError as e:
#         logger.error("\n".join([
#             f"Error registering {uuid}: {parcel}", readable_exception(e)
#         ]))

@app.task(name="register_parcel", serializer="pickle")
def register_parcel(parcel: ParcelCandidate):
    try:
        parcel_model = Parcel.objects.create(
            name=parcel.name, price=parcel.price, uuid=parcel.uuid,
            weight=parcel.weight, type_id=parcel.type
        )
        parcel_model.count_delivery_price(get_usd_exchange_rate())
        logger.info(f"Parcel {parcel_model.uuid} registered successfully")
    except ValueError as e:
        logger.error("\n".join([
            f"Error registering {parcel.uuid}: {parcel}", readable_exception(e)
        ]))
