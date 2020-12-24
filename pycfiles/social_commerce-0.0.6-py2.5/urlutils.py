# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialcommerce/apps/cms/urlutils.py
# Compiled at: 2009-10-31 23:19:40
import re
from django.conf import settings
any_path_re = re.compile('^/?[a-zA-Z0-9_-]+(/[a-zA-Z0-9_-]+)?/?$')

def levelize_path(path):
    """Splits given path to list of paths removing latest level in each step.
    
    >>> path = '/application/item/new'
    >>> levelize_path(path)
    ['/application/item/new', '/application/item', '/application']
    """
    parts = path.rstrip('/').split('/')
    paths = []
    for i in range(len(parts), 0, -1):
        sub_path = ('/').join(parts[:i])
        if sub_path:
            paths.append(sub_path)

    return paths


def urljoin(*segments):
    """Joins url segments together and appends trailing slash if required.
    
    >>> urljoin('a', 'b', 'c')
    'a/b/c/'
    
    >>> urljoin('a', '//b//', 'c')
    'a/b/c/'
    
    >>> urljoin('/a', '/b/', '/c/')
    '/a/b/c/'
    
    >>> urljoin('/a', '')
    '/a/'
    """
    cleaned_segments = map(lambda segment: segment.strip('/'), segments)
    nonempty_segments = filter(lambda segment: segment > '', cleaned_segments)
    url = ('/').join(nonempty_segments)
    if segments[0].startswith('/') and not url.startswith('/'):
        url = '/' + url
    if settings.APPEND_SLASH and not url.endswith('/'):
        url += '/'
    return url