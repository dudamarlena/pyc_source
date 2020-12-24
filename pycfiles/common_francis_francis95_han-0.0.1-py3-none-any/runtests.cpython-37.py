# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/marc/Git/common-framework/common/runtests.py
# Compiled at: 2019-09-02 10:20:07
# Size of source mod 2**32: 3877 bytes
__doc__ = '\nA standalone test runner script, configuring the minimum settings required for tests to execute.\nRe-use at your own risk: many Django applications will require different settings and/or templates to run their tests.\n'
import os, sys
APP_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, APP_DIR)
SETTINGS_DICT = {'BASE_DIR':APP_DIR, 
 'SECRET_KEY':'1', 
 'INSTALLED_APPS':('django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
 'django.contrib.sites', 'django.contrib.messages', 'django.contrib.staticfiles',
 'rest_framework', 'rest_framework.authtoken', 'pytz', 'common'), 
 'ROOT_URLCONF':'common.tests.urls', 
 'DATABASES':{'default': {'ENGINE':'django.db.backends.sqlite3', 
              'NAME':os.path.join(APP_DIR, 'db.sqlite3')}}, 
 'MIDDLEWARE':('django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
 'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware',
 'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware',
 'django.middleware.clickjacking.XFrameOptionsMiddleware'), 
 'SITE_ID':1, 
 'TEMPLATES':[
  {'BACKEND':'django.template.backends.django.DjangoTemplates', 
   'DIRS':os.path.join(APP_DIR, 'tests/templates'), 
   'APP_DIRS':True, 
   'OPTIONS':{'context_processors': [
                           'django.template.context_processors.debug',
                           'django.template.context_processors.request',
                           'django.contrib.auth.context_processors.auth',
                           'django.contrib.messages.context_processors.messages']}}], 
 'REST_FRAMEWORK':{'DEFAULT_PERMISSION_CLASSES':('rest_framework.permissions.IsAuthenticated', ), 
  'DEFAULT_AUTHENTICATION_CLASSES':('rest_framework.authentication.TokenAuthentication', 'rest_framework.authentication.SessionAuthentication'), 
  'DEFAULT_RENDERER_CLASSES':('rest_framework.renderers.JSONRenderer', ), 
  'DEFAULT_PARSER_CLASSES':('rest_framework.parsers.JSONParser', ), 
  'DEFAULT_PAGINATION_CLASS':'common.api.pagination.CustomPageNumberPagination', 
  'PAGE_SIZE':10, 
  'TEST_REQUEST_DEFAULT_FORMAT':'json', 
  'COERCE_DECIMAL_TO_STRING':True}, 
 'NOTIFY_CHANGES':False, 
 'LANGUAGE_CODE':'fr', 
 'TIME_ZONE':'Europe/Paris', 
 'USE_I18N':True, 
 'USE_L10N':True, 
 'USE_TZ':True, 
 'STATIC_URL':'/static/'}

def run_tests():
    from django.conf import settings
    (settings.configure)(**SETTINGS_DICT)
    import django
    if hasattr(django, 'setup'):
        django.setup()
    from django.test.utils import get_runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['common.tests'])
    sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests()