# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mgarabedian/steelscript/github/steelscript/docs/appfwk_project/local_settings.py
# Compiled at: 2017-08-09 16:41:06
from steelscript.appfwk.project.settings import *
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATAHOME = os.getenv('DATAHOME', PROJECT_ROOT)
PCAP_STORE = os.path.join(DATAHOME, 'data', 'pcap')
DATA_CACHE = os.path.join(DATAHOME, 'data', 'datacache')
INITIAL_DATA = os.path.join(DATAHOME, 'data', 'initial_data')
REPORTS_DIR = os.path.join(PROJECT_ROOT, 'reports')
LOG_DIR = os.path.join(DATAHOME, 'logs')
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
MEDIA_ROOT = DATA_CACHE
APPFWK_TASK_MODEL = 'async'
if APPFWK_TASK_MODEL == 'celery':
    LOCAL_APPS = ('djcelery', )
    INSTALLED_APPS += LOCAL_APPS
    BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_ACKS_LATE = True
    import djcelery
    djcelery.setup_loader()
    TEST_RUNNER = 'djcelery.contrib.test_runner.CeleryTestSuiteRunner'
LOCAL_APPS = ()
INSTALLED_APPS += LOCAL_APPS
GUEST_USER_ENABLED = False
GUEST_USER_TIME_ZONE = 'US/Eastern'
if GUEST_USER_ENABLED:
    REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = ['rest_framework.permissions.AllowAny']
    REST_FRAMEWORK.pop('EXCEPTION_HANDLER')
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': os.path.join(DATAHOME, 'data', 'project.db'), 
               'USER': '', 
               'PASSWORD': '', 
               'HOST': '', 
               'PORT': ''}}
LOGGING['handlers']['logfile']['filename'] = os.path.join(LOG_DIR, 'log.txt')
LOGGING['handlers']['backend-log']['filename'] = os.path.join(LOG_DIR, 'log-db.txt')
LOCAL_ERROR_HANDLERS = ()
GLOBAL_ERROR_HANDLERS += LOCAL_ERROR_HANDLERS
SECRET_KEY = '@+^^movly@4_rl-d*&0996q749x9d^ahabhjg(4cw3m7fghjuq'