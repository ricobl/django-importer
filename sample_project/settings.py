# -*- coding: utf-8 -*-

# Path auto-discovery ###################################
import os
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
#########################################################

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1
USE_I18N = True
TIME_ZONE = 'America/Sao_Paulo'
LANGUAGE_CODE = 'pt-br'

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'data.db'
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''
TEST_DATABASE_NAME = 'data.test.db'

SECRET_KEY = '!cv0et@y@(13y#k2nw#af-q=avm9)67e_l!ia+_90f!9fz7285'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

ROOT_URLCONF = 'django_importer.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    # Project
    'tasks',
)

