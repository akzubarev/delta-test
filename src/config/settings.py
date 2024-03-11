import json
import os
import socket
import sys
from datetime import timedelta

#   _________  _  ____________
#  / ___/ __ \/ |/ / __/_  __/
# / /__/ /_/ /    /\ \  / /
# \___/\____/_/|_/___/ /_/


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, 'apps'))

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_URL = '/staticfiles/'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', False)

ALLOWED_HOSTS = os.getenv("DOMAINS").split(",")
ALLOWED_HOSTS.append(socket.gethostbyname(socket.gethostname()))

# STR_TIME_FORMAT = "%d.%m.%Y, %H:%M:%S"

#    ___   ___  ___  ____
#   / _ | / _ \/ _ \/ __/
#  / __ |/ ___/ ___/\ \
# /_/ |_/_/  /_/  /___/

INSTALLED_APPS = [
    # Admin
    # 'jazzmin',
    # 'django.contrib.admin',

    # Django core
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'celery',
    'django_celery_beat',
    'rest_framework',
    'drf_yasg',
    'django_filters',

    # Apps
    'apps.parcels',
]
#    __  __________  ___  __   _____      _____   ___  ____
#   /  |/  /  _/ _ \/ _ \/ /  / __/ | /| / / _ | / _ \/ __/
#  / /|_/ // // // / // / /__/ _/ | |/ |/ / __ |/ , _/ _/
# /_/  /_/___/____/____/____/___/ |__/|__/_/ |_/_/|_/___/

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CSRF_USE_SESSIONS = True
ROOT_URLCONF = 'config.urls'
ASGI_APPLICATION = 'config.routing.application'
WSGI_APPLICATION = 'config.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

#    ___  ___
#   / _ \/ _ )
#  / // / _ |
# /____/____/

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRESQL_DATABASE"),
        "USER": os.getenv("POSTGRESQL_USERNAME"),
        "PASSWORD": os.getenv("POSTGRESQL_PASSWORD"),
        "HOST": os.getenv("POSTGRESQL_HOST"),
        "PORT": os.getenv("POSTGRESQL_PORT"),
        'DISABLE_SERVER_SIDE_CURSORS': True,
    }
}

#    __   ____  ________   __   ____
#   / /  / __ \/ ___/ _ | / /  / __/
#  / /__/ /_/ / /__/ __ |/ /__/ _/
# /____/\____/\___/_/ |_/____/___/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        # 'file': {
        #     'level': 'DEBUG',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': 'celery.log',
        #     'formatter': 'verbose',
        #     'maxBytes': 1024 * 1024 * 100,  # 100 mb
        # },

    },
    'loggers': {
        '': {  # any (use path to limit)
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),  # and higher
            'handlers': ['default'],
        },
        'celery': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False

        },
    },
    'formatters': {
        'verbose': {
            'exp_format': '{asctime} {name} {module} {levelname} {message}',
            'style': '{',
        },
        'simple': {
            'exp_format': '{levelname} {message}',
            'style': '{',
        },
    },
}

# DRF
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}

# REDIS
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_QUEUE_HOST = os.getenv("REDIS_QUEUE_HOST", "redis-queues")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_USER = os.getenv("REDIS_USER", 'default')
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_DB_NUM = os.getenv("REDIS_DATABASE", "0")
REDIS_KEY_PREFIX = os.getenv('REDIS_KEY_PREFIX')
REDIS_BROKER = f"redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_QUEUE_HOST}:{REDIS_PORT}/{REDIS_DB_NUM}"
# REDIS-CACHE
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# REDIS CACHE CONFIG
redis_location = f"redis://{REDIS_USER}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NUM}"
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": redis_location,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": REDIS_PASSWORD
        },
        "KEY_PREFIX": REDIS_KEY_PREFIX
    }
}

# RABBITMQ
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", 'localhost')
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", 5672)
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBIMQ_BROKER = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}'

# CELERY
CELERY_BROKER_URL = RABBIMQ_BROKER
CELERY_BROKER_TRANSPORT_OPTIONS = {
    "visibility_timeout": 3600,
    'queue_order_strategy': 'priority',
    'global_keyprefix': REDIS_KEY_PREFIX,
    'priority_steps': list(range(5)),
    'sep': ':'
}
CELERY_RESULT_BACKEND = REDIS_BROKER
CELERY_ACCEPT_CONTENT = ['application/json', 'application/x-python-serialize']
CELERY_TASK_SERIALIZER = "pickle"  # "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_EXPIRES = 60
CELERY_TASK_RESULT_EXPIRES = 60
CELERY_IGNORE_RESULT = True
task_store_errors_even_if_ignored = True
CELERYD_PREFETCH_MULTIPLIER = 2
CELERYD_MAX_TASKS_PER_CHILD = 25
LOGIN_URL = '/login'
