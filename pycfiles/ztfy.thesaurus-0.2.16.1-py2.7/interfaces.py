# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/thesaurus/extension/gps/interfaces.py
# Compiled at: 2012-06-04 08:15:21
from zope.interface import Interface
from ztfy.thesaurus import _
from ztfy.utils.schema import DottedDecimalField

class IThesaurusTermGPSExtensionInfo(Interface):
    """Thesaurus term GPS extension info"""
    latitude = DottedDecimalField(title=_('Latitude'), description=_('GPS latitude value, in WGS84 coordinates system'), required=True)
    longitude = DottedDecimalField(title=_('Longitude'), description=_('GPS longitude value, in WGS84 coordinates system'), required=True)


class IThesaurusTermGPSExtensionTarget(Interface):
    """Thesaurus term GPS extension marker interface"""
    pass