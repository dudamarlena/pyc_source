# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/slow/model/model.py
# Compiled at: 2006-01-10 04:15:14
"""MixIns and Elements for XPathModel.

All MixIns require the final class to provide the attribute
DEFAULT_NAMESPACE.
"""
import re, operator
from itertools import izip
from xpathmodel import autoconstruct

class NameError(ValueError):
    __module__ = __name__

    def __init__(self, name):
        if name:
            message = 'invalid name: %s' % name
        else:
            message = 'missing name: %s' % name
        ValueError.__init__(self, message)


class NamedObject(object):
    """MixIn for name attributes and readablename sub-elements as properties."""
    __module__ = __name__
    _val_name = '[a-z][_a-z0-9]*$'
    _attr_name = './@name'
    _get_readable_name = 'string(./{%(DEFAULT_NAMESPACE)s}readablename/text())'

    @autoconstruct
    def _set_readable_name(self, _xpath_result, name):
        """./{%(DEFAULT_NAMESPACE)s}readablename"""
        _xpath_result[0].text = name