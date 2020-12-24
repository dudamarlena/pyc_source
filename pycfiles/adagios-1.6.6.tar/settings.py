# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gardar/code/adagios/adagios/settings.py
# Compiled at: 2020-01-05 16:38:51
DEBUG = True
TEMPLATE_DEBUG = DEBUG
USE_TZ = True
import os
from glob import glob
from warnings import warn
import string
djangopath = os.path.dirname(__file__)
ADMINS = ()
MANAGERS = ADMINS
STATIC_URL = '/media/'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': '/tmp/test', 
               'USER': '', 
               'PASSWORD': '', 
               'HOST': '', 
               'PORT': ''}}
TIME_ZONE = None
USE_TZ = True
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
STATIC_URL = '/media/'
STATIC_ROOT = '%s/media/' % djangopath
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader')
MIDDLEWARE_CLASSES = ('django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.locale.LocaleMiddleware',
                      'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware',
                      'adagios.auth.AuthorizationMiddleWare')
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
LANGUAGES = (
 ('en', 'English'),
 ('fr', 'French'))
LOCALE_PATHS = (
 '%s/locale/' % djangopath,)
ROOT_URLCONF = 'adagios.urls'
TEMPLATE_DIRS = (
 '%s/templates' % djangopath,)
INSTALLED_APPS = [
 'django.contrib.sessions',
 'django.contrib.sites',
 'adagios.objectbrowser',
 'adagios.rest',
 'adagios.misc',
 'adagios.pnp',
 'adagios.contrib']
TEMPLATE_CONTEXT_PROCESSORS = ('adagios.context_processors.on_page_load', 'django.core.context_processors.debug',
                               'django.core.context_processors.i18n', 'django.core.context_processors.static',
                               'django.core.context_processors.request', 'django.contrib.messages.context_processors.messages')
THEMES_FOLDER = 'themes'
THEME_DEFAULT = 'default'
THEME_ENTRY_POINT = 'style.css'
USER_PREFS_PATH = '/var/lib/adagios/userdata/'
TOPMENU_HOME = 'Adagios'
TOPMENU_ITEMS = [
 ('Configure', 'objectbrowser', 'objectbrowser.views.list_object_types', 'glyph-edit'),
 ('Nagios', 'nagios', 'misc.views.nagios', 'glyph-list')]
UNHANDLED_SERVICES = {'state__isnot': 0, 
   'acknowledged': 0, 
   'scheduled_downtime_depth': 0, 
   'host_state': 0, 
   'host_scheduled_downtime_depth': 0, 
   'host_acknowledged': 0}
UNHANDLED_HOSTS = {'state': 1, 
   'acknowledged': 0, 
   'scheduled_downtime_depth': 0}
ALLOWED_HOSTS = [
 '*']
graphite_url = 'http://localhost:9091'
GRAPHITE_PERIODS = [
 ('4 hours', 'hours', '-4h'),
 ('One day', 'day', '-1d'),
 ('One week', 'week', '-1w'),
 ('One month', 'month', '-1mon'),
 ('One year', 'year', '-1y')]
graphite_querystring = 'target={host_}.{service_}.{metric_}&width=500&height=200&from={from_}d&lineMode=connected&title={title}&target={host_}.{service_}.{metric_}_warn&target={host_}.{service_}.{metric_}_crit'
graphite_title = '{host} - {service} - {metric}'
GRAPHITE_DEFAULT_TAB = 'day'
nagios_config = None
nagios_url = '/nagios'
nagios_init_script = None
nagios_service = 'nagios'
nagios_binary = '/usr/bin/nagios'
livestatus_path = None
livestatus_limit = 500
default_host_template = 'generic-host'
default_service_template = 'generic-service'
default_contact_template = 'generic-contact'
enable_githandler = False
enable_loghandler = False
enable_authorization = False
enable_status_view = True
enable_bi = True
enable_pnp4nagios = True
enable_graphite = False
enable_local_logs = True
contrib_dir = '/var/lib/adagios/contrib/'
serverside_includes = '/etc/adagios/ssi'
escape_html_tags = True
warn_if_selinux_is_active = True
destination_directory = '/etc/nagios/adagios/'
administrators = 'nagiosadmin,@users'
pnp_url = '/pnp4nagios'
pnp_filepath = '/usr/share/nagios/html/pnp4nagios/index.php'
include = ''
django_secret_key = ''
map_center = '64.119595,-21.655426'
map_zoom = '10'
title_prefix = 'Adagios - '
auto_reload = False
refresh_rate = '30'
plugins = {}
PROFILE_LOG_BASE = '/var/lib/adagios'
adagios_configfile = '/etc/adagios/adagios.conf'

def reload_configfile(adagios_configfile=None):
    """Process adagios.conf style file and any includes; updating the settings"""
    if not adagios_configfile:
        adagios_configfile = globals()['adagios_configfile']
    try:
        if not os.path.exists(adagios_configfile):
            alternative_adagios_configfile = '%s/adagios.conf' % djangopath
            message = "Config file '{adagios_configfile}' not found. Using {alternative_adagios_configfile} instead."
            warn(message.format(**locals()))
            adagios_configfile = alternative_adagios_configfile
            open(adagios_configfile, 'a').close()
        execfile(adagios_configfile, globals())
        configfiles = glob(include)
        for configfile in configfiles:
            execfile(configfile, globals())

    except IOError as e:
        warn('Unable to open %s: %s' % (adagios_configfile, e.strerror))


reload_configfile()
try:
    from django.utils.crypto import get_random_string
except ImportError:

    def get_random_string(length, stringset=string.ascii_letters + string.digits + string.punctuation):
        """
        Returns a string with `length` characters chosen from `stringset`
        >>> len(get_random_string(20)) == 20
        """
        return ('').join([ stringset[(i % len(stringset))] for i in [ ord(x) for x in os.urandom(length) ] ])


if not django_secret_key:
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    SECRET_KEY = get_random_string(50, chars)
    try:
        data = "\n# Automaticly generated secret_key\ndjango_secret_key = '%s'\n" % SECRET_KEY
        with open(adagios_configfile, 'a') as (config_fh):
            config_fh.write(data)
    except Exception as e:
        warn('ERROR: Got %s while trying to save django secret_key in %s' % (type(e), adagios_configfile))

else:
    SECRET_KEY = django_secret_key
ALLOWED_INCLUDE_ROOTS = (serverside_includes,)
if enable_status_view:
    plugins['status'] = 'adagios.status'
if enable_bi:
    plugins['bi'] = 'adagios.bi'
for k, v in plugins.items():
    INSTALLED_APPS.append(v)

PREFS_DEFAULT = {'language': 'en', 
   'theme': THEME_DEFAULT, 
   'refresh_rate': refresh_rate}
os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = 'localhost:8000-9000'
TEST_RUNNER = 'django.test.runner.DiscoverRunner'