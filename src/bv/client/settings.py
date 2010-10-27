DEBUG = False
TEMPLATE_DEBUG = SERVE_STATIC_FILES = DEBUG

PROJECT_NAME = "Bison Vert Client"
WITH_TITLE_HEADER = True

#rights
ADMINS = ()
MANAGERS = ADMINS

#Database
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'bvclient.sql'

TIME_ZONE = 'Europe/Paris'
LANGUAGE_CODE = 'fr'
SITE_ID = 1
USE_I18N = True

import os.path
PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
MEDIA_ROOT = os.path.join(PROJECT_ROOT_PATH, 'staticfiles')
MEDIA_URL = '/media/'
 

# XXX temporary fix
MINITAGE_ROOT_PATH = os.path.join(PROJECT_ROOT_PATH, '..', '..', '..', '..')
GEOS_LIBRARY_PATH = os.path.join(MINITAGE_ROOT_PATH, *('dependencies/geos-3.2/parts/part/lib/libgeos_c.so'.split('/')))

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT_PATH, 'templates'),
)

STATIC_DOC_ROOT = os.path.join(PROJECT_ROOT_PATH, 'staticfiles')

ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = 'nppo6u@=%eeb-=7owurguf=d4)38zbqmdkjdmmvr4kwb5!6!msm'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'bv.libclient.ext.dj.AuthenticationMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'bv.client.utils.context_processors.js_ext',
    'bv.libclient.ext.dj.bvauth',
    'bv.client.utils.context_processors.server_urls',
)

ROOT_URLCONF = 'bv.client.urls'

JS_EXT = '-min.js' if not DEBUG else '.js'

INSTALLED_APPS = (
    # external
    'django.contrib.admin', 
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',

    # internal
    'bv.client.trips',
    'bv.client.talks', 
    'bv.client.ratings', 
    'bv.client.utils',
    'oauthclient',
)

PERSISTENT_SESSION_KEY = 'testtesttest'
SESSION_COOKIE_NAME = 'bvclient'

# bvclient django extension related settings
BVCLIENT_OAUTH_APPID = 'bisonvert' # must match to oauthclient token identifier

# oauthclient django application related settings
OAUTHCLIENT_REDIRECT_AFTER_LOGIN = OAUTHCLIENT_REDIRECT_AFTER_LOGOUT = 'trips:home'
OAUTHCLIENT_ERROR_TEMPLATE  = 'oauthclient/error.html'

# Map settings
DEFAULT_MAP_CENTER_NAME = "France" 
DEFAULT_MAP_CENTER_POINT = "POINT( 2.213749 46.227638 )" 
DEFAULT_MAP_CENTER_ZOOM = 5 

# pagination params
DEFAULT_ITEMS_PER_PAGE = 10

# DEFAULT_SERVER_ROOT_URL = "http://api.bisonvert.net" 
DEFAULT_SERVER_ROOT_URL = "http://127.0.0.1:8085"
DEFAULT_SERVER_URLS = {
    'accounts': {
        'get': '%s/account/'
    }, 
}

try:
    from local_settings import *
except ImportError:
    pass
