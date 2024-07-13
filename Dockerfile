FROM python:3.12-slim

ENV LANG=C.UTF-8 TZ=Asia/Shanghai

MAINTAINER dairoot

RUN apt-get update && apt-get install -y --no-install-recommends build-essential xvfb xauth python3-tk python3-dev gnome-screenshot tesseract-ocr

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install -U pip && pip install -r requirements.txt

RUN playwright install chrome

COPY . .
