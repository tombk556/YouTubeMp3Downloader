FROM python:3.11.2-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

COPY src/ /app/src/
COPY templates/ /app/templates/
COPY static/ /app/static/
COPY app.py /app/

EXPOSE 8080
