# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/inquant/contentmirror/base/manager.py
# Compiled at: 2008-05-21 10:20:02
__author__ = 'Stefan Eletzhofer <stefan.eletzhofer@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 65383 $'
__version__ = '$Revision: 65383 $'[11:-2]
from zope import component
from zope import interface
from zope.annotation.interfaces import IAnnotations, IAttributeAnnotatable
from zope.app.component.hooks import getSite
from zope.event import notify
from persistent.dict import PersistentDict
from Acquisition import aq_inner
from inquant.contentmirror.base.interfaces import IContentMirroredEvent, IContentNoLongerMirroredEvent
from inquant.contentmirror.base.interfaces import IMirrorAddedEvent, IMirrorRemovedEvent
from inquant.contentmirror.base.interfaces import IMirrorWillBeAddedEvent, IMirrorWillBeRemovedEvent
from inquant.contentmirror.base.interfaces import IMirroredContent
from inquant.contentmirror.base.interfaces import IMirrorReferenceManager
from inquant.contentmirror.base.interfaces import IMirrorUIDManager
from inquant.contentmirror.base.interfaces import IMirrorContentProvider
from inquant.contentmirror.base.interfaces import IMirroredContentManager
from inquant.contentmirror.base.utils import give_new_context, info, debug

class ContentMirrored(object):
    __module__ = __name__
    interface.implements(IContentMirroredEvent)

    def __init__(self, obj):
        self.object = obj


class ContentNoLongerMirrored(object):
    __module__ = __name__
    interface.implements(IContentNoLongerMirroredEvent)

    def __init__(self, obj):
        self.object = obj


class MirrorAdded(object):
    __module__ = __name__
    interface.implements(IMirrorAddedEvent)

    def __init__(self, obj, container):
        self.object = obj
        self.container = container


class MirrorRemoved(MirrorAdded):
    __module__ = __name__
    interface.implements(IMirrorRemovedEvent)


class MirrorWillBeAdded(MirrorAdded):
    __module__ = __name__
    interface.implements(IMirrorWillBeAddedEvent)


class MirrorWillBeRemoved(MirrorRemoved):
    __module__ = __name__
    interface.implements(IMirrorWillBeRemovedEvent)


class AnnotationUIDManager(object):
    __module__ = __name__
    KEY = 'inquant.contentmirror.uidmanager'
    interface.implements(IMirrorUIDManager)
    component.adapts(IAttributeAnnotatable)

    def __init__(self, context):
        self.context = context
        s = IAnnotations(context)
        self.storage = s.setdefault(self.KEY, PersistentDict())

    def items(self):
        return self.storage.items()

    def keys(self):
        return self.storage.keys()

    def set(self, key, uid):
        self.storage[key] = uid

    def get(self, key, default=None):
        return self.storage.get(key, default)

    def remove(self, key):
        del self.storage[key]


class DefaultReferenceManager(object):
    """ this default implementation stores information on where a content is
    mirrored on the conten itself using annotations """
    __module__ = __name__
    component.adapts(IMirroredContent)
    interface.implements(IMirrorReferenceManager)
    KEY = 'inquant.contentmirror.refmanager.mirrors'
    KEY_OPATH = 'inquant.contentmirror.refmanager.original'

    def __init__(self, context):
        self.context = aq_inner(context)

    def _make_key(self, obj, container):
        return '%s/%s' % (('/').join(container.getPhysicalPath()), obj.getId())

    @property
    def storage(self):
        s = IAnnotations(self.context)
        return s[self.KEY]

    @property
    def opath(self):
        s = IAnnotations(self.context)
        return s[self.KEY_OPATH]

    def initialize(self, original):
        s = IAnnotations(self.context)
        s[self.KEY] = PersistentDict()
        s[self.KEY_OPATH] = ('/').join(original.getPhysicalPath())

    def deinitialize(self, original):
        s = IAnnotations(self.context)
        del s[self.KEY]
        del s[self.KEY_OPATH]

    def update(self, original):
        info('update: old %s' % self.opath)
        s = IAnnotations(self.context)
        s[self.KEY_OPATH] = ('/').join(original.getPhysicalPath())
        info('update: new %s' % self.opath)

    def add(self, obj, container):
        notify(MirrorWillBeAdded(obj, container))
        key = self._make_key(obj, container)
        d = dict(container_uid=container.UID(), container_path=('/').join(container.getPhysicalPath()))
        self.storage[key] = d
        notify(MirrorAdded(obj, container))
        info('DefaultReferenceManager: added %s: %s' % (key, d))

    def remove(self, obj, container):
        notify(MirrorWillBeRemoved(obj, container))
        key = self._make_key(obj, container)
        del self.storage[key]
        debug('DefaultReferenceManager: removed %s' % key)
        notify(MirrorRemoved(obj, container))
        if not len(self.storage.keys()):
            return True
        else:
            return False

    def isMirror(self, obj, container):
        """ return True if the object given is a mirror """
        key = self._make_key(obj, container)
        return key == self.opath

    def getOriginal(self):
        site = getSite()
        return site.restrictedTraverse(self.opath)

    def items(self):
        return self.storage.items()


class DefaultMirrorManager(object):
    __module__ = __name__
    interface.implements(IMirroredContentManager)

    def addMirror(self, obj, container):
        if not IMirrorContentProvider.providedBy(container):
            interface.alsoProvides(container, IMirrorContentProvider)
        uid_manager = IMirrorUIDManager(container)
        if uid_manager.get(obj.getId()) == obj.UID():
            return
        uid_manager.set(obj.getId(), obj.UID())
        new_obj = give_new_context(obj, container)
        if not IMirroredContent.providedBy(obj):
            interface.alsoProvides(obj, IMirroredContent)
            notify(ContentMirrored(obj))
        refmgr = IMirrorReferenceManager(obj)
        refmgr.add(new_obj, container)
        info('DefaultMirrorManager: added mirror of %s to %s' % (new_obj.absolute_url(), container.absolute_url()))

    def removeMirror(self, obj, container):
        if not IMirrorContentProvider.providedBy(container):
            return False
        if not IMirroredContent.providedBy(obj):
            return False
        uid_manager = IMirrorUIDManager(container)
        if not uid_manager.get(obj.getId()):
            return False
        new_obj = give_new_context(obj, container)
        uid_manager.remove(obj.getId())
        refmgr = IMirrorReferenceManager(obj)
        if refmgr.remove(new_obj, container):
            original = refmgr.getOriginal()
            notify(ContentNoLongerMirrored(original))
            interface.noLongerProvides(original, IMirroredContent)
        if not uid_manager.keys():
            interface.noLongerProvides(container, IMirrorContentProvider)
        info('DefaultMirrorManager: removed mirror of %s in %s' % (new_obj.absolute_url(), container.absolute_url()))
        return True