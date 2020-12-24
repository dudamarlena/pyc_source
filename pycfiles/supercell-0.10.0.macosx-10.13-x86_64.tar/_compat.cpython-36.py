# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jannis/Documents/code/rtr-supercell/supercell/env3/lib/python3.6/site-packages/supercell/_compat.py
# Compiled at: 2019-01-08 09:09:15
# Size of source mod 2**32: 2731 bytes
"""
Python 2.6/2.7/3.3 compatibility module.

Heavily inspired by jinja2 and
http://lucumr.pocoo.org/2013/5/21/porting-to-python-3-redux/

Also provides a schematics 1.1.1 compatibility helper.
"""
import sys
__all__ = [
 'unichr', 'range_type', 'text_type', 'string_types', 'iterkeys',
 'itervalues', 'iteritems', 'imap', 'izip', 'ifilter']
PY2 = sys.version_info[0] == 2
PYPY = hasattr(sys, 'pypy_translation_info')
_identity = lambda x: x
if not PY2:
    unichr = chr
    range_type = range
    text_type = str
    string_types = (str,)
    iterkeys = lambda d: iter(d.keys())
    itervalues = lambda d: iter(d.values())
    iteritems = lambda d: iter(d.items())
    ifilter = filter
    imap = map
    izip = zip
else:
    unichr = chr
    range_type = xrange
    text_type = unicode
    string_types = (str, unicode)
    iterkeys = lambda d: d.iterkeys()
    itervalues = lambda d: d.itervalues()
    iteritems = lambda d: d.iteritems()
    from itertools import imap, izip, ifilter

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


def error_messages(schematics_error):
    if hasattr(schematics_error, 'to_primitive'):
        return schematics_error.to_primitive()
    else:
        return schematics_error.messages