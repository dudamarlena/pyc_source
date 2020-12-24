# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/conf/global_settings.py
# Compiled at: 2018-07-11 18:15:30
gettext_noop = lambda s: s
DEBUG = False
TEMPLATE_DEBUG = False
DEBUG_PROPAGATE_EXCEPTIONS = False
USE_ETAGS = False
ADMINS = ()
INTERNAL_IPS = ()
ALLOWED_HOSTS = []
TIME_ZONE = 'America/Chicago'
USE_TZ = False
LANGUAGE_CODE = 'en-us'
LANGUAGES = (
 (
  'af', gettext_noop('Afrikaans')),
 (
  'ar', gettext_noop('Arabic')),
 (
  'az', gettext_noop('Azerbaijani')),
 (
  'bg', gettext_noop('Bulgarian')),
 (
  'be', gettext_noop('Belarusian')),
 (
  'bn', gettext_noop('Bengali')),
 (
  'br', gettext_noop('Breton')),
 (
  'bs', gettext_noop('Bosnian')),
 (
  'ca', gettext_noop('Catalan')),
 (
  'cs', gettext_noop('Czech')),
 (
  'cy', gettext_noop('Welsh')),
 (
  'da', gettext_noop('Danish')),
 (
  'de', gettext_noop('German')),
 (
  'el', gettext_noop('Greek')),
 (
  'en', gettext_noop('English')),
 (
  'en-gb', gettext_noop('British English')),
 (
  'eo', gettext_noop('Esperanto')),
 (
  'es', gettext_noop('Spanish')),
 (
  'es-ar', gettext_noop('Argentinian Spanish')),
 (
  'es-mx', gettext_noop('Mexican Spanish')),
 (
  'es-ni', gettext_noop('Nicaraguan Spanish')),
 (
  'es-ve', gettext_noop('Venezuelan Spanish')),
 (
  'et', gettext_noop('Estonian')),
 (
  'eu', gettext_noop('Basque')),
 (
  'fa', gettext_noop('Persian')),
 (
  'fi', gettext_noop('Finnish')),
 (
  'fr', gettext_noop('French')),
 (
  'fy-nl', gettext_noop('Frisian')),
 (
  'ga', gettext_noop('Irish')),
 (
  'gl', gettext_noop('Galician')),
 (
  'he', gettext_noop('Hebrew')),
 (
  'hi', gettext_noop('Hindi')),
 (
  'hr', gettext_noop('Croatian')),
 (
  'hu', gettext_noop('Hungarian')),
 (
  'ia', gettext_noop('Interlingua')),
 (
  'id', gettext_noop('Indonesian')),
 (
  'is', gettext_noop('Icelandic')),
 (
  'it', gettext_noop('Italian')),
 (
  'ja', gettext_noop('Japanese')),
 (
  'ka', gettext_noop('Georgian')),
 (
  'kk', gettext_noop('Kazakh')),
 (
  'km', gettext_noop('Khmer')),
 (
  'kn', gettext_noop('Kannada')),
 (
  'ko', gettext_noop('Korean')),
 (
  'lb', gettext_noop('Luxembourgish')),
 (
  'lt', gettext_noop('Lithuanian')),
 (
  'lv', gettext_noop('Latvian')),
 (
  'mk', gettext_noop('Macedonian')),
 (
  'ml', gettext_noop('Malayalam')),
 (
  'mn', gettext_noop('Mongolian')),
 (
  'nb', gettext_noop('Norwegian Bokmal')),
 (
  'ne', gettext_noop('Nepali')),
 (
  'nl', gettext_noop('Dutch')),
 (
  'nn', gettext_noop('Norwegian Nynorsk')),
 (
  'pa', gettext_noop('Punjabi')),
 (
  'pl', gettext_noop('Polish')),
 (
  'pt', gettext_noop('Portuguese')),
 (
  'pt-br', gettext_noop('Brazilian Portuguese')),
 (
  'ro', gettext_noop('Romanian')),
 (
  'ru', gettext_noop('Russian')),
 (
  'sk', gettext_noop('Slovak')),
 (
  'sl', gettext_noop('Slovenian')),
 (
  'sq', gettext_noop('Albanian')),
 (
  'sr', gettext_noop('Serbian')),
 (
  'sr-latn', gettext_noop('Serbian Latin')),
 (
  'sv', gettext_noop('Swedish')),
 (
  'sw', gettext_noop('Swahili')),
 (
  'ta', gettext_noop('Tamil')),
 (
  'te', gettext_noop('Telugu')),
 (
  'th', gettext_noop('Thai')),
 (
  'tr', gettext_noop('Turkish')),
 (
  'tt', gettext_noop('Tatar')),
 (
  'udm', gettext_noop('Udmurt')),
 (
  'uk', gettext_noop('Ukrainian')),
 (
  'ur', gettext_noop('Urdu')),
 (
  'vi', gettext_noop('Vietnamese')),
 (
  'zh-cn', gettext_noop('Simplified Chinese')),
 (
  'zh-tw', gettext_noop('Traditional Chinese')))
LANGUAGES_BIDI = ('he', 'ar', 'fa')
USE_I18N = True
LOCALE_PATHS = ()
LANGUAGE_COOKIE_NAME = 'django_language'
USE_L10N = False
MANAGERS = ADMINS
DEFAULT_CONTENT_TYPE = 'text/html'
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'
SERVER_EMAIL = 'root@localhost'
SEND_BROKEN_LINK_EMAILS = False
DATABASES = {}
DATABASE_ROUTERS = []
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
INSTALLED_APPS = ()
TEMPLATE_DIRS = ()
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader')
TEMPLATE_CONTEXT_PROCESSORS = ('django.contrib.auth.context_processors.auth', 'django.core.context_processors.debug',
                               'django.core.context_processors.i18n', 'django.core.context_processors.media',
                               'django.core.context_processors.static', 'django.core.context_processors.tz',
                               'django.contrib.messages.context_processors.messages')
TEMPLATE_STRING_IF_INVALID = ''
DEFAULT_FROM_EMAIL = 'webmaster@localhost'
EMAIL_SUBJECT_PREFIX = '[Django] '
APPEND_SLASH = True
PREPEND_WWW = False
FORCE_SCRIPT_NAME = None
DISALLOWED_USER_AGENTS = ()
ABSOLUTE_URL_OVERRIDES = {}
ALLOWED_INCLUDE_ROOTS = ()
ADMIN_FOR = ()
IGNORABLE_404_URLS = ()
SECRET_KEY = ''
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = None
FILE_UPLOAD_HANDLERS = ('django.core.files.uploadhandler.MemoryFileUploadHandler',
                        'django.core.files.uploadhandler.TemporaryFileUploadHandler')
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440
FILE_UPLOAD_TEMP_DIR = None
FILE_UPLOAD_PERMISSIONS = None
FORMAT_MODULE_PATH = None
DATE_FORMAT = 'N j, Y'
DATETIME_FORMAT = 'N j, Y, P'
TIME_FORMAT = 'P'
YEAR_MONTH_FORMAT = 'F Y'
MONTH_DAY_FORMAT = 'F j'
SHORT_DATE_FORMAT = 'm/d/Y'
SHORT_DATETIME_FORMAT = 'm/d/Y P'
DATE_INPUT_FORMATS = ('%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%b %d %Y', '%b %d, %Y',
                      '%d %b %Y', '%d %b, %Y', '%B %d %Y', '%B %d, %Y', '%d %B %Y',
                      '%d %B, %Y')
TIME_INPUT_FORMATS = ('%H:%M:%S', '%H:%M')
DATETIME_INPUT_FORMATS = ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M',
                          '%Y-%m-%d', '%m/%d/%Y %H:%M:%S', '%m/%d/%Y %H:%M:%S.%f',
                          '%m/%d/%Y %H:%M', '%m/%d/%Y', '%m/%d/%y %H:%M:%S', '%m/%d/%y %H:%M:%S.%f',
                          '%m/%d/%y %H:%M', '%m/%d/%y')
FIRST_DAY_OF_WEEK = 0
DECIMAL_SEPARATOR = '.'
USE_THOUSAND_SEPARATOR = False
NUMBER_GROUPING = 0
THOUSAND_SEPARATOR = ','
TRANSACTIONS_MANAGED = False
DEFAULT_TABLESPACE = ''
DEFAULT_INDEX_TABLESPACE = ''
X_FRAME_OPTIONS = 'SAMEORIGIN'
USE_X_FORWARDED_HOST = False
WSGI_APPLICATION = None
SECURE_PROXY_SSL_HEADER = None
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware')
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_AGE = 1209600
SESSION_COOKIE_DOMAIN = None
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_PATH = '/'
SESSION_COOKIE_HTTPONLY = True
SESSION_SAVE_EVERY_REQUEST = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_FILE_PATH = None
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}
CACHE_MIDDLEWARE_KEY_PREFIX = ''
CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_ALIAS = 'default'
COMMENTS_ALLOW_PROFANITIES = False
PROFANITIES_LIST = ()
AUTH_USER_MODEL = 'auth.User'
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', )
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'
LOGIN_REDIRECT_URL = '/accounts/profile/'
PASSWORD_RESET_TIMEOUT_DAYS = 3
PASSWORD_HASHERS = ('django.contrib.auth.hashers.PBKDF2PasswordHasher', 'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
                    'django.contrib.auth.hashers.BCryptPasswordHasher', 'django.contrib.auth.hashers.SHA1PasswordHasher',
                    'django.contrib.auth.hashers.MD5PasswordHasher', 'django.contrib.auth.hashers.UnsaltedSHA1PasswordHasher',
                    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher', 'django.contrib.auth.hashers.CryptPasswordHasher')
SIGNING_BACKEND = 'django.core.signing.TimestampSigner'
CSRF_FAILURE_VIEW = 'django.views.csrf.csrf_failure'
CSRF_COOKIE_NAME = 'csrftoken'
CSRF_COOKIE_DOMAIN = None
CSRF_COOKIE_PATH = '/'
CSRF_COOKIE_SECURE = False
MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'
LOGGING_CONFIG = 'django.utils.log.dictConfig'
LOGGING = {}
DEFAULT_EXCEPTION_REPORTER_FILTER = 'django.views.debug.SafeExceptionReporterFilter'
TEST_RUNNER = 'django.test.simple.DjangoTestSuiteRunner'
FIXTURE_DIRS = ()
STATICFILES_DIRS = ()
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder')