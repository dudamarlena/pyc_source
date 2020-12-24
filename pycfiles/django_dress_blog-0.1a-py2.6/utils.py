# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dress_blog/utils.py
# Compiled at: 2012-07-20 05:27:44
import datetime, re
try:
    from hashlib import md5
except ImportError:
    import md5

from django.db.models.manager import Manager
from django.conf import settings
from django.utils import formats
from django.utils.dateformat import format
from django.utils.encoding import smart_str
from django.utils.translation import ungettext, ugettext

def clean_cache_key(key):
    """Replace spaces with '-' and hash if length is greater than 250."""
    cache_key = re.sub('\\s+', '-', key)
    cache_key = smart_str(cache_key)
    if len(cache_key) > 250:
        m = md5()
        m.update(cache_key)
        cache_key = cache_key[:200] + '-' + m.hexdigest()
    return cache_key


def create_cache_key(klass, field=None, field_value=None):
    """
    Helper to generate standard cache keys.

    Concepts borrowed from mmalone's django-caching:
    http://github.com/mmalone/django-caching/blob/ef7dd47e9beff39496e6a28ae129bae1b5f9ed71/app/managers.py

    Required Arguments
    ------------------
        'klass'
            Model or Manager

        'field'
            string, the specific Model field name used to create a more
            specific cache key. If you specify a field, it is used for the
            lookup to grab the value.

         'field_value'
            value, unique value used to generate a distinct key. Often
            this will be the ID, slug, name, etc.

            *Note: could be optimized/restricted to pk lookup only

    Returns
    -------
        'key'
            The key name.

    Example
    --------
        >> from blog.models import Post
        >> slug_val = 'test-foo'
        >> mykey = create_cache_key(Post, 'slug', slug_val)
        >> obj = cache.get(mykey)
    """
    key_model = '%s.%s.%s:%s'
    key = ''
    if field and field_value:
        if isinstance(klass, Manager):
            key = key_model % (klass.model._meta.app_label, klass.model._meta.module_name, field, field_value)
        else:
            key = key_model % (klass._meta.app_label, klass._meta.module_name, field, field_value)
    if not key:
        raise Exception('Cache key cannot be empty.')
    return clean_cache_key(key)


def colloquial_date(d, fmt):
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime(d.year, d.month, d.day)
    delta = datetime.datetime.today() - d
    since = delta.days
    if since <= 0:
        return ugettext('Today')
    if since <= 1:
        return ugettext('Yesterday')
    if 2 <= since <= 6:
        return ugettext('Last %(weekday)s') % {'weekday': format(d, 'l')}
    try:
        return formats.date_format(d, fmt)
    except AttributeError:
        try:
            return format(d, fmt)
        except AttributeError:
            return ''