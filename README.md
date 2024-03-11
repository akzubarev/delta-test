# Тестовое задание Delta

Така как собеседование проходится на позицию Django-разработчика, было принято
решение выполнять задачу на Django, несмотря на то что в общем случае FastAPI
лучше подходит для разработки микросервисов. ТЗ с отметками о выполнении
приложено файлом TZ.md

### Используется:

- API: Django + DRF, документация Swagger
- Очереди: celery + RabbitMQ
- Кэш: redis
- Тестирование: DjangoTest
- База данных: PostgreSQL (замена с MySQL согласована)
- Docker: все разработанные контейнеры билдятся на одном образе python:
  3.10-alpine, также при отсутствии скачиваются образы redis, postgres,
  rabbitmq и nginx (последний тут не нужен, оставлен просто для демонстрации
  умения с ним работать)

---

## Запуск

- Скопировать `src/.env.template -> src/.env` и проставить свои значения вместо
  шаблонных либо ничего не менять
- `docker compose up -d` для запуска всех контейнеров
- `docker compose exec api python manage.py test` для запуска тестов
- `docker compose logs --follow api` логи API
- `docker compose logs --follow celery-worker` логи тасков

## Проверка

- Интерактивная документация Swagger по `localhost:8000/api/swagger/`
- API располагается по `localhost:8000/api/v1/parcels/`
    - `GET /?limit={int}&offset={int}&type={int}&delivery={bool}` - список
      посылок
    - `POST /` - создать посылку
    - `GET /types/` - типы посылок
    - `POST /claim/` - привязать посылку к компании

## Документация (насколько это можно так назвать)

Почти все вроде бы лежит по стандартным папкам, методы самодокументирующиеся, в
некоторых местах прокомментированы принятые решения, общая структура:

- Config: `/config/settings.py`
- Celery: `/celeryconf/`
- DB: `/apps/parcels/models`
- API: `/apps/parcels/views`, `/apps/parcels/serializers`
    - Список посылок - `ParcelsViewSet.list()`
    - Посылка по id - `ParcelsViewSet.retrieve(uuid)`
    - Список типов посылок - `ParcelsViewSet.types()`
    - Добавить посылку - `ParcelsViewSet.create(name,weight,price,type)`
    - Привязать посылку - `ParcelsViewSet.claim(uuid, company_id)`
- Таски: `/apps/parcels/tasks`, скедулинг в `/apps/parcels/app`
- Тесты `/apps.parcels/tests`

Все ошибки возвращаются как PermissionDenied с параметром "detail"
или ValidationError с параметром "errors" из rest_framework.exceptions