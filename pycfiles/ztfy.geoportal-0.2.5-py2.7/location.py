# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/geoportal/location.py
# Compiled at: 2012-11-07 11:52:41
from ztfy.geoportal.interfaces import IGeoportalLocation
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

class GeoportalLocation(object):
    """Geoportal location object"""
    implements(IGeoportalLocation)
    longitude = FieldProperty(IGeoportalLocation['longitude'])
    latitude = FieldProperty(IGeoportalLocation['latitude'])