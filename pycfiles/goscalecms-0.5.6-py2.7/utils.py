# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/goscale/utils.py
# Compiled at: 2013-03-18 00:56:22
import datetime, urllib, urllib2, re, os, pytz
from goscale import conf
from django.core.cache import cache
from django import http
from django.core import urlresolvers
from django.utils import html as html_utils
from django.utils import simplejson
from django.utils import translation
from django import template
from django.utils import importlib
from django.core import exceptions
from django.contrib.sites import models as site_models
from django.conf import settings
from cms.models import CMSPlugin

def get_plugins(sites=None):
    """
    Returns all GoScale plugins

    It ignored all other django-cms plugins
    """
    plugins = []
    for plugin in CMSPlugin.objects.all():
        if plugin:
            cl = plugin.get_plugin_class().model
            if 'posts' in cl._meta.get_all_field_names():
                instance = plugin.get_plugin_instance()[0]
                plugins.append(instance)

    if sites and len(sites) > 0:
        onsite = []
        for plugin in plugins:
            try:
                if plugin.page.site in sites:
                    onsite.append(plugin)
            except AttributeError:
                continue

        return onsite
    return plugins


def update_plugin(plugin_id):
    """
    Updates a single plugin by ID

    Returns a plugin instance and posts count
    """
    try:
        instance = CMSPlugin.objects.get(id=plugin_id).get_plugin_instance()[0]
        instance.update()
    except:
        return (None, 0)

    return (
     instance, instance.posts.count())


def process_feed_tz_delta(date_string):
    date_match = re.findall('[\\-\\+]\\d{2}:?\\d{2}', date_string)
    if date_match:
        factor = 1
        tz_string = date_match[0].replace(':', '')
        if tz_string.startswith('-'):
            factor = -1
        tz_delta = (int(tz_string[-4:-2]) * 3600 + int(tz_string[-2:]) * 60) * factor
        return tz_delta
    return 0


def get_datetime_now():
    """ Returns now() in UTC timezone

    More info: http://pytz.sourceforge.net/
    """
    return datetime.datetime.now(tz=pytz.utc)


def get_utc(dt):
    """ Converts datetime to UTC timezone

    More info: http://pytz.sourceforge.net/
    """
    return dt.replace(tzinfo=pytz.utc)


def get_datetime_by_parsed(pDate, tz_delta=0):
    if not pDate:
        return None
    else:
        dt = datetime.datetime(pDate[0], pDate[1], pDate[2], pDate[3], pDate[4], pDate[5]) + datetime.timedelta(seconds=tz_delta)
        return get_utc(dt)


def get_short_summary(html):
    max_length_shortcontent = conf.GOSCALE_POST_SUMMARY_LIMIT
    content_temp = html_utils.strip_tags(html)
    if len(content_temp) < max_length_shortcontent:
        return content_temp
    shortcontent_temp = content_temp[:max_length_shortcontent]
    if shortcontent_temp.rfind('.') != -1:
        shortcontent_temp = shortcontent_temp[:shortcontent_temp.rfind('.') + 1]
    else:
        shortcontent_temp = shortcontent_temp[:shortcontent_temp.rfind(' ') + 1] + '...'
    return shortcontent_temp


def dict2obj(d):
    """A helper function which convert a dict to an object.
    """
    if isinstance(d, (list, tuple)):
        d = [ dict2obj(x) for x in d ]
    if not isinstance(d, dict):
        return d

    class ObjectFromDict(object):
        pass

    o = ObjectFromDict()
    for k in d:
        o.__dict__[k] = dict2obj(d[k])

    return o


def forge_request(url):
    """A helper function which forges a request for fetching json from vimeo and youku.
    """
    return urllib2.Request(url, None, {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'})