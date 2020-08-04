#!/bin/sh

python manage.py migrate                  # Apply database migrations
python manage.py collectstatic --noinput  # Collect static files

# start rabbitmq services
#service rabbitmq-server start

#rabbitmq-plugins enable rabbitmq_management
#rabbitmqctl add_user tekhaus checkoutTekhaus1!
#rabbitmqctl add_vhost tekeq
#rabbitmqctl set_permissions -p tekeq tekhaus ".*" ".*" ".*"
#rabbitmqctl set_user_tags tekhaus administrator

# start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn -w 4 tekhaus.wsgi:application --bind 0.0.0.0:8000


