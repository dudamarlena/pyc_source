# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nazrul/www/python/Contributions/apps/hybrid-access-control-system/hacs/events.py
# Compiled at: 2016-07-13 15:01:16
# Size of source mod 2**32: 3379 bytes
from __future__ import unicode_literals
import logging
from django.conf import settings
from django.core.cache import caches
from django.contrib.auth.models import Group
from .globals import HACS_SITE_CACHE
from .utils import set_site_settings
from .lru_wrapped import get_user_key
from .lru_wrapped import get_group_key
from .lru_wrapped import get_site_urlconf
from .defaults import HACS_CACHE_SETTING_NAME
from .lru_wrapped import get_site_http_methods
from .lru_wrapped import site_in_maintenance_mode
from .lru_wrapped import get_site_blacklisted_uri
from .lru_wrapped import get_site_whitelisted_uri
from .lru_wrapped import get_generated_urlconf_file
from .lru_wrapped import get_generated_urlconf_module
__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'
logger = logging.getLogger('hacs.events')

class DummyRequest(object):
    __doc__ = ''

    def __init__(self):
        """"""
        self.site = None


def post_save_routingtable_model(sender, **kwargs):
    """"""
    if not kwargs['created']:
        get_generated_urlconf_file.cache_clear()
        get_generated_urlconf_module.cache_clear()


def post_save_siteroutingrules_model(sender, **kwargs):
    """"""
    instance = kwargs['instance']
    if instance.is_active and instance.maintenance_mode:
        set_site_settings(instance.site)
    else:
        try:
            del HACS_SITE_CACHE[instance.site.domain]
        except KeyError:
            pass

    _invalidate_site_lru()


def post_save_contenttyperoutingrules_model(sender, **kwargs):
    """"""
    cache = caches[getattr(settings, 'HACS_CACHE_SETTING_NAME', HACS_CACHE_SETTING_NAME)]
    is_group = (kwargs['instance'].content_type.app_label, kwargs['instance'].content_type.model) == ('auth',
                                                                                                      'group')
    request = DummyRequest()
    request.site = kwargs['instance'].site
    if is_group:
        group = Group.objects.get(pk=kwargs['instance'].object_id)
        group_key = get_group_key(request, group)
        if cache.get(group, None):
            cache.delete(group_key)
        for user in group.user_set.all():
            request.user = user
            user_key = get_user_key(request)
            if cache.get(user_key, None):
                cache.delete(user_key)
                continue

    else:
        from django.contrib.auth import get_user_model
        request.user = get_user_model().objects.get(pk=kwargs['instance'].object_id)
        user_key = get_user_key(request)
    if cache.get(user_key, None):
        cache.delete(user_key)
    _invalidate_contenttype_lru()


def _invalidate_site_lru():
    """"""
    get_site_urlconf.cache_clear()
    site_in_maintenance_mode.cache_clear()
    get_site_http_methods.cache_clear()
    get_site_blacklisted_uri.cache_clear()
    get_site_whitelisted_uri.cache_clear()


def _invalidate_contenttype_lru():
    """"""
    get_group_key.cache_clear()
    get_user_key.cache_clear()
    get_generated_urlconf_module.cache_clear()
    get_generated_urlconf_file.cache_clear()