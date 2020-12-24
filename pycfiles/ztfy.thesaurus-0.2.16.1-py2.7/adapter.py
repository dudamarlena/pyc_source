# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/thesaurus/extension/gps/adapter.py
# Compiled at: 2013-08-28 03:25:14
from persistent import Persistent
from zope.annotation.interfaces import IAnnotations
from ztfy.thesaurus.extension.gps.interfaces import IThesaurusTermGPSExtensionInfo, IThesaurusTermGPSExtensionTarget
from zope.component import adapter
from zope.interface import implements, implementer
from zope.schema.fieldproperty import FieldProperty

class ThesaurusTermGPSExtension(Persistent):
    """Thesaurus term GPS extension"""
    implements(IThesaurusTermGPSExtensionInfo)
    latitude = FieldProperty(IThesaurusTermGPSExtensionInfo['latitude'])
    longitude = FieldProperty(IThesaurusTermGPSExtensionInfo['longitude'])


GPS_EXTENSION_KEY = 'ztfy.thesaurus.extension.gps'

@adapter(IThesaurusTermGPSExtensionTarget)
@implementer(IThesaurusTermGPSExtensionInfo)
def ThesaurusTermGPSExtensionFactory(context):
    """Thesaurus term GPS extension factory"""
    annotations = IAnnotations(context)
    info = annotations.get(GPS_EXTENSION_KEY)
    if info is None:
        info = annotations[GPS_EXTENSION_KEY] = ThesaurusTermGPSExtension()
    return info