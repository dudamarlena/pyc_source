# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/geoportal/schema.py
# Compiled at: 2012-07-04 13:01:37
from zope.schema.interfaces import ITuple
from zope.interface import implements
from zope.schema import Tuple
from ztfy.utils.schema import DottedDecimalField

class ILocationField(ITuple):
    """Location (longitude/latitude) field interface"""
    pass


class LocationField(Tuple):
    """Longitude/latitude location field"""
    implements(ILocationField)

    def __init__(self, value_type=None, unique=False, **kw):
        super(LocationField, self).__init__(min_length=2, max_length=2, value_type=DottedDecimalField(), unique=False, **kw)