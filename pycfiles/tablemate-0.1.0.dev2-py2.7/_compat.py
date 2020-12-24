# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tablemate/_compat.py
# Compiled at: 2015-04-12 20:22:55
"""
    tablemate._compat

    Some py2/py3 compatibility support based on a stripped down
    version of six so there is no dependency on a specific version
    of it.

    Copied from Jinja2 (2015-03-22, #9bf5fcb). See also

        http://lucumr.pocoo.org/2013/5/21/porting-to-python-3-redux/

    :copyright: Copyright (c) 2013 by the Jinja team, see their AUTHORS.
    :license: BSD, see the module's source for details.
"""
import sys
PY2 = sys.version_info[0] == 2
PYPY = hasattr(sys, 'pypy_translation_info')
_identity = lambda x: x
if not PY2:
    unichr = chr
    range_type = range
    text_type = str
    string_types = (str,)
    integer_types = (int,)
    iterkeys = lambda d: iter(d.keys())
    itervalues = lambda d: iter(d.values())
    iteritems = lambda d: iter(d.items())
    import pickle
    from io import BytesIO, StringIO
    NativeStringIO = StringIO

    def reraise(tp, value, tb=None):
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value


    ifilter = filter
    imap = map
    izip = zip
    intern = sys.intern
    implements_iterator = _identity
    implements_to_string = _identity
    encode_filename = _identity
    get_next = lambda x: x.__next__
else:
    unichr = unichr
    text_type = unicode
    range_type = xrange
    string_types = (str, unicode)
    integer_types = (int, long)
    iterkeys = lambda d: d.iterkeys()
    itervalues = lambda d: d.itervalues()
    iteritems = lambda d: d.iteritems()
    import cPickle as pickle
    from cStringIO import StringIO as BytesIO, StringIO
    NativeStringIO = BytesIO
    exec 'def reraise(tp, value, tb=None):\n raise tp, value, tb'
    from itertools import imap, izip, ifilter
    intern = intern

    def implements_iterator(cls):
        cls.next = cls.__next__
        del cls.__next__
        return cls


    def implements_to_string(cls):
        cls.__unicode__ = cls.__str__
        cls.__str__ = lambda x: x.__unicode__().encode('utf-8')
        return cls


    get_next = lambda x: x.next

    def encode_filename(filename):
        if isinstance(filename, unicode):
            return filename.encode('utf-8')
        return filename


def with_metaclass(meta, *bases):

    class metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__

        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            else:
                return meta(name, bases, d)

    return metaclass('temporary_class', None, {})


try:
    from urllib.parse import quote_from_bytes as url_quote
except ImportError:
    from urllib import quote as url_quote