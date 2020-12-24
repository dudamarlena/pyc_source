# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/file/adapter.py
# Compiled at: 2013-05-27 11:11:24
from zope.annotation.interfaces import IAnnotations
from zope.location.interfaces import ISublocations
from ztfy.file.interfaces import IFilePropertiesContainer, IFilePropertiesContainerAttributes
from zc.set import Set
from zope.component import adapts
from zope.interface import implements
FILE_PROPERTIES_ANNOTATIONS_KEY = 'ztfy.file.container.attributes'

class FilePropertiesContainerAttributesAdapter(object):
    """File properties container attributes adapter"""
    adapts(IFilePropertiesContainer)
    implements(IFilePropertiesContainerAttributes)

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context, None)
        if annotations is not None:
            attributes = annotations.get(FILE_PROPERTIES_ANNOTATIONS_KEY)
            if attributes is None:
                attributes = annotations[FILE_PROPERTIES_ANNOTATIONS_KEY] = Set()
            self.attributes = attributes
        elif not hasattr(self, 'attributes'):
            self.attributes = Set()
        return


class FilePropertiesContainerSublocationsAdapter(object):
    """File properties container sub-locations adapter"""
    adapts(IFilePropertiesContainer)
    implements(ISublocations)

    def __init__(self, context):
        self.context = context

    def sublocations(self):
        return (v for v in (getattr(self.context, attr, None) for attr in IFilePropertiesContainerAttributes(self.context).attributes) if v is not None)