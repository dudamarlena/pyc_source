# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/geoportal/interfaces.py
# Compiled at: 2013-03-28 07:05:42
from zope.interface import Interface
from zope.schema import TextLine, Bool
from ztfy.utils.schema import DottedDecimalField
from ztfy.geoportal import _

class IGeoportalConfigurationUtility(Interface):
    """GeoPortal utility configuration interface"""
    api_key = TextLine(title=_('GeoPortal API key'), required=True)
    version = TextLine(title=_('GeoPortal version'), required=True, default='latest')
    development = Bool(title=_('Use development version ?'), required=True, default=False)


class IGeoportalLocation(Interface):
    """Geoportal location fields interface"""
    longitude = DottedDecimalField(title=_('Longitude'), description=_('Longitude field in WGS84 coordinates system'), required=False)
    latitude = DottedDecimalField(title=_('Latitude'), description=_('Latitude field in WGS84 coordinates system'), required=False)


class IGeoportalLocationEditForm(Interface):
    """Geoportal location edit form marker interface"""
    pass