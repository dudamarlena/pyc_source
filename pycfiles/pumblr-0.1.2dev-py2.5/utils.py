# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pumblr/utils.py
# Compiled at: 2010-09-12 13:06:57
import re, string, urllib

def urlencode(query):
    """
    urlencode(remove key if value is None)
    >>> urlencode(dict(a=1, b=2, c=None))
    'a=1&b=2'
    >>> urlencode(dict(aaaa=1000, c='hoge', a=None))
    'aaaa=1000&c=hoge'
    """
    delkeys = []
    for (key, val) in query.iteritems():
        if val is None:
            delkeys.append(key)

    for key in delkeys:
        query.pop(key)

    return urllib.urlencode(query)


def extract_dict(json):
    """
    'var hoge={...}' -> '{...}'

    >>> extract_dict('var hoge = {"fuga":1}')
    '{"fuga":1}'
    """
    return re.match('^.*?({.*}).*$', json, re.DOTALL | re.MULTILINE | re.UNICODE).group(1)


def make_variable_name(name):
    """
    replace invalide character

    example:
    >>> make_variable_name('hoge-fuga-piyo')
    'hoge_fuga_piyo'
    >>> make_variable_name('Love & Peace')
    'Love___Peace'
    >>> make_variable_name('12abc23')
    'i12abc23'
    """
    if name[0] in string.digits:
        name = 'i' + name
    return re.sub('[^A-Za-z0-9_]', '_', name)


def import_json():
    """
    import json module and return the module
    >>> json = import_json()
    """
    try:
        import simplejson as json
    except ImportError:
        try:
            import json
        except ImportError:
            try:
                from django.utils import simplejson as json
            except ImportError:
                raise ImportError, "Can't load a json library"

    return json