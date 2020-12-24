# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kc/code/kevinconway/confpy/confpy/core/compat.py
# Compiled at: 2019-08-24 22:17:43
# Size of source mod 2**32: 1561 bytes
"""Py2/Py3 compatibility helpers."""
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
try:
    import __builtin__ as builtins
except ImportError:
    import builtins

import itertools
if hasattr(builtins, 'xrange'):
    range = builtins.xrange
else:
    range = builtins.range
if not hasattr(builtins, 'unicode'):
    unicode = builtins.str
else:
    unicode = builtins.unicode
if not hasattr(builtins, 'basestring'):
    basestring = unicode
else:
    basestring = builtins.basestring
if not hasattr(builtins, 'long'):
    long = builtins.int
else:
    long = builtins.long
if hasattr(itertools, 'izip'):
    zip = itertools.izip
else:
    zip = builtins.zip

def iteritems(dictionary):
    """Replacement to account for iteritems/items switch in Py3."""
    if hasattr(dictionary, 'iteritems'):
        return dictionary.iteritems()
    return dictionary.items()


try:
    from ConfigParser import SafeConfigParser as _ConfigParser
except ImportError:
    from configparser import ConfigParser as _ConfigParser

class ConfigParser(_ConfigParser, object):
    __doc__ = 'Compatibility shim for the deprecated readfp handling.'

    def read_file(self, f):
        """Add a check for read_file and use it if it exists."""
        parent = super(ConfigParser, self)
        if hasattr(parent, 'read_file'):
            return parent.read_file(f)
        return super(ConfigParser, self).readfp(f)