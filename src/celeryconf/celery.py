import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery("post-service")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


def main():
    app.start()


if __name__ == '__main__':
    main()
