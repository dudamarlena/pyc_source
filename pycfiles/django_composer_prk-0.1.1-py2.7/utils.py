# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/composer/utils.py
# Compiled at: 2017-10-20 11:35:08
_composer_utils_cache = {}

def _build_view_names_recurse(url_patterns=None, namespace=None):
    """Returns a tuple of url pattern names suitable for use as field choices.
    """
    if url_patterns is None:
        from django.conf import settings
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
    if not _composer_utils_cache.has_key('get_view_choices'):
        result = _build_view_names_recurse()
        result.sort()
        _composer_utils_cache['get_view_choices'] = result
    return _composer_utils_cache['get_view_choices']