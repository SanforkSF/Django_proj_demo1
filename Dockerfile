FROM python:3.9.5-slim-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DATABASE_URL 'postgresql://postgres:postgres@localhost/interflaska'
ENV FLASK_APP 'interview.py'

COPY requirements.txt /app/requirements.txt

COPY . /app/

RUN apt-get update && pip install --upgrade pip && \
    apt-get -y install libpq-dev gcc && \
    pip install psycopg2 && pip install -r requirements.txt

EXPOSE 5000
EXPOSE 5432


CMD ["python", "interview.py"]