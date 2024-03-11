import requests
from celery.utils.log import get_task_logger
from django.core.cache import cache

import common.global_vars as c
from celeryconf import app
from utils.text_utils import readable_exception

logger = get_task_logger(__name__)


@app.task(name="cache_usd_exchange_rate")
def cache_usd_exchange_rate() -> float:
    return _cache_usd()


def get_usd_exchange_rate() -> float:
    course = cache.get(c.USD_COURSE_KEY)
    return course if course is not None else _cache_usd()


def _cache_usd():
    old_course = cache.get(c.USD_COURSE_KEY)
    try:
        data = requests.get(c.USD_COURSE_API).json()
        res = float(data.get("Valute").get("USD").get("Value"))
        logger.info(f"USD exchange rate updated successfully: {res:.2f}")
        return res
    except requests.exceptions.RequestException or TypeError as e:
        logger.error("\n".join([
            "Error updating dollar exchange rate", readable_exception(e)
        ]))
        if old_course is not None:
            cache.set(c.USD_COURSE_KEY, old_course, timeout=c.USD_COURSE_TTL)
            return old_course
    return None
