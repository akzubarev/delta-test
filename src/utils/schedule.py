import json
import logging

from django_celery_beat.models import PeriodicTask, CrontabSchedule

from utils.text_utils import readable_exception

logger = logging.getLogger(__name__)


def schedule_with_beat(task_name: str, task_uri: str,
                       cron: str, kwargs: dict = None):
    if kwargs is None:
        kwargs = dict()

    try:
        for task in PeriodicTask.objects.filter(
                name__contains=task_name):
            task.delete()

        time_split = cron.split(" ")
        schedule = CrontabSchedule.objects.get_or_create(
            minute=time_split[0], hour=time_split[1],
            day_of_week=time_split[2],
            day_of_month=time_split[3], month_of_year=time_split[4]
        )[0]
        PeriodicTask.objects.get_or_create(
            name=task_name, crontab=schedule, task=task_uri,
            kwargs=json.dumps(kwargs)
        )
        logger.info(f"{task_name} scheduled")

    except Exception as e:
        logger.warning(readable_exception(e))
