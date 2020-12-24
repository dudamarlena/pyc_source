# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thot/url.py
# Compiled at: 2013-03-05 21:43:25
from fnmatch import fnmatch
from os.path import splitext, split, relpath
from thot.utils import OrderedDict
registry = OrderedDict()

def get_url(page):
    """Returns the final output url string for `page`"""
    urlfunc = get_url_func(page)
    url = urlfunc(page)
    return url


def get_url_func(page):
    """
    Returns the entry from the url registry that matches the specified
    url header value.
    """
    path = page['path']
    url = page['url']
    for pattern in reversed(registry):
        rules = registry[pattern]
        if fnmatch(path, pattern):
            if url in rules:
                return rules[url]
            if pattern == '*' and url != 'default':
                return lambda **x: url
            if 'default' in rules:
                return rules['default']


def register(func=None, match='*'):
    """A registry for url rules"""

    def decorated(func):
        match_rules = registry.setdefault(match, {})
        match_rules[func.__name__] = func

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    if func is None:

        def decorator(func):
            return decorated(func)

        return decorator
    else:
        return decorated(func)


@register
def default(page):
    """default url rule"""
    path = page['path']
    ext = page['output_ext']
    url = splitext(path)[0] + '.' + ext
    head, tail = split(url)
    if tail == 'index.html':
        url = head + '/'
    return url


@register
def pretty(page):
    return '$year/$month/$day/$slug/'