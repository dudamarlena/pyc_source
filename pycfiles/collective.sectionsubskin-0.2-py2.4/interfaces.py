# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/sectionsubskin/interfaces.py
# Compiled at: 2008-07-18 06:49:04
from zope.app.content import interfaces as contentifaces
from zope.interface import alsoProvides, Attribute
try:
    from zope.component.interfaces import IObjectEvent
except:
    from zope.app.event.interfaces import IObjectEvent

try:
    from p4a.subtyper.interfaces import IPortalTypedFolderishDescriptor
except:
    from zope.interface import Interface as IPortalTypedFolderishDescriptor

class ISubskinDefinition(IPortalTypedFolderishDescriptor):
    """Defines one of the possible subskins."""
    __module__ = __name__


class ITraverseThroughEvent(IObjectEvent):
    """An event which gets sent when traversal passes through an object"""
    __module__ = __name__


alsoProvides(ISubskinDefinition, contentifaces.IContentType)