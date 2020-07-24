FROM python:3.7

LABEL "author"="justinelm@me.com"

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /tekhaus
WORKDIR /tekhaus
ADD . /tekhaus
COPY ./requirements.txt /tekhaus/requirements.txt

RUN pip install --upgrade pip
RUN pip3.7 install -r requirements.txt

COPY . /tekhaus

# nginx configuration
RUN mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf_orig
RUN mv ./docker/prod/nginx/docker_nginx.conf /etc/nginx/nginx.conf

# EXPOSE ports
EXPOSE 8000
EXPOSE 8080
EXPOSE 5672
EXPOSE 80

# Must make start.sh executable, otherwise permission denied
RUN chmod +x start.sh
#ENTRYPOINT ["/tekhaus/start.sh"]







