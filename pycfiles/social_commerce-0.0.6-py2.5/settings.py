# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialcommerce/settings.py
# Compiled at: 2009-11-01 00:53:14
import os.path, pinax, posixpath
PINAX_ROOT = os.path.realpath(os.path.dirname(pinax.__file__))
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
PINAX_THEME = 'default'
try:
    DEBUG
except NameError:
    DEBUG = True

TEMPLATE_DEBUG = DEBUG
SERVE_MEDIA = DEBUG
ADMINS = ()
MANAGERS = ADMINS
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'dev.db'
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''
if DATABASE_ENGINE == 'mysql':
    DATABASE_OPTIONS = {'init_command': 'SET NAMES "utf8"'}
TIME_ZONE = 'US/Eastern'
LANGUAGE_CODE = 'en'
SITE_ID = 1
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'site_media', 'media')
MEDIA_URL = '/site_media/media/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'site_media', 'static')
STATIC_URL = '/site_media/static/'
STATICFILES_DIRS = (
 (
  'social_project', os.path.join(PROJECT_ROOT, 'media')),
 (
  'pinax', os.path.join(PINAX_ROOT, 'media', PINAX_THEME)))
ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, 'admin/')
SECRET_KEY = ''
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.load_template_source', 'django.template.loaders.app_directories.load_template_source')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django_openid.consumer.SessionConsumer', 'account.middleware.LocaleMiddleware',
                      'django.middleware.doc.XViewMiddleware', 'pagination.middleware.PaginationMiddleware',
                      'django_sorting.middleware.SortingMiddleware', 'djangodblog.middleware.DBLogMiddleware',
                      'pinax.middleware.security.HideSensistiveFieldsMiddleware',
                      'django.middleware.transaction.TransactionMiddleware', 'cms.middleware.CurrentPageMiddleware',
                      'cms.middleware.MultilingualURLMiddleware')
ROOT_URLCONF = 'socialcommerce.urls'
from django.contrib import admindocs
DJANGO_DOCS_ROOT = os.path.realpath(os.path.dirname(admindocs.__file__))
TEMPLATE_DIRS = (
 os.path.join(PROJECT_ROOT, 'templates'),
 os.path.join(PINAX_ROOT, 'templates', PINAX_THEME),
 os.path.join(DJANGO_DOCS_ROOT, 'templates'))
TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.auth', 'django.core.context_processors.debug',
                               'django.core.context_processors.i18n', 'django.core.context_processors.media',
                               'django.core.context_processors.request', 'pinax.core.context_processors.pinax_settings',
                               'notification.context_processors.notification', 'announcements.context_processors.site_wide_announcements',
                               'account.context_processors.openid', 'account.context_processors.account',
                               'messages.context_processors.inbox', 'friends_app.context_processors.invitations',
                               'socialcommerce.context_processors.combined_inbox_count')
COMBINED_INBOX_COUNT_SOURCES = ('messages.context_processors.inbox', 'friends_app.context_processors.invitations',
                                'notification.context_processors.notification')
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'django.contrib.humanize', 'django.contrib.markup',
                  'pinax.templatetags', 'notification', 'django_openid', 'emailconfirmation',
                  'django_extensions', 'robots', 'friends', 'mailer', 'messages',
                  'announcements', 'oembed', 'djangodblog', 'pagination', 'threadedcomments',
                  'threadedcomments_extras', 'wiki', 'swaps', 'timezones', 'app_plugins',
                  'voting', 'voting_extras', 'tagging', 'bookmarks', 'blog', 'ajax_validation',
                  'photologue', 'avatar', 'flag', 'microblogging', 'locations', 'uni_form',
                  'django_sorting', 'django_markup', 'analytics', 'profiles', 'staticfiles',
                  'account', 'signup_codes', 'tribes', 'photos', 'tag_app', 'topics',
                  'groups', 'cms', 'cms.plugins.text', 'cms.plugins.picture', 'cms.plugins.link',
                  'cms.plugins.file', 'mptt', 'django.contrib.admin')
ABSOLUTE_URL_OVERRIDES = {'auth.user': lambda o: '/profiles/%s/' % o.username}
MARKUP_FILTER_FALLBACK = 'none'
MARKUP_CHOICES = (
 ('restructuredtext', 'reStructuredText'),
 ('textile', 'Textile'),
 ('markdown', 'Markdown'),
 ('creole', 'Creole'))
WIKI_MARKUP_CHOICES = MARKUP_CHOICES
AUTH_PROFILE_MODULE = 'profiles.Profile'
NOTIFICATION_LANGUAGE_MODULE = 'account.Account'
ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_REQUIRED_EMAIL = False
ACCOUNT_EMAIL_VERIFICATION = False
EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG
CONTACT_EMAIL = 'feedback@example.com'
SITE_NAME = 'Pinax'
LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URLNAME = 'what_next'
INTERNAL_IPS = ('127.0.0.1', )
ugettext = lambda s: s
LANGUAGES = (('en', 'English'), )

class NullStream(object):

    def write(*args, **kwargs):
        pass

    writeline = write
    writelines = write


RESTRUCTUREDTEXT_FILTER_SETTINGS = {'cloak_email_addresses': True, 
   'file_insertion_enabled': False, 
   'raw_enabled': False, 
   'warning_stream': NullStream(), 
   'strip_comments': True}
BEHIND_PROXY = False
FORCE_LOWERCASE_TAGS = True
WIKI_REQUIRES_LOGIN = True
CMS_TEMPLATES = (
 (
  'base.html', ugettext('default')),)
execfile(PROJECT_ROOT + '/satchmo_settings.py')
try:
    DEBUG_TOOLBAR
except NameError:
    DEBUG_TOOLBAR = False

if DEBUG_TOOLBAR:
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware', )
    INSTALLED_APPS += ('debug_toolbar', )
    DEBUG_TOOLBAR_PANELS = ('debug_toolbar.panels.version.VersionDebugPanel', 'debug_toolbar.panels.timer.TimerDebugPanel',
                            'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
                            'debug_toolbar.panels.headers.HeaderDebugPanel', 'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
                            'debug_toolbar.panels.template.TemplateDebugPanel', 'debug_toolbar.panels.sql.SQLDebugPanel',
                            'debug_toolbar.panels.logger.LoggingPanel')
try:
    from local_settings import *
except ImportError:
    pass