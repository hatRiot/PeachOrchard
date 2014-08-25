"""
Django settings for server project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import random

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

#
# Hard coding a secret key is lame; instead, lets not distribute a key file and randomly generate
# one at first launch
#


def _generate_secret_key(loc):
    """ Generate a 64 byte random string to set as our secret key; this value
    is used by Django as well as Peach Orchard during node authentication.
    """

    key = '%064x' % random.randrange(16**64)
    with open(loc, "w+") as f:
        f.write("SECRET_KEY = '%s'" % key)

# attempt to load the key
try:
    from core.secret_key import *
except ImportError:
    _generate_secret_key(BASE_DIR + '/server/core/secret_key.py')
    from core.secret_key import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

#
# Nodes need to store crash information; we'll stash that here
# Dir structure:
#       .node/
#           1/
#           2/
#               01_02_2014-01-0101/
#               01_02_2014-01-0102/
#                   log.txt
#
NODE_DIR = BASE_DIR + '/.nodes'
if not os.path.isdir(NODE_DIR):
    os.mkdir(NODE_DIR)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'server',
    'bootstrap3',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'server.urls'

WSGI_APPLICATION = 'server.wsgi.application'

TEMPLATE_DIRS = (
        (BASE_DIR + '/server/templates'),
    )

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'po.db'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    (BASE_DIR + '/static'),
)