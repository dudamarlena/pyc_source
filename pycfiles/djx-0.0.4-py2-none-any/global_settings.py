# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/conf/global_settings.py
# Compiled at: 2019-02-14 00:35:14
"""
Default Django settings. Override these with settings in the module pointed to
by the DJANGO_SETTINGS_MODULE environment variable.
"""
from __future__ import unicode_literals

def gettext_noop(s):
    return s


DEBUG = False
DEBUG_PROPAGATE_EXCEPTIONS = False
USE_ETAGS = False
ADMINS = []
INTERNAL_IPS = []
ALLOWED_HOSTS = []
TIME_ZONE = b'America/Chicago'
USE_TZ = False
LANGUAGE_CODE = b'en-us'
LANGUAGES = [
 (
  b'af', gettext_noop(b'Afrikaans')),
 (
  b'ar', gettext_noop(b'Arabic')),
 (
  b'ast', gettext_noop(b'Asturian')),
 (
  b'az', gettext_noop(b'Azerbaijani')),
 (
  b'bg', gettext_noop(b'Bulgarian')),
 (
  b'be', gettext_noop(b'Belarusian')),
 (
  b'bn', gettext_noop(b'Bengali')),
 (
  b'br', gettext_noop(b'Breton')),
 (
  b'bs', gettext_noop(b'Bosnian')),
 (
  b'ca', gettext_noop(b'Catalan')),
 (
  b'cs', gettext_noop(b'Czech')),
 (
  b'cy', gettext_noop(b'Welsh')),
 (
  b'da', gettext_noop(b'Danish')),
 (
  b'de', gettext_noop(b'German')),
 (
  b'dsb', gettext_noop(b'Lower Sorbian')),
 (
  b'el', gettext_noop(b'Greek')),
 (
  b'en', gettext_noop(b'English')),
 (
  b'en-au', gettext_noop(b'Australian English')),
 (
  b'en-gb', gettext_noop(b'British English')),
 (
  b'eo', gettext_noop(b'Esperanto')),
 (
  b'es', gettext_noop(b'Spanish')),
 (
  b'es-ar', gettext_noop(b'Argentinian Spanish')),
 (
  b'es-co', gettext_noop(b'Colombian Spanish')),
 (
  b'es-mx', gettext_noop(b'Mexican Spanish')),
 (
  b'es-ni', gettext_noop(b'Nicaraguan Spanish')),
 (
  b'es-ve', gettext_noop(b'Venezuelan Spanish')),
 (
  b'et', gettext_noop(b'Estonian')),
 (
  b'eu', gettext_noop(b'Basque')),
 (
  b'fa', gettext_noop(b'Persian')),
 (
  b'fi', gettext_noop(b'Finnish')),
 (
  b'fr', gettext_noop(b'French')),
 (
  b'fy', gettext_noop(b'Frisian')),
 (
  b'ga', gettext_noop(b'Irish')),
 (
  b'gd', gettext_noop(b'Scottish Gaelic')),
 (
  b'gl', gettext_noop(b'Galician')),
 (
  b'he', gettext_noop(b'Hebrew')),
 (
  b'hi', gettext_noop(b'Hindi')),
 (
  b'hr', gettext_noop(b'Croatian')),
 (
  b'hsb', gettext_noop(b'Upper Sorbian')),
 (
  b'hu', gettext_noop(b'Hungarian')),
 (
  b'ia', gettext_noop(b'Interlingua')),
 (
  b'id', gettext_noop(b'Indonesian')),
 (
  b'io', gettext_noop(b'Ido')),
 (
  b'is', gettext_noop(b'Icelandic')),
 (
  b'it', gettext_noop(b'Italian')),
 (
  b'ja', gettext_noop(b'Japanese')),
 (
  b'ka', gettext_noop(b'Georgian')),
 (
  b'kk', gettext_noop(b'Kazakh')),
 (
  b'km', gettext_noop(b'Khmer')),
 (
  b'kn', gettext_noop(b'Kannada')),
 (
  b'ko', gettext_noop(b'Korean')),
 (
  b'lb', gettext_noop(b'Luxembourgish')),
 (
  b'lt', gettext_noop(b'Lithuanian')),
 (
  b'lv', gettext_noop(b'Latvian')),
 (
  b'mk', gettext_noop(b'Macedonian')),
 (
  b'ml', gettext_noop(b'Malayalam')),
 (
  b'mn', gettext_noop(b'Mongolian')),
 (
  b'mr', gettext_noop(b'Marathi')),
 (
  b'my', gettext_noop(b'Burmese')),
 (
  b'nb', gettext_noop(b'Norwegian Bokmål')),
 (
  b'ne', gettext_noop(b'Nepali')),
 (
  b'nl', gettext_noop(b'Dutch')),
 (
  b'nn', gettext_noop(b'Norwegian Nynorsk')),
 (
  b'os', gettext_noop(b'Ossetic')),
 (
  b'pa', gettext_noop(b'Punjabi')),
 (
  b'pl', gettext_noop(b'Polish')),
 (
  b'pt', gettext_noop(b'Portuguese')),
 (
  b'pt-br', gettext_noop(b'Brazilian Portuguese')),
 (
  b'ro', gettext_noop(b'Romanian')),
 (
  b'ru', gettext_noop(b'Russian')),
 (
  b'sk', gettext_noop(b'Slovak')),
 (
  b'sl', gettext_noop(b'Slovenian')),
 (
  b'sq', gettext_noop(b'Albanian')),
 (
  b'sr', gettext_noop(b'Serbian')),
 (
  b'sr-latn', gettext_noop(b'Serbian Latin')),
 (
  b'sv', gettext_noop(b'Swedish')),
 (
  b'sw', gettext_noop(b'Swahili')),
 (
  b'ta', gettext_noop(b'Tamil')),
 (
  b'te', gettext_noop(b'Telugu')),
 (
  b'th', gettext_noop(b'Thai')),
 (
  b'tr', gettext_noop(b'Turkish')),
 (
  b'tt', gettext_noop(b'Tatar')),
 (
  b'udm', gettext_noop(b'Udmurt')),
 (
  b'uk', gettext_noop(b'Ukrainian')),
 (
  b'ur', gettext_noop(b'Urdu')),
 (
  b'vi', gettext_noop(b'Vietnamese')),
 (
  b'zh-hans', gettext_noop(b'Simplified Chinese')),
 (
  b'zh-hant', gettext_noop(b'Traditional Chinese'))]
LANGUAGES_BIDI = [
 b'he', b'ar', b'fa', b'ur']
USE_I18N = True
LOCALE_PATHS = []
LANGUAGE_COOKIE_NAME = b'django_language'
LANGUAGE_COOKIE_AGE = None
LANGUAGE_COOKIE_DOMAIN = None
LANGUAGE_COOKIE_PATH = b'/'
USE_L10N = False
MANAGERS = ADMINS
DEFAULT_CONTENT_TYPE = b'text/html'
DEFAULT_CHARSET = b'utf-8'
FILE_CHARSET = b'utf-8'
SERVER_EMAIL = b'root@localhost'
DATABASES = {}
DATABASE_ROUTERS = []
EMAIL_BACKEND = b'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = b'localhost'
EMAIL_PORT = 25
EMAIL_USE_LOCALTIME = False
EMAIL_HOST_USER = b''
EMAIL_HOST_PASSWORD = b''
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
EMAIL_SSL_CERTFILE = None
EMAIL_SSL_KEYFILE = None
EMAIL_TIMEOUT = None
INSTALLED_APPS = []
TEMPLATES = []
FORM_RENDERER = b'django.forms.renderers.DjangoTemplates'
DEFAULT_FROM_EMAIL = b'webmaster@localhost'
EMAIL_SUBJECT_PREFIX = b'[Django] '
APPEND_SLASH = True
PREPEND_WWW = False
FORCE_SCRIPT_NAME = None
DISALLOWED_USER_AGENTS = []
ABSOLUTE_URL_OVERRIDES = {}
IGNORABLE_404_URLS = []
SECRET_KEY = b''
DEFAULT_FILE_STORAGE = b'django.core.files.storage.FileSystemStorage'
MEDIA_ROOT = b''
MEDIA_URL = b''
STATIC_ROOT = None
STATIC_URL = None
FILE_UPLOAD_HANDLERS = [
 b'django.core.files.uploadhandler.MemoryFileUploadHandler',
 b'django.core.files.uploadhandler.TemporaryFileUploadHandler']
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440
DATA_UPLOAD_MAX_MEMORY_SIZE = 2621440
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000
FILE_UPLOAD_TEMP_DIR = None
FILE_UPLOAD_PERMISSIONS = None
FILE_UPLOAD_DIRECTORY_PERMISSIONS = None
FORMAT_MODULE_PATH = None
DATE_FORMAT = b'N j, Y'
DATETIME_FORMAT = b'N j, Y, P'
TIME_FORMAT = b'P'
YEAR_MONTH_FORMAT = b'F Y'
MONTH_DAY_FORMAT = b'F j'
SHORT_DATE_FORMAT = b'm/d/Y'
SHORT_DATETIME_FORMAT = b'm/d/Y P'
DATE_INPUT_FORMATS = [
 b'%Y-%m-%d', b'%m/%d/%Y', b'%m/%d/%y',
 b'%b %d %Y', b'%b %d, %Y',
 b'%d %b %Y', b'%d %b, %Y',
 b'%B %d %Y', b'%B %d, %Y',
 b'%d %B %Y', b'%d %B, %Y']
TIME_INPUT_FORMATS = [
 b'%H:%M:%S',
 b'%H:%M:%S.%f',
 b'%H:%M']
DATETIME_INPUT_FORMATS = [
 b'%Y-%m-%d %H:%M:%S',
 b'%Y-%m-%d %H:%M:%S.%f',
 b'%Y-%m-%d %H:%M',
 b'%Y-%m-%d',
 b'%m/%d/%Y %H:%M:%S',
 b'%m/%d/%Y %H:%M:%S.%f',
 b'%m/%d/%Y %H:%M',
 b'%m/%d/%Y',
 b'%m/%d/%y %H:%M:%S',
 b'%m/%d/%y %H:%M:%S.%f',
 b'%m/%d/%y %H:%M',
 b'%m/%d/%y']
FIRST_DAY_OF_WEEK = 0
DECIMAL_SEPARATOR = b'.'
USE_THOUSAND_SEPARATOR = False
NUMBER_GROUPING = 0
THOUSAND_SEPARATOR = b','
DEFAULT_TABLESPACE = b''
DEFAULT_INDEX_TABLESPACE = b''
X_FRAME_OPTIONS = b'SAMEORIGIN'
USE_X_FORWARDED_HOST = False
USE_X_FORWARDED_PORT = False
WSGI_APPLICATION = None
SECURE_PROXY_SSL_HEADER = None
MIDDLEWARE_CLASSES = [
 b'django.middleware.common.CommonMiddleware',
 b'django.middleware.csrf.CsrfViewMiddleware']
MIDDLEWARE = None
SESSION_CACHE_ALIAS = b'default'
SESSION_COOKIE_NAME = b'sessionid'
SESSION_COOKIE_AGE = 1209600
SESSION_COOKIE_DOMAIN = None
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_PATH = b'/'
SESSION_COOKIE_HTTPONLY = True
SESSION_SAVE_EVERY_REQUEST = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_ENGINE = b'django.contrib.sessions.backends.db'
SESSION_FILE_PATH = None
SESSION_SERIALIZER = b'django.contrib.sessions.serializers.JSONSerializer'
CACHES = {b'default': {b'BACKEND': b'django.core.cache.backends.locmem.LocMemCache'}}
CACHE_MIDDLEWARE_KEY_PREFIX = b''
CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_ALIAS = b'default'
AUTH_USER_MODEL = b'auth.User'
AUTHENTICATION_BACKENDS = [
 b'django.contrib.auth.backends.ModelBackend']
LOGIN_URL = b'/accounts/login/'
LOGIN_REDIRECT_URL = b'/accounts/profile/'
LOGOUT_REDIRECT_URL = None
PASSWORD_RESET_TIMEOUT_DAYS = 3
PASSWORD_HASHERS = [
 b'django.contrib.auth.hashers.PBKDF2PasswordHasher',
 b'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
 b'django.contrib.auth.hashers.Argon2PasswordHasher',
 b'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
 b'django.contrib.auth.hashers.BCryptPasswordHasher']
AUTH_PASSWORD_VALIDATORS = []
SIGNING_BACKEND = b'django.core.signing.TimestampSigner'
CSRF_FAILURE_VIEW = b'django.views.csrf.csrf_failure'
CSRF_COOKIE_NAME = b'csrftoken'
CSRF_COOKIE_AGE = 31449600
CSRF_COOKIE_DOMAIN = None
CSRF_COOKIE_PATH = b'/'
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
CSRF_HEADER_NAME = b'HTTP_X_CSRFTOKEN'
CSRF_TRUSTED_ORIGINS = []
CSRF_USE_SESSIONS = False
MESSAGE_STORAGE = b'django.contrib.messages.storage.fallback.FallbackStorage'
LOGGING_CONFIG = b'logging.config.dictConfig'
LOGGING = {}
DEFAULT_EXCEPTION_REPORTER_FILTER = b'django.views.debug.SafeExceptionReporterFilter'
TEST_RUNNER = b'django.test.runner.DiscoverRunner'
TEST_NON_SERIALIZED_APPS = []
FIXTURE_DIRS = []
STATICFILES_DIRS = []
STATICFILES_STORAGE = b'django.contrib.staticfiles.storage.StaticFilesStorage'
STATICFILES_FINDERS = [
 b'django.contrib.staticfiles.finders.FileSystemFinder',
 b'django.contrib.staticfiles.finders.AppDirectoriesFinder']
MIGRATION_MODULES = {}
SILENCED_SYSTEM_CHECKS = []
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SECURE_HSTS_SECONDS = 0
SECURE_REDIRECT_EXEMPT = []
SECURE_SSL_HOST = None
SECURE_SSL_REDIRECT = False