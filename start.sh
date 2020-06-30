#!/bin/sh
python manage.py migrate                  # Apply database migrations
python manage.py collectstatic --noinput  # Collect static files

# start up services
service rabbitmq-server start
rabbitmq-plugins enable rabbitmq_management
rabbitmqctl add_user tekhaus checkoutTekhaus1!
rabbitmqctl add_vhost tekeq
rabbitmqctl set_permissions -p tekeq tekhaus ".*" ".*" ".*"
rabbitmqctl set_user_tags tekhaus administrator

service celeryd start
service memcached start
service nginx start
# service ssh start

# start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn tekhaus.wsgi:application \
      --bind 0.0.0.0:8000 \

