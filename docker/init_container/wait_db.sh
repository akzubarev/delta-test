#!/bin/sh

cmd="$@"
echo >&2 "--------------"
echo >&2 "$cmd"
echo >&2 "--------------"

until PGPASSWORD="$POSTGRESQL_PASSWORD" psql \
  -h "$POSTGRESQL_HOST" \
  -p "$POSTGRESQL_PORT" \
  -U "$POSTGRESQL_USERNAME" \
  -d "$POSTGRESQL_DATABASE" \
  -c '\q'; do
  echo >&2 "Postgres is unavailable - sleeping"
  sleep 1
done
echo >&2 "Postgres is up, continuing"

sh -c "$cmd"
