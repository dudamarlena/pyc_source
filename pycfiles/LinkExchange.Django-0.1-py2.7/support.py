# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/linkexchange_django/support.py
# Compiled at: 2011-05-12 16:12:18
import os, os.path, urllib, logging
from django.conf import settings
from django.contrib.sites.models import Site, RequestSite
from django.utils.encoding import iri_to_uri
from linkexchange.config import file_config, ConfigError
from linkexchange.utils import normalize_uri
from linkexchange.platform import Platform
from linkexchange.clients import PageRequest
log = logging.getLogger('linkexchange.django')
platform = None
formatters = None
options = None

def configure():
    global formatters
    global options
    global platform

    def check_mod_dir(mod):
        if isinstance(mod, basestring):
            try:
                mod = __import__(mod, {}, {}, [''])
            except ImportError:
                return

        fn = os.path.join(os.path.dirname(mod.__file__), 'linkexchange.cfg')
        if not os.path.exists(fn):
            return
        else:
            return fn

    try:
        real_settings = __import__(os.environ['DJANGO_SETTINGS_MODULE'], {}, {}, [''])
    except KeyError:
        real_settings = None

    try:
        cfgfile = settings.LINKEXCHANGE_CONFIG
    except AttributeError:
        cfgfile = None

    if not cfgfile and real_settings:
        cfgfile = check_mod_dir(real_settings)
    if not cfgfile:
        cfgfile = check_mod_dir(settings.ROOT_URLCONF)
    if cfgfile:
        defaults = {}
        if isinstance(cfgfile, basestring):
            defaults['basedir'] = os.path.abspath(os.path.dirname(cfgfile))
        else:
            if real_settings:
                defaults['basedir'] = os.path.abspath(os.path.dirname(real_settings.__file__))
            else:
                defaults['basedir'] = os.getcwd()
            try:
                if not file_config(globals(), cfgfile, defaults=defaults):
                    log.error('Unable to read configuration file: %s', cfgfile)
            except ConfigError as e:
                log.error('Configuration error: %s', str(e))

    try:
        platform = Platform(settings.LINKEXCHANGE_CLIENTS)
    except AttributeError:
        pass

    try:
        formatters = settings.LINKEXCHANGE_FORMATTERS
    except AttributeError:
        pass

    if options is None:
        options = {}
    try:
        options.update(settings.LINKEXCHANGE_OPTIONS)
    except AttributeError:
        pass

    if platform is None:
        log.warning('LinkExchange is not configured')
    return


def convert_request(request):
    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)
    path = request.path
    if type(path) == unicode:
        path = path.encode('utf-8')
    query_string = iri_to_uri(request.environ.get('QUERY_STRING', ''))
    request_uri = urllib.quote(path) + (query_string and '?' + query_string or '')
    request = PageRequest(host=options.get('host', current_site.domain), uri=normalize_uri(request_uri), cookies=request.COOKIES, remote_addr=request.META.get('REMOTE_ADDR', None), meta=request.META)
    return request


configure()