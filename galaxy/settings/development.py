# (c) 2012-2018, Ansible by Red Hat
#
# This file is part of Ansible Galaxy
#
# Ansible Galaxy is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by
# the Apache Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Ansible Galaxy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Apache License for more details.
#
# You should have received a copy of the Apache License
# along with Galaxy.  If not, see <http://www.apache.org/licenses/>.
# Django settings for galaxy project.

import os

from .default import *  # noqa


# =========================================================
# Django Core Settings
# =========================================================

DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
# ---------------------------------------------------------

INSTALLED_APPS += (  # noqa: F405
    'debug_toolbar',
)

MIDDLEWARE += [  # noqa: F405
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Static files
# ---------------------------------------------------------

STATIC_ROOT = ''

MEDIA_ROOT = '/var/lib/galaxy/media/'

# Database
# ---------------------------------------------------------

DATABASES = {
    'default': {
        'NAME': 'galaxy',
        'USER': 'galaxy',
        'PASSWORD': 'galaxy',
        'HOST': 'localhost',
        'PORT': 5432,
        'CONN_MAX_AGE': None,
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
    }
}

# Create default alias for worker logging
DATABASES['logging'] = DATABASES['default'].copy()

# Email settings
# ---------------------------------------------------------

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'

EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'var', 'email')  # noqa: F405

# =========================================================
# Third Party Apps Settings
# =========================================================

# Debug Toolbar
# ---------------------------------------------------------

DEBUG_TOOLBAR_PATCH_SETTINGS = False

# Celery settings
# ---------------------------------------------------------

# BROKER_URL = 'amqp://galaxy:galaxy@rabbitmq:5672/galaxy'
BROKER_URL = 'amqp://galaxy:galaxy@localhost:5672/galaxy'

# Redis
# ---------------------------------------------------------

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

# InfluxDB
# ---------------------------------------------------------

INFLUX_DB_HOST = 'localhost'
# INFLUX_DB_HOST = 'influxdb'
INFLUX_DB_PORT = 8086
INFLUX_DB_USERNAME = 'admin'
INFLUX_DB_PASSWORD = 'admin'
INFLUX_DB_UI_EVENTS_DB_NAME = 'galaxy_metrics'

# =========================================================
# Galaxy Settings
# =========================================================

SITE_ENV = 'DEV'

SITE_NAME = 'localhost'

WAIT_FOR = [
    {'host': 'postgres', 'port': 5432},
    {'host': 'localhost', 'port': 5672},
    {'host': 'localhost', 'port': 8086},
]

SOCIALACCOUNT_AFTER_CONNECT_REDIRECT_URL = 'http://localhost:4200/build/ansible/galaxy/settings'
