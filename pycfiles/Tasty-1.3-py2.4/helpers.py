# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tasty/helpers.py
# Compiled at: 2007-05-08 14:16:57
from types import *
from sqlobject import *
from tasty.model import User, Item, Tag
from restclient import POST
import cherrypy

def sqlobject_to_strings(d):
    if isinstance(d, SQLObject):
        if isinstance(d, User):
            return {'user': d.username}
        if isinstance(d, Item):
            return {'item': d.name}
        if isinstance(d, Tag):
            return {'tag': d.name}
        return str(d)
    if isinstance(d, DictType):
        new_dict = {}
        for k in d.keys():
            new_dict[k] = sqlobject_to_strings(d[k])

        return new_dict
    if isinstance(d, ListType) or isinstance(d, TupleType):
        return [ sqlobject_to_strings(i) for i in d ]
    return d


def xmlify(d):
    """ super simple approach to turning an arbitrary data structure into xml """
    if type(d) == DictType:
        parts = []
        for k in d.keys():
            parts.append('<%s>%s</%s>' % (k, xmlify(d[k]), k))

        return ('\n').join(parts)
    if type(d) == StringType or type(d) == UnicodeType:
        return d
    if type(d) == TupleType:
        return '<%s>%s</%s>' % (d[0], d[1], d[0])
    if type(d) == ListType:
        parts = []
        for k in d:
            parts.append(xmlify(k))

        return '<list>' + ('\n').join(parts) + '</list>'
    return str(d)


def htmlify(d):
    """ super simple approach to turning an arbitrary data structure into html

    should probably figure a way to just map it to a kid template instead...
    """
    if type(d) == StringType or type(d) == UnicodeType:
        return d
    if type(d) == ListType:
        return '<ul>' + ('\n').join([ '<li>%s</li>' % htmlify(k) for k in d ]) + '</ul>'
    if type(d) == TupleType:
        return '<span class="%s">%s</span>' % (d[0], d[1])
    if type(d) == DictType:
        parts = []
        for k in d.keys():
            parts.append('<b>%s</b>: %s' % (k, htmlify(d[k])))

        return ('\n').join(parts)
    return str(d)


def deunicodify(s):
    if type(s) == UnicodeType:
        return s.encode('utf8')
    else:
        return s


def broadcast_event(event, params={}):
    pebble_base = cherrypy.config.get('pebblebase', '')
    if pebble_base == '':
        return
    POST(pebble_base + '/event/' + event + '/trigger', params=params, async=True)