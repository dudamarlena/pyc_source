# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/slideshowfolder/slideshowsetting.py
# Compiled at: 2008-06-02 02:45:55
__doc__ = '\nmodule: slideshowfolder\ncreated by: Johnpaul Burbank <jpburbank@tegus.ca>\nDate: July 8, 2007\n'
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