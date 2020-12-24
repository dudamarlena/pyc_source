# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/marrow/templating/serialize/json_.py
# Compiled at: 2012-05-23 13:16:55
from __future__ import unicode_literals
try:
    from simplejson import dumps
except ImportError:
    try:
        from json import dumps
    except ImportError:
        raise ImportError(b'Your version of Python requires that you install the simplejson package for JSON support.')

__all__ = [b'render']

def render(data, template=None, content_type=b'application/json', i18n=None, **kw):
    """A basic JSON serializer templating language.
    
    Accepts the same extended arguments as the JSON dumps() function, see:
    
        http://docs.python.org/library/json.html#json.dump
    
    Data may be of any datatype supported by the json standard library or simplejson.
    
    Sample usage:
    
        >>> from alacarte.core import Engines
        >>> render = Engines()
        >>> render.json(dict(hello="world"))
        ('application/json', '{"hello": "world"}')
    
    More compact notation:
        
        >>> from alacarte.core import Engines
        >>> render = Engines()
        >>> render.json(dict(hello="world"), separators=(',', ':'))
        ('application/json', '{"hello":"world"}')
        
    """
    return (
     content_type, dumps(data, **kw))