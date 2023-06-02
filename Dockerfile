FROM python:3.11.1-slim

RUN apt -y update
RUN apt install -y lame

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . . 
