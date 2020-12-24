# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/ruamel/yaml/compat.py
# Compiled at: 2017-07-27 07:36:53
from __future__ import print_function
import sys, os, types
try:
    from ruamel.ordereddict import ordereddict
except:
    try:
        from collections import OrderedDict
    except ImportError:
        from orderddict import OrderedDict

    class ordereddict(OrderedDict):
        if not hasattr(OrderedDict, 'insert'):

            def insert(self, pos, key, value):
                if pos >= len(self):
                    self[key] = value
                    return
                od = ordereddict()
                od.update(self)
                for k in od:
                    del self[k]

                for index, old_key in enumerate(od):
                    if pos == index:
                        self[key] = value
                    self[old_key] = od[old_key]


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY3:

    def utf8(s):
        return s


    def to_str(s):
        return s


    def to_unicode(s):
        return s


else:

    def utf8(s):
        return s.encode('utf-8')


    def to_str(s):
        return str(s)


    def to_unicode(s):
        return unicode(s)


if PY3:
    string_types = (
     str,)
    integer_types = (int,)
    class_types = (type,)
    text_type = str
    binary_type = bytes
    MAXSIZE = sys.maxsize
    unichr = chr
    import io
    StringIO = io.StringIO
    BytesIO = io.BytesIO
else:
    string_types = (
     basestring,)
    integer_types = (int, long)
    class_types = (type, types.ClassType)
    text_type = unicode
    binary_type = str
    unichr = unichr
    import StringIO
    StringIO = StringIO.StringIO
    import cStringIO
    BytesIO = cStringIO.StringIO
if PY3:
    builtins_module = 'builtins'
else:
    builtins_module = '__builtin__'

def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    return meta('NewBase', bases, {})


DBG_TOKEN = 1
DBG_EVENT = 2
DBG_NODE = 4
_debug = None

def dbg(val=None):
    global _debug
    if _debug is None:
        _debug = os.environ.get('YAMLDEBUG')
        if _debug is None:
            _debug = 0
        else:
            _debug = int(_debug)
    if val is None:
        return _debug
    else:
        return _debug & val


def nprint(*args, **kw):
    if dbg:
        print(*args, **kw)