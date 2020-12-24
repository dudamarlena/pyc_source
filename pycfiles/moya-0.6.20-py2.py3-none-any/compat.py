# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/compat.py
# Compiled at: 2016-12-08 16:29:22
"""
Python 2/3 compatibility layer

http://lucumr.pocoo.org/2013/5/21/porting-to-python-3-redux/

"""
import sys
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY2:
    text_type = unicode
    binary_type = str
    string_types = (basestring,)
    xrange = xrange
    unichr = unichr
    int_types = (int, long)
    py2bytes = lambda s: s.encode('utf-8')
    raw_input = raw_input
else:
    text_type = str
    binary_type = bytes
    xrange = range
    string_types = (str, bytes)
    unichr = chr
    int_types = (int,)
    py2bytes = lambda s: s
    raw_input = input
if PY2:
    iterkeys = lambda d: d.iterkeys()
    itervalues = lambda d: d.itervalues()
    iteritems = lambda d: d.iteritems()
else:
    iterkeys = lambda d: iter(d.keys())
    itervalues = lambda d: iter(d.values())
    iteritems = lambda d: iter(d.items())
if PY2:
    from urlparse import urlparse, parse_qs, urlunparse
    from urllib import urlencode, quote, unquote, quote_plus
    from itertools import izip_longest as zip_longest
    from urllib import urlopen
    import SocketServer as socketserver
else:
    from urllib.parse import urlparse, parse_qs, urlunparse
    from urllib.parse import urlencode, quote, unquote, quote_plus
    from itertools import zip_longest
    from urllib.request import urlopen
    import socketserver
if PY2:
    import cPickle as pickle
else:
    import pickle
if PY2:
    from imp import reload
else:
    try:
        from importlib import reload
    except ImportError:
        from imp import reload

if PY2:

    def implements_to_string(cls):
        cls.__unicode__ = cls.__str__
        cls.__str__ = lambda x: x.__unicode__().encode('utf-8')
        return cls


else:
    implements_to_string = lambda x: x
if PY2:

    def implements_iterator(cls):
        cls.next = cls.__next__
        del cls.__next__
        return cls


else:
    implements_iterator = lambda x: x
if PY2:

    def implements_bool(cls):
        cls.__nonzero__ = cls.__bool__
        del cls.__bool__
        return cls


else:

    def implements_bool(cls):
        return cls


if PY2:
    number_types = (
     int, long, float)
else:
    number_types = (
     int, float)
if PY2:
    next_method_name = 'next'
else:
    next_method_name = '__next__'
if PY2:
    cmp = cmp
else:

    def cmp(a, b):
        if a < b:
            return -1
        else:
            if a == b:
                return 0
            return +1


class string(object):
    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digits = '0123456789'
    punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'


def with_metaclass(meta, *bases):

    class Metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__

        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            else:
                return meta(name, bases, d)

    return Metaclass('temporary_class', None, {})