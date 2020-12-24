# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/iccommunity/core/annotations.py
# Compiled at: 2008-10-06 10:31:14
from zope.interface import implements
try:
    from zope.annotation.interfaces import IAttributeAnnotatable, IAnnotations
except:
    from zope.app.annotation.interfaces import IAttributeAnnotatable, IAnnotations

from persistent.dict import PersistentDict

class KeywordBasedAnnotations(object):
    __module__ = __name__
    implements(IAttributeAnnotatable)
    _anno_key = 'icCommunityANNO'

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(self.context)
        self._metadata = annotations.get(self._anno_key, None)
        if self._metadata is None:
            self._metadata = PersistentDict()
            annotations[self._anno_key] = self._metadata
        return