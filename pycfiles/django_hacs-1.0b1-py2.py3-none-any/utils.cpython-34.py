# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nazrul/www/python/Contributions/apps/hybrid-access-control-system/hacs/utils.py
# Compiled at: 2016-07-12 02:07:20
# Size of source mod 2**32: 12101 bytes
from __future__ import unicode_literals
import os, re, copy, glob, json, datetime, warnings, importlib, collections
from django.apps import apps
from django.utils import six
from django.conf import settings
from django.utils import timezone
from django.utils._os import safe_join
from django.utils.encoding import smart_text
from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.module_loading import module_has_submodule
from .models import SiteRoutingRules
from .globals import HACS_SITE_CACHE
from .globals import HTTP_METHOD_LIST
from .defaults import HACS_FALLBACK_URLCONF
from .defaults import HACS_GENERATED_URLCONF_DIR
from .globals import HACS_GENERATED_FILENAME_PREFIX
__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'
UserModel = get_user_model()
urlconf_template = '# -*- coding: utf-8 -*-\nfrom django.conf.urls import include\nfrom django.conf.urls import url\nfrom django.contrib import admin\n\n__author__ = "Md Nazrul Islam<connect2nazrul@gmail.com>"\n\nadmin.autodiscover()\nurlpatterns = [\n{urlpatterns}\n]\n\n{handlers}\n'

def set_site_settings(site, silent_if_not_exist=True):
    """
    :param site:
    :param silent_if_not_exist
    :return:
    """
    try:
        site_rules = SiteRoutingRules.objects.get(site=site)
    except SiteRoutingRules.DoesNotExist:
        if not silent_if_not_exist:
            raise
        warnings.warn('%s has not assigned any route yet!' % site.domain)
        try:
            HACS_SITE_CACHE[site.domain].update({'urlconf': getattr(settings, 'HACS_FALLBACK_URLCONF', HACS_FALLBACK_URLCONF)})
        except KeyError:
            HACS_SITE_CACHE[site.domain] = {'urlconf': getattr(settings, 'HACS_FALLBACK_URLCONF', HACS_FALLBACK_URLCONF)}

    else:
        generate_urlconf_file_on_demand(site_rules.route)
        generated_urlconf_module = get_generated_urlconf_module(get_generated_urlconf_file(site_rules.route.route_name))
    try:
        HACS_SITE_CACHE[site.domain].update({'urlconf': generated_urlconf_module, 
         'maintenance_mode': site_rules.maintenance_mode, 
         'allowed_http_methods': site_rules.allowed_method or HTTP_METHOD_LIST, 
         'blacklisted_uri': site_rules.blacklisted_uri, 
         'whitelisted_uri': site_rules.whitelisted_uri, 
         'is_active': site_rules.is_active})
    except KeyError:
        HACS_SITE_CACHE[site.domain] = {'urlconf': generated_urlconf_module,  'maintenance_mode': site_rules.maintenance_mode, 
         'allowed_http_methods': site_rules.allowed_method, 
         'blacklisted_uri': site_rules.blacklisted_uri, 
         'whitelisted_uri': site_rules.whitelisted_uri, 
         'is_active': site_rules.is_active}


def get_site_settings(site):
    """
    @Linked to `lru_wrapped`
    :param site
    """
    try:
        return HACS_SITE_CACHE[site.domain]
    except KeyError:
        set_site_settings(site)
        return HACS_SITE_CACHE[site.domain]


def get_site_urlconf(site):
    """
    @Linked to `lru_wrapped`
    :param site
    """
    return get_site_settings(site)['urlconf']


def get_site_blacklisted_uri(site):
    """
    @Linked to `lru_wrapped`
    :param site
    """
    return get_site_settings(site)['blacklisted_uri']


def get_site_whitelisted_uri(site):
    """
    @Linked to `lru_wrapped`
    :param site
    """
    return get_site_settings(site)['whitelisted_uri']


def site_in_maintenance_mode(site):
    """
    @Linked to `lru_wrapped`
    :param site
    """
    try:
        return HACS_SITE_CACHE[site.domain]['maintenance_mode']
    except KeyError:
        set_site_settings(site, False)
        return HACS_SITE_CACHE[site.domain]['maintenance_mode']


def get_site_http_methods(site):
    """
    @Linked to `lru_wrapped`
    :param site
    """
    try:
        return HACS_SITE_CACHE[site.domain]['allowed_http_methods']
    except KeyError:
        set_site_settings(site)
        return HACS_SITE_CACHE[site.domain]['allowed_http_methods'] or HTTP_METHOD_LIST


def get_group_key(request, group, prefix='hacl', suffix=None):
    """
    @Linked to `lru_wrapped`
    :param request:
    :param group:
    :param prefix:
    :param suffix:
    :return:
    """
    if suffix is None:
        suffix = ''
    return '{prefix}:site_{site_id}:group_{group_id}{suffix}'.format(prefix=prefix, site_id=request.site.id, group_id=group.id, suffix=suffix)


def get_user_key(request, prefix='hacl', suffix=None):
    """
    @Linked to `lru_wrapped`
    :param request:
    :param prefix:
    :param suffix:
    :return:
    """
    if suffix is None:
        suffix = ''
    return '{prefix}:site_{site_id}:user_{user_id}{suffix}'.format(prefix=prefix, site_id=request.site.id, user_id=request.user.is_authenticated() and request.user.id or 0, suffix=suffix)


def get_generated_urlconf_file(route_name, prefix=None):
    """
    @Linked to `lru_wrapped`
    :param route_name
    :param prefix
    :return:
    """
    route_name = sanitize_filename(route_name)
    if prefix:
        prefix = sanitize_filename(prefix)
    else:
        prefix = HACS_GENERATED_FILENAME_PREFIX
    return safe_join(getattr(settings, 'HACS_GENERATED_URLCONF_DIR', HACS_GENERATED_URLCONF_DIR), '%s_%s_urls.py' % (
     prefix, route_name))


def get_generated_urlconf_module(filename, validation=True):
    """
    @Linked to `lru_wrapped`
    :param filename:
    :param validation:
    :return:
    """
    if validation:
        if not os.path.exists(filename):
            raise OSError("Specified file: %s does't exists!" % filename)
    return filename.split('/')[(-1)].split('.')[0]


def generate_urlconf_file_on_demand(route):
    """
    """
    generated_urlconf_file = get_generated_urlconf_file(route.route_name)
    route_updated_on = route.updated_on
    if route_updated_on:
        route_updated_on = route_updated_on.astimezone(timezone.utc).replace(tzinfo=None)
    if not os.path.exists(generated_urlconf_file) or os.path.exists(generated_urlconf_file) and route_updated_on and datetime.datetime.utcfromtimestamp(os.path.getmtime(generated_urlconf_file)) < route_updated_on:
        generate_urlconf_file(generated_urlconf_file, route)


def generate_urlconf_file(filename, route):
    """
    :param filename:
    :param route:
    :return:
    """
    with open(filename, 'w') as (f):
        urlpatterns = ''
        for url in route.urls:
            url_module = url['url_module']
            if url.get('app_name'):
                if isinstance(url_module, six.string_types):
                    url_module = (
                     url_module, url.get('app_name'))
            else:
                if isinstance(url_module, (tuple, list, set)):
                    if len(url_module) == 1:
                        url_module = tuple(url_module) + url.get('app_name')
                if not isinstance(url_module, six.string_types):
                    if isinstance(url_module, (list, set)):
                        url_module = tuple(url_module)
                    if isinstance(url_module, tuple):
                        if len(url_module) > 2:
                            url_module = url_module[0:2]
                            if not url.get('namespace'):
                                url['namespace'] = url_module[2]
                        url_module = smart_text(url_module)
                    elif url_module != 'admin.site.urls':
                        url_module = "'%s'" % url_module
                    urlpatterns += "\turl(r'{prefix}', include({url_module}{namespace})),\n".format(prefix=url.get('prefix') + '/' if url.get('prefix', None) else '^', url_module=url_module, namespace=url.get('namespace') and ", namespace='%s'" % url.get('namespace', None) or '')

        error_handlers = ''
        if route.handlers:
            for name, handler in route.handlers.items() or {}.items():
                error_handlers += '%s="%s"\n' % (name, handler)

        f.write(copy.copy(urlconf_template).format(urlpatterns=urlpatterns, handlers=error_handlers))


def sanitize_filename(filename):
    """
    :param filename:
    :return:
    """
    filename = re.sub('[^A-Za-z0-9\\-_]+', '', filename)
    return filename.replace('-', '_')


def get_installed_apps_urlconf(pattern='*urls.py', to_json=False, exclude=()):
    """
    @Linked to `lru_wrapped`
    :param pattern:
    :param to_json:
    :param exclude: apps those should be excluded
    :return:
    """
    result = collections.deque()
    handlers = ('handler400', 'handler403', 'handler404', 'handler500')
    if exclude:
        if isinstance(exclude, six.string_types):
            exclude = (
             exclude,)
    for app in apps.get_app_configs():
        if app.label in exclude:
            continue
        urlconf_modules = map(lambda x: '.'.join((app.name, x.replace(app.path, '').lstrip('/').split('.')[0])), glob.glob(os.path.join(app.path, pattern)))
        urlconf_dir = os.path.join(app.path, 'urls')
        if os.path.exists(urlconf_dir):
            if module_has_submodule(app.module, 'urls'):
                urls_module = importlib.import_module('.'.join((app.name, 'urls')))
                if hasattr(urls_module, 'urlpatterns'):
                    urlconf_modules += ['.'.join((app.name, 'urls'))]
                urlconf_modules += map(lambda x: '.'.join((app.name, 'urls', x.replace(app.path, '').lstrip('/').split('.')[0])), glob.glob(os.path.join(urlconf_dir, pattern)))
        if not urlconf_modules:
            continue
        for urlconf in urlconf_modules:
            urlconf_module = importlib.import_module(urlconf)
            if not hasattr(urlconf_module, 'urlpatterns'):
                continue
            error_handlers = collections.defaultdict(dict)
            for handler in handlers:
                if hasattr(urlconf_module, handler):
                    error_handlers[handler] = getattr(urlconf_module, handler)
                    continue

            item = collections.namedtuple('app_' + app.name.replace('.', '_'), ['module', 'app_label', 'prefix', 'error_handlers'])
            result.append(item(module=urlconf, app_label=app.label, error_handlers=error_handlers, prefix=None))

    if to_json:
        return json.dumps(list(result), cls=DjangoJSONEncoder)
    else:
        return tuple(result)


def get_user_object(username_or_email_or_mobile, silent=True):
    """
    :param
    :param username_or_email_or_mobile:
    :param silent:
    :return:
    """
    try:
        return UserModel.objects.get(**{UserModel.USERNAME_FIELD: username_or_email_or_mobile})
    except UserModel.DoesNotExist:
        if not silent:
            raise
        return


__all__ = [str(x) for x in ('set_site_settings', 'get_site_settings', 'get_site_urlconf',
                            'get_group_key', 'get_user_key', 'get_generated_urlconf_file',
                            'get_generated_urlconf_module', 'generate_urlconf_file',
                            'generate_urlconf_file_on_demand', 'sanitize_filename',
                            'get_installed_apps_urlconf', 'get_user_object', 'site_in_maintenance_mode',
                            'get_site_http_methods', 'get_site_blacklisted_uri',
                            'get_site_whitelisted_uri')]