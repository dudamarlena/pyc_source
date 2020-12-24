# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/sc/base/hotsites/interfaces.py
# Compiled at: 2009-12-29 13:58:42
from zope.interface import Interface, alsoProvides
from zope.app.content.interfaces import IContentType

class IHotSite(Interface):
    """ A section of your Plone Site that act as a Hot Site """
    __module__ = __name__


alsoProvides(IHotSite, IContentType)

class INoHotSite(Interface):
    """ A marker interface that allows subtyping reset """
    __module__ = __name__


alsoProvides(INoHotSite, IContentType)