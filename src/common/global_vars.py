from config.settings import CACHES

REDIS_KEY_PREFIX = CACHES['default']['KEY_PREFIX']

USD_COURSE_KEY = "usd_exchange_rate"
USD_COURSE_TTL = 10 * 60
USD_COURSE_API = "https://www.cbr-xml-daily.ru/daily_json.js"

CACHE_KEY_TTL = 15 * 60
HANDLE_PARCELS_SCHEDULE = "*/5 * * * *"
RECALCULATE_DOLLAR_SCHEDULE = "*/5 * * * *"


PARCELS_KEY = "parcels"
