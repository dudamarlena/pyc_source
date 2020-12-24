# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-fat3/egg/alacarte/serialize/json_.py
# Compiled at: 2010-03-18 05:47:02
try:
    from json import dumps
except ImportError:
    try:
        from simplejson import dumps
    except ImportError:
        raise ImportError('Your version of Python requires that you install the simplejson package for JSON support.')

__all__ = ['render']

def render(data, template=None, content_type='application/json', **kw):
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