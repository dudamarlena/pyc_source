# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/inquant/contentmirror/base/interfaces.py
# Compiled at: 2008-04-25 09:17:19
__author__ = 'Stefan Eletzhofer <stefan.eletzhofer@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 62293 $'
__version__ = '$Revision: 62293 $'[11:-2]
from zope import interface
from zope.component.interfaces import IObjectEvent

class IMirrorContentProvider(interface.Interface):
    """ marker interface for objects providing mirror content """
    __module__ = __name__


class IMirroredContent(interface.Interface):
    """ marker interface for content which is in fact mirrored somewhere """
    __module__ = __name__


class IMirroredContentManager(interface.Interface):
    """ manager which mirrors content """
    __module__ = __name__

    def addMirror(obj, container):
        """ add a mirror object to a container """
        pass

    def removeMirror(obj, container):
        """ remove the object mirror form the container
            returns True if mirror was removed.
            returns False if object was not mirrored here.
        """
        pass


class IMirrorReferenceManager(interface.Interface):
    """ manages references of mirrors of a object """
    __module__ = __name__

    def add(obj, container):
        """ record a reference of the object to the container """
        pass

    def remove(obj, container):
        """ record the fact that 'obj' is no longer mirrored in 'container' """
        pass

    def initialize(original):
        """ set information about the original object """
        pass

    def update(original):
        """ update information about the original object """
        pass

    def deinitialize(original):
        """ content no longer mirrored, record the fact """
        pass

    def getOriginal():
        """ return the original object """
        pass

    def isMirror(obj, container):
        """ return True if obj is a mirror in container """
        pass

    def items():
        """ return a iterable of dicts { container_uid, container_path } which
            record the places this object is mirrored to. """
        pass


class IContentMirroredEvent(IObjectEvent):
    __module__ = __name__


class IContentNoLongerMirroredEvent(IObjectEvent):
    __module__ = __name__


class IMirrorWillBeAddedEvent(IObjectEvent):
    __module__ = __name__
    container = interface.Attribute('the container the mirror is added to')
    object = interface.Attribute('the object to be mirrored')


class IMirrorAddedEvent(IObjectEvent):
    __module__ = __name__
    container = interface.Attribute('the container the mirror is added to')
    object = interface.Attribute('the object to be mirrored')


class IMirrorWillBeRemovedEvent(IObjectEvent):
    __module__ = __name__
    container = interface.Attribute('the container the mirror is removed from')
    object = interface.Attribute('the mirrored object')


class IMirrorRemovedEvent(IObjectEvent):
    __module__ = __name__
    container = interface.Attribute('the container the mirror is removed from')
    object = interface.Attribute('the mirrored object')


class IMirrorContentLocator(interface.Interface):
    """ an adapter which is able to lookup and return a content
        object.
        rhe content object returned will be inserted (mirrored) at the
        adapter's context. """
    __module__ = __name__

    def locate(name):
        """ locate a content object identified by the key "name"  and
            return it """
        pass


class IMirrorUIDManager(interface.Interface):
    """
    Storage for key->UID mappings.
    """
    __module__ = __name__

    def keys(self):
        """ """
        pass

    def get(key, default=None):
        """ return the UID stored for key """
        pass

    def set(key, uid):
        """ store a uid for the given key """
        pass

    def remove(key):
        """ remove the key from the storage """
        pass