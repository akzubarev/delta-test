from django.apps import AppConfig

from common.global_vars import RECALCULATE_DOLLAR_SCHEDULE


class ParcelsApp(AppConfig):
    name = "apps.parcels"

    def ready(self):
        # noinspection PyUnresolvedReferences
        from utils.schedule import schedule_with_beat

        # Регулярный таск отключен тк вместо него используется очередь
        # schedule_with_beat(
        #     "count_delivery_prices",
        #     task_uri='count_delivery_prices',
        #     cron=HANDLE_PARCELS_SCHEDULE
        # )

        # В целом этот тоже необязательный, тк правила кэширования курса доллара
        # в ТЗ не указаны, вместо регулярного таска можно уменьшить CACHE_TTL
        # и метод get_usd_exchange_rate() будет сам обращаться за новым значением
        # только при надобности, когда оно будет исчезать из кэша, но я решил
        # оставить чтобы было понятно что в celery_beat я тоже умею
        schedule_with_beat(
            "cache_dollar",
            task_uri='cache_dollar',
            cron=RECALCULATE_DOLLAR_SCHEDULE
        )
