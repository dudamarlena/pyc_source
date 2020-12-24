# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/foundry/utils.py
# Compiled at: 2015-04-30 10:11:23
from datetime import date
import random
from django.core.cache import cache
from django.conf import settings
try:
    from django.utils.http import is_safe_url
except ImportError:
    import urlparse

    def is_safe_url(url, host=None):
        """
        Copied from Django 1.4.10:
        https://github.com/django/django/blob/1.4.10/django/utils/http.py#L228
        """
        if not url:
            return False
        url_info = urlparse.urlparse(url)
        return (not url_info[1] or url_info[1] == host) and (not url_info[0] or url_info[0] in ('http',
                                                                                                'https'))


from preferences import preferences
_foundry_utils_cache = {}

def _build_view_names_recurse(url_patterns=None, namespace=None):
    """
    Returns a tuple of url pattern names suitable for use as field choices
    """
    if url_patterns is None:
        urlconf = settings.ROOT_URLCONF
        url_patterns = __import__(settings.ROOT_URLCONF, globals(), locals(), [
         'urlpatterns'], -1).urlpatterns
    result = []
    for pattern in url_patterns:
        try:
            if pattern.name is not None:
                if pattern.regex.pattern.find('<') == -1:
                    key = ''
                    if namespace:
                        key = namespace + ':'
                    key += pattern.name
                    result.append((key, key))
        except AttributeError:
            if not pattern.regex.pattern.startswith('^admin'):
                try:
                    result += _build_view_names_recurse(pattern.url_patterns, pattern.namespace)
                except AttributeError:
                    pass

    return result


def get_view_choices():
    if not _foundry_utils_cache.has_key('get_view_choices'):
        result = _build_view_names_recurse()
        result.sort()
        _foundry_utils_cache['get_view_choices'] = result
    return _foundry_utils_cache['get_view_choices']


def get_preference(klass_name, attr):
    key = 'jmbo_foundry' + str(settings.SITE_ID) + klass_name + attr
    empty_marker = '__empty__'
    none_marker = '__none__'
    v = cache.get(key, empty_marker)
    if v != empty_marker:
        if v == none_marker:
            return
        else:
            return v

    v = getattr(getattr(preferences, klass_name), attr)
    if v is None:
        cache.set(key, none_marker, 60)
    else:
        cache.set(key, v, 60)
    return v


def get_age(dob):
    """
    Calculates age from date of birth (datetime.date object). Adapted from:
    http://stackoverflow.com/questions/2217488/age-from-birthdate-in-python
    """
    today = date.today()
    try:
        birthday = dob.replace(year=today.year)
    except ValueError:
        birthday = dob.replace(year=today.year, day=born.day - 1)

    if birthday > today:
        return today.year - dob.year - 1
    else:
        return today.year - dob.year


def generate_random_key(length, valid_characters='abcdefghijklmnopqrstuvwxyz0123456789'):
    key = ''
    for i in range(length):
        key = '%s%s' % (key, random.choice(valid_characters))

    return key