"""
Django settings for cryptoproject project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y0z0j))mk9h4c=zl$*r)4-yu@i!lfpkz9o_rkpfzuhtc4*6me9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'coinsapp.apps.CoinsappConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # to include the app in the project, name format is App name with first capital character + Config = .CoinsappConfig
    'django_celery_beat',
    'django_extensions',
    'bootstrap4',

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

ROOT_URLCONF = 'cryptoproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'cryptoproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
import dj_database_url
DATABASE_URL='postgres://czhxvcpjphiqmu:2265ad9ce7bad542dfae8ff8a38cc84d2fc699386897db56be4b053e3e738509@ec2-54-243-253-24.compute-1.amazonaws.com:5432/d4050bcqchvfdq'
import dj_database_url
DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.




from datetime import timedelta
# CELERY STUFF

CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
BROKER_URL = "redis://localhost:6379/2"



CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Nairobi'
CELERY_ENABLE_UTC = False
CELERY_IMPORTS=("coinsapp.tasks")
CELERY_BEAT_SCHEDULE = {
    # 'get_market': {
    #     'task': 'coinsapp.tasks.get_all_markets',
    #     'schedule':  timedelta(minutes=1),
    #         },
    'main-task': {
        'task': 'coinsapp.tasks.get_coin_data',
        'schedule':  timedelta(minutes=1),
            },
    'remove-task': {
        'task': 'coinsapp.tasks.remove_old_values',
        'schedule':  timedelta(hours=1),
            },
                        }
