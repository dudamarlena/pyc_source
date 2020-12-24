# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/contentsync/browser/utilities.py
# Compiled at: 2009-05-11 14:25:19
from zope.interface import implements, alsoProvides
from zope.event import notify
from Acquisition import aq_inner, aq_base
from Products.CMFCore.utils import getToolByName
from collective.contentsync.events import SynchronizeStateChangeEvent
from interfaces import ISynchronizer, ISynchronizedObject
from time import sleep

class State:
    __module__ = __name__

    def __init__(self, source, view, step=1, total=0):
        self.source = source
        self.view = view
        self.step = step
        self.total = total
        self.initializing = True
        self.index = 0
        self.message = ''
        self.label = None
        self.done = False
        notify(SynchronizeStateChangeEvent(self))
        self.initializing = False
        return

    def edit(self, **kw):
        for (k, v) in kw.items():
            setattr(self, k, v)

        notify(SynchronizeStateChangeEvent(self))

    def log(self, message):
        self.message = message
        notify(SynchronizeStateChangeEvent(self))
        self.message = ''

    def reset(self):
        self.__init__(source=self.source, view=self.view)


class Synchronizer(object):
    """
    Provide synchronization methods
    """
    __module__ = __name__
    implements(ISynchronizer)

    def synchronize(self, source, targets, view=None):
        state = State(source=source, view=view)
        portal = getToolByName(source, 'portal_url').getPortalObject()
        source_path = ('/').join(source.getPhysicalPath())
        source_child_paths = []
        for (_, child) in source.ZopeFind(source, search_sub=1):
            source_child_paths.append(('/').join(child.getPhysicalPath()))

        source_child_paths.sort()
        state.edit(total=len(targets))
        count = 0
        sync = {}
        for target in targets:
            count += 1
            state.edit(index=count, label='Inspecting %s' % ('/').join(target.getPhysicalPath()[1:]))
            target_path = ('/').join(target.getPhysicalPath())
            sync_add_paths = []
            sync_rename_paths = []
            for source_child_path in source_child_paths:
                if source_child_path == source_path:
                    raise 'Target %s includes source %s' % (target_path, source_path)
                parent_path = ('/').join(source_child_path.split('/')[:-1])
                if parent_path in sync_add_paths:
                    continue
                source_obj = portal.unrestrictedTraverse(source_child_path)
                tpath = source_child_path.replace(source_path, '').lstrip('/')
                try:
                    target_obj = aq_base(target).unrestrictedTraverse(tpath)
                except AttributeError:
                    sync_add_paths.append(source_child_path)
                else:
                    if source_obj.title != target_obj.title:
                        sync_rename_paths.append((('/').join(target.getPhysicalPath()) + '/' + tpath, source_obj.title))

            sync_delete_paths = []
            target_child_paths = []
            for (_, child) in target.ZopeFind(target, search_sub=1):
                target_child_paths.append(('/').join(child.getPhysicalPath()))

            target_child_paths.sort()
            for target_child_path in target_child_paths:
                parent_path = ('/').join(target_child_path.split('/')[:-1])
                if parent_path in sync_delete_paths:
                    continue
                corresponding_path = source_path + '/' + target_child_path.replace(target_path, '').lstrip('/')
                if corresponding_path not in source_child_paths:
                    obj = portal.unrestrictedTraverse(target_child_path)
                    if ISynchronizedObject.isImplementedBy(obj):
                        sync_delete_paths.append(target_child_path)

            sync.setdefault(target, {})
            sync[target]['add'] = sync_add_paths
            sync[target]['delete'] = sync_delete_paths
            sync[target]['rename'] = sync_rename_paths

        state.edit(total=len(sync.keys()))
        count = 1
        for (target, di) in sync.items():
            target_path = ('/').join(target.getPhysicalPath())
            for path in di['add']:
                source_object = portal.unrestrictedTraverse(path)
                source_container = source_object.getParentNode()
                corresponding_path = ('/').join(path.replace(source_path, target_path).split('/')[:-1])
                dest = portal.unrestrictedTraverse(corresponding_path)
                cp = source_container.manage_copyObjects([source_object.getId()])
                spath = ('/').join(source_object.getPhysicalPath()[1:])
                dpath = ('/').join(dest.getPhysicalPath()[1:])
                try:
                    state.edit(label='Copy %s to %s' % (spath, dpath))
                    dest.manage_pasteObjects(cp)
                except:
                    state.log('Cannot copy %s to %s' % (spath, dpath))

                root = dest[source_object.getId()]
                alsoProvides(root, ISynchronizedObject)
                for (_, child) in source.ZopeFind(root, search_sub=1):
                    alsoProvides(child, ISynchronizedObject)

            for path in di['delete']:
                obj = portal.unrestrictedTraverse(path)
                container = obj.getParentNode()
                container.manage_delObjects([obj.getId()])

            for (path, title) in di['rename']:
                obj = portal.unrestrictedTraverse(path)
                u_obj = aq_base(obj)
                if hasattr(u_obj, 'edit'):
                    method = getattr(u_obj, 'edit')
                    if callable(method):
                        obj.edit(title=title)
                        continue
                obj.title = title

            state.edit(index=count)
            count += 1

        state.edit(done=True)