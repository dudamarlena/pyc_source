# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/sectionsubskin/definition.py
# Compiled at: 2008-07-18 06:49:04
from zope.interface import implements, alsoProvides
try:
    from p4a.subtyper import interfaces as stifaces
except:
    stifaces = None

from collective.sectionsubskin.interfaces import ISubskinDefinition

class BaseDefinition(object):
    """The base class for skin definitions."""
    __module__ = __name__
    to_implement = (
     ISubskinDefinition,)
    isSubtype = True
    if stifaces is not None and isSubtype:
        to_implement.append(stifaces.IPortalTypedFolderishDescriptor)
    for_portal_type = 'Folder'
    implements(*to_implement)

    def __init__(self, *args, **kwargs):
        alsoProvides(self, (self.type_interface,))
        super(BaseDefinition, self).__init__(*args, **kwargs)

    def __repr__(self):
        if hasattr(self, 'title'):
            return '<SectionSubSkin named %s>' % self.title
        else:
            return '<Broken SectionSubSkin described by %s>' % str(self.__dict__)