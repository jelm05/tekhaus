FROM python:3.7

LABEL "author"="justinelm@me.com"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#RUN pip install --upgrade pip

RUN mkdir -p /tekhaus
COPY requirements.txt /tekhaus/requirements.txt
WORKDIR /tekhaus
RUN pip3.7 install -r requirements.txt
COPY . /tekhaus

# EXPOSE ports
EXPOSE 8000
EXPOSE 8080


## set up celery service
#RUN mv /onboardingStudio/django_project/docker/celeryd /etc/init.d/celeryd
#RUN chmod 755 /etc/init.d/celeryd
#RUN chown root:root /etc/init.d/celeryd
#RUN mv /onboardingStudio/django_project/docker/celeryd_conf /etc/default/celeryd


# setup up rabbitmq-server
RUN curl -s https://packagecloud.io/install/repositories/rabbitmq/rabbitmq-server/script.deb.sh | bash
RUN curl -fsSL https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc | apt-key add -
RUN apt-get update -y
RUN apt-get install -y \
    erlang-base  \
    erlang-asn1  \
    erlang-crypto  \
    erlang-eldap  \
    erlang-ftp  \
    erlang-inets  \
    erlang-mnesia  \
    erlang-os-mon  \
    erlang-parsetools  \
    erlang-public-key  \
    erlang-runtime-tools  \
    erlang-snmp  \
    erlang-ssl  \
    erlang-syntax-tools  \
    erlang-tftp  \
    erlang-tools  \
    erlang-xmerl
RUN apt-get install -y rabbitmq-server=3.7.23-1


# CMD ["gunicorn", "--bind", ":8000", "tekhaus.wsgi:application"]
#CMD ["python", "tekhaus/manage.py", "runserver", "0.0.0.0:8000"]


# start gunicorn and django
RUN chmod +x start.sh
ENTRYPOINT ["/tekhaus/start.sh"]


