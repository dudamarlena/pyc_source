# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/settings.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import os, re, djblets
from django.core.urlresolvers import reverse
from reviewboard.dependencies import dependency_error, fail_if_missing_dependencies
from reviewboard.staticbundles import PIPELINE_STYLESHEETS, PIPELINE_JAVASCRIPT

def _(s):
    return s


DEBUG = True
ADMINS = (('Example Admin', 'admin@example.com'), )
MANAGERS = ADMINS
USE_TZ = True
TIME_ZONE = b'UTC'
LANGUAGE_CODE = b'en-us'
SITE_ID = 1
EMAIL_SUBJECT_PREFIX = b'[Review Board] '
EMAIL_DEFAULT_SENDER_SERVICE_NAME = b'Review Board'
USE_I18N = True
MIDDLEWARE_CLASSES = [
 b'django.middleware.gzip.GZipMiddleware',
 b'reviewboard.admin.middleware.InitReviewBoardMiddleware',
 b'corsheaders.middleware.CorsMiddleware',
 b'django.middleware.clickjacking.XFrameOptionsMiddleware',
 b'django.middleware.common.CommonMiddleware',
 b'django.middleware.http.ConditionalGetMiddleware',
 b'django.middleware.locale.LocaleMiddleware',
 b'django.contrib.sessions.middleware.SessionMiddleware',
 b'django.contrib.auth.middleware.AuthenticationMiddleware',
 b'django.contrib.messages.middleware.MessageMiddleware',
 b'djblets.siteconfig.middleware.SettingsMiddleware',
 b'reviewboard.admin.middleware.LoadSettingsMiddleware',
 b'djblets.extensions.middleware.ExtensionsMiddleware',
 b'djblets.integrations.middleware.IntegrationsMiddleware',
 b'djblets.log.middleware.LoggingMiddleware',
 b'reviewboard.accounts.middleware.TimezoneMiddleware',
 b'reviewboard.accounts.middleware.UpdateLastLoginMiddleware',
 b'reviewboard.admin.middleware.CheckUpdatesRequiredMiddleware',
 b'reviewboard.accounts.middleware.X509AuthMiddleware',
 b'reviewboard.site.middleware.LocalSiteMiddleware',
 b'djblets.extensions.middleware.ExtensionsMiddlewareRunner',
 b'reviewboard.admin.middleware.ExtraExceptionInfoMiddleware']
RB_EXTRA_MIDDLEWARE_CLASSES = []
SITE_ROOT_URLCONF = b'reviewboard.urls'
ROOT_URLCONF = b'djblets.urls.root'
REVIEWBOARD_ROOT = os.path.abspath(os.path.split(__file__)[0])
SITE_ROOT = b'/'
STATICFILES_DIRS = (
 (
  b'lib', os.path.join(REVIEWBOARD_ROOT, b'static', b'lib')),
 (
  b'rb', os.path.join(REVIEWBOARD_ROOT, b'static', b'rb')),
 (
  b'djblets',
  os.path.join(os.path.dirname(djblets.__file__), b'static', b'djblets')))
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder',
                       'djblets.extensions.staticfiles.ExtensionFinder', 'pipeline.finders.PipelineFinder')
STATICFILES_STORAGE = b'pipeline.storage.PipelineCachedStorage'
RB_BUILTIN_APPS = [
 b'corsheaders',
 b'django.contrib.admin',
 b'django.contrib.auth',
 b'django.contrib.contenttypes',
 b'django.contrib.sites',
 b'django.contrib.sessions',
 b'django.contrib.staticfiles',
 b'djblets',
 b'djblets.avatars',
 b'djblets.configforms',
 b'djblets.datagrid',
 b'djblets.extensions',
 b'djblets.features',
 b'djblets.feedview',
 b'djblets.forms',
 b'djblets.gravatars',
 b'djblets.integrations',
 b'djblets.log',
 b'djblets.pipeline',
 b'djblets.privacy',
 b'djblets.recaptcha',
 b'djblets.siteconfig',
 b'djblets.util',
 b'haystack',
 b'oauth2_provider',
 b'pipeline',
 b'reviewboard',
 b'reviewboard.accounts',
 b'reviewboard.admin',
 b'reviewboard.attachments',
 b'reviewboard.avatars',
 b'reviewboard.changedescs',
 b'reviewboard.diffviewer',
 b'reviewboard.extensions',
 b'reviewboard.hostingsvcs',
 b'reviewboard.integrations',
 b'reviewboard.notifications',
 b'reviewboard.oauth',
 b'reviewboard.reviews',
 b'reviewboard.scmtools',
 b'reviewboard.site',
 b'reviewboard.webapi']
try:
    import django_reset
    RB_BUILTIN_APPS.append(b'django_reset')
except ImportError:
    pass

RB_EXTRA_APPS = []
WEB_API_ENCODERS = ('djblets.webapi.encoders.ResourceAPIEncoder', )
WEB_API_AUTH_BACKENDS = ('reviewboard.webapi.auth_backends.WebAPIBasicAuthBackend',
                         'djblets.webapi.auth.backends.api_tokens.WebAPITokenAuthBackend')
WEB_API_SCOPE_DICT_CLASS = b'djblets.webapi.oauth2_scopes.ExtensionEnabledWebAPIScopeDictionary'
WEB_API_ROOT_RESOURCE = b'reviewboard.webapi.resources.root.root_resource'
SESSION_ENGINE = b'django.contrib.sessions.backends.cached_db'
CACHES = {b'default': {b'BACKEND': b'django.core.cache.backends.locmem.LocMemCache', 
                b'LOCATION': b'reviewboard'}}
LOGGING_NAME = b'reviewboard'
LOGGING_REQUEST_FORMAT = b'%(_local_site_name)s - %(user)s - %(path)s'
LOGGING_BLACKLIST = [
 b'django.db.backends',
 b'MARKDOWN',
 b'PIL.Image']
AUTH_PROFILE_MODULE = b'accounts.Profile'
CACHE_EXPIRATION_TIME = 2592000
TEST_RUNNER = b'reviewboard.test.RBTestRunner'
RUNNING_TEST = os.environ.get(b'RB_RUNNING_TESTS') == b'1'
LOCAL_ROOT = None
PRODUCTION = True
ALLOWED_HOSTS = [
 b'*']
LANGUAGE_COOKIE_NAME = b'rblanguage'
SESSION_COOKIE_NAME = b'rbsessionid'
SESSION_COOKIE_AGE = 31536000
SUPPORT_URL_BASE = b'https://www.beanbaginc.com/support/reviewboard/'
DEFAULT_SUPPORT_URL = SUPPORT_URL_BASE + b'?support-data=%(support_data)s'
REGISTER_SUPPORT_URL = SUPPORT_URL_BASE + b'register/?support-data=%(support_data)s'
HOSTINGSVCS_HOOK_REGEX = b'(?:Reviewed at %(server_url)sr/|Review request #)(?P<id>\\d+)'
HOSTINGSVCS_HOOK_REGEX_FLAGS = re.IGNORECASE
SVNTOOL_BACKENDS = [
 b'reviewboard.scmtools.svn.pysvn',
 b'reviewboard.scmtools.svn.subvertpy']
GRAVATAR_DEFAULT = b'mm'
TEMPLATE_DIRS = [
 os.path.join(REVIEWBOARD_ROOT, b'templates')]
TEMPLATE_LOADERS = [
 (
  b'djblets.template.loaders.conditional_cached.Loader',
  ('django.template.loaders.filesystem.Loader', 'djblets.template.loaders.namespaced_app_dirs.Loader',
 'djblets.extensions.loaders.Loader'))]
TEMPLATE_CONTEXT_PROCESSORS = [
 b'django.contrib.auth.context_processors.auth',
 b'django.contrib.messages.context_processors.messages',
 b'django.core.context_processors.debug',
 b'django.core.context_processors.i18n',
 b'django.core.context_processors.media',
 b'django.core.context_processors.request',
 b'django.core.context_processors.static',
 b'djblets.cache.context_processors.ajax_serial',
 b'djblets.cache.context_processors.media_serial',
 b'djblets.siteconfig.context_processors.siteconfig',
 b'djblets.siteconfig.context_processors.settings_vars',
 b'djblets.urls.context_processors.site_root',
 b'reviewboard.accounts.context_processors.auth_backends',
 b'reviewboard.accounts.context_processors.profile',
 b'reviewboard.admin.context_processors.version',
 b'reviewboard.site.context_processors.localsite']
EXTENSIONS_ENABLED_BY_DEFAULT = [
 b'rbintegrations.extension.RBIntegrationsExtension']
try:
    import settings_local
    from settings_local import *
except ImportError as exc:
    dependency_error(b'Unable to import settings_local.py: %s' % exc)

for db_info in DATABASES.values():
    if db_info[b'ENGINE'] == b'django.db.backends.mysql':
        db_info[b'ENGINE'] = b'djblets.db.backends.mysql'

SESSION_COOKIE_PATH = SITE_ROOT
INSTALLED_APPS = RB_BUILTIN_APPS + RB_EXTRA_APPS + [b'django_evolution']
MIDDLEWARE_CLASSES += RB_EXTRA_MIDDLEWARE_CLASSES
TEMPLATES = [
 {b'BACKEND': b'django.template.backends.django.DjangoTemplates', 
    b'DIRS': TEMPLATE_DIRS, 
    b'OPTIONS': {b'context_processors': TEMPLATE_CONTEXT_PROCESSORS, 
                 b'debug': DEBUG, 
                 b'loaders': TEMPLATE_LOADERS}}]
if not LOCAL_ROOT:
    local_dir = os.path.dirname(settings_local.__file__)
    if os.path.exists(os.path.join(local_dir, b'reviewboard')):
        LOCAL_ROOT = os.path.join(local_dir, b'reviewboard')
        PRODUCTION = False
    else:
        LOCAL_ROOT = os.path.dirname(local_dir)
if PRODUCTION:
    SITE_DATA_DIR = os.path.join(LOCAL_ROOT, b'data')
else:
    SITE_DATA_DIR = os.path.dirname(LOCAL_ROOT)
HTDOCS_ROOT = os.path.join(LOCAL_ROOT, b'htdocs')
STATIC_ROOT = os.path.join(HTDOCS_ROOT, b'static')
MEDIA_ROOT = os.path.join(HTDOCS_ROOT, b'media')
ADMIN_MEDIA_ROOT = STATIC_ROOT + b'admin/'
EXTENSIONS_STATIC_ROOT = os.path.join(MEDIA_ROOT, b'ext')
HAYSTACK_CONNECTIONS = {b'default': {b'ENGINE': b'haystack.backends.whoosh_backend.WhooshEngine', 
                b'PATH': os.path.join(SITE_DATA_DIR, b'search-index')}}
HAYSTACK_SIGNAL_PROCESSOR = b'reviewboard.search.signal_processor.SignalProcessor'
if b'staticfiles' not in CACHES:
    CACHES[b'staticfiles'] = {b'BACKEND': b'django.core.cache.backends.locmem.LocMemCache', b'LOCATION': b'staticfiles-filehashes'}
CACHES[b'forwarded_backend'] = CACHES[b'default']
CACHES[b'default'] = {b'BACKEND': b'djblets.cache.forwarding_backend.ForwardingCacheBackend', 
   b'LOCATION': b'forwarded_backend'}
STATIC_DIRECTORY = b'static/'
STATIC_URL = getattr(settings_local, b'STATIC_URL', SITE_ROOT + STATIC_DIRECTORY)
MEDIA_DIRECTORY = b'media/'
MEDIA_URL = getattr(settings_local, b'MEDIA_URL', SITE_ROOT + MEDIA_DIRECTORY)
LOGIN_URL = SITE_ROOT + b'account/login/'
LOGIN_REDIRECT_URL = SITE_ROOT + b'dashboard/'
if RUNNING_TEST:
    PIPELINE_COMPILERS = []
else:
    PIPELINE_COMPILERS = [
     b'djblets.pipeline.compilers.es6.ES6Compiler',
     b'djblets.pipeline.compilers.less.LessCompiler']
NODE_PATH = os.path.join(REVIEWBOARD_ROOT, b'..', b'node_modules')
os.environ[b'NODE_PATH'] = NODE_PATH
PIPELINE = {b'PIPELINE_ENABLED': PRODUCTION or not DEBUG or os.getenv(b'FORCE_BUILD_MEDIA', b''), 
   b'COMPILERS': PIPELINE_COMPILERS, 
   b'JAVASCRIPT': PIPELINE_JAVASCRIPT, 
   b'STYLESHEETS': PIPELINE_STYLESHEETS, 
   b'JS_COMPRESSOR': b'pipeline.compressors.uglifyjs.UglifyJSCompressor', 
   b'CSS_COMPRESSOR': None, 
   b'BABEL_BINARY': os.path.join(NODE_PATH, b'babel-cli', b'bin', b'babel.js'), 
   b'BABEL_ARGUMENTS': [
                      b'--presets', b'es2015', b'--plugins', b'dedent',
                      b'-s', b'true'], 
   b'LESS_BINARY': os.path.join(NODE_PATH, b'less', b'bin', b'lessc'), 
   b'LESS_ARGUMENTS': [
                     b'--include-path=%s' % STATIC_ROOT,
                     b'--no-color',
                     b'--source-map',
                     b'--js',
                     b'--autoprefix=> 2%, ie >= 9',
                     b'--global-var=STATIC_ROOT=""'], 
   b'UGLIFYJS_BINARY': os.path.join(NODE_PATH, b'uglify-js', b'bin', b'uglifyjs')}
TEST_PACKAGES = [
 b'reviewboard']
ABSOLUTE_URL_OVERRIDES = {b'auth.user': lambda u: reverse(b'user', kwargs={b'username': u.username})}
FEATURE_CHECKER = b'reviewboard.features.checkers.RBFeatureChecker'
OAUTH2_PROVIDER = {b'APPLICATION_MODEL': b'oauth.Application', 
   b'DEFAULT_SCOPES': b'root:read', 
   b'SCOPES': {}}
fail_if_missing_dependencies()