FROM python:3.10.2-alpine

RUN apk --no-cache add sqlite
RUN mkdir /data

RUN pip --no-cache install pipenv
ENV TZ UTC

WORKDIR /app

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install --deploy --system
RUN pip install ipdb
