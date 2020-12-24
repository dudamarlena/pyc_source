# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/slideshowfolder/slideshowsetting.py
# Compiled at: 2008-06-02 02:45:55
"""
module: slideshowfolder
created by: Johnpaul Burbank <jpburbank@tegus.ca>
Date: July 8, 2007
"""
from zope.interface import implements
from persistent.dict import PersistentDict
try:
    from zope.annotation.interfaces import IAnnotations
except ImportError:
    from zope.app.annotation.interfaces import IAnnotations

from AccessControl import ClassSecurityInfo
from Products.CMFCore import permissions
from interfaces import ISlideShowSettings
from config import PROJ

class SlideShowSettings(object):
    """Implementation of ISlideShowSettings. Provides properties from the schema of the interface."""
    __module__ = __name__
    implements(ISlideShowSettings)

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        self._metadata = annotations.get(PROJ, None)
        if self._metadata is None:
            self._metadata = PersistentDict()
            annotations[PROJ] = self._metadata
        return

    def __getattr__(self, name):
        return self._metadata.get(name, ISlideShowSettings[name].default)

    def __setattr__(self, name, value):
        if name[0] == '_' or name == 'context':
            self.__dict__[name] = value
        else:
            self._metadata[name] = value