FROM python:3.12.8-alpine

WORKDIR /app/

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update

COPY . /app/

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

CMD ["gunicorn", "store.wsgi"]



