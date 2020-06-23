FROM python:3.7

LABEL "author"="justinelm@me.com"

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /tekhaus
WORKDIR /tekhaus
COPY . /tekhaus
RUN pip3.7 install -r requirements.txt

# EXPOSE ports
EXPOSE 8000
EXPOSE 8080


