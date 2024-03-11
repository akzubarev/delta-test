# pull the official docker image
FROM python:3.10-alpine

RUN apk add --update --no-cache \
    postgresql-client \
    libffi-dev \
    gcc libc-dev \
    postgresql-dev python3-dev musl-dev

# set deploy directory
WORKDIR /usr/src/deploy

# set env VARIABLES
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install pipenv

COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy --ignore-pipfile
RUN apk del --no-cache \
    postgresql-dev \
    gcc \
    libc-dev \
    libffi-dev \
    python3-dev \
    musl-dev

# copy startup scripts
COPY ./docker/init_container/ /startup/
RUN chmod a+x /startup/*

# set app directory
WORKDIR /usr/src/app

# point to staticfiles shared volume for nginx
VOLUME ["/usr/src/app/staticfiles"]

# specify container entrypoint
ENTRYPOINT ["sh", "/startup/wait_db.sh"]

