"""
Django settings for tekhaus project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import os.path
import environ

env = environ.Env(
    DEBUG=(bool, False)
)

# Read .env file
environ.Env.read_env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = tuple(env.list('ALLOWED_HOSTS', default=[]))

DEBUG = env('DEBUG')

SECRET_KEY = env('SECRET_KEY')

# MAILHOG VIA DOCKER COMPOSE CONFIG
EMAIL_HOST = 'smtp-server'
EMAIL_PORT = '1025'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'checkouts.apps.CheckoutsConfig',
    'django_select2',
    'django_celery_results',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tekhaus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tekhaus.wsgi.application'

# SELECT2 WIDGETS
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    },
    'select2': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 60 * 60 * 24,
    },
}
SELECT2_CACHE_BACKEND = 'select2'
CACHE_PREFIX = 'select2_'

SELECT2_CSS = '//cdnjs.cloudflare.com/ajax/libs/select2/4.0.6-rc.0/css/select2.min.css'
SELECT2_JS = '//cdnjs.cloudflare.com/ajax/libs/select2/4.0.6-rc.0/js/select2.min.js'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# CELERY SERVICE RABBITMQ BROKER
# CELERY_BROKER_URL = "amqp://rabbitmq"
CELERY_BROKER_URL = env.str('CELERY_BROKER_URL', default='amqp://rabbitmq')
CELERY_TASK_SERIALIZER = 'json'

# WORKING WITH DJANGO_CELERY_RESULTS
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_TMP = os.path.join(BASE_DIR, 'static')

# STATIC_ROOT = '/static_files/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# FOR HEROKU DEPLOYMENT
os.makedirs(STATIC_TMP, exist_ok=True)
os.makedirs(STATIC_ROOT, exist_ok=True)

LOGIN_REDIRECT_URL = 'dashboard'

LOGOUT_REDIRECT_URL = 'login'


