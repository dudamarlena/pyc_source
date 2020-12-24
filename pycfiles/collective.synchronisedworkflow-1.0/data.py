# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/synchro/data.py
# Compiled at: 2008-12-16 18:21:21
__doc__ = '\ncontent to be dispatched\n'
from zope.interface import implements
from zope.interface import Interface
from zope.component import queryAdapter
from zope.component import queryMultiAdapter
from zope.component import adapts
from interfaces import IPluginData
from interfaces import IFssPluginData
from interfaces import IZexpPluginData
from interfaces import ILinguaPluginData
from interfaces import IDeletePluginData
from interfaces import IPluginImporter
from interfaces import IPluginExporter
from interfaces import IDeleteImporter
from interfaces import ISynchroData
from interfaces import IFssImporter
from interfaces import IZexpImporter
from interfaces import IImportContext
from Products.CMFCore.utils import getToolByName
try:
    from plone.locking.interfaces import ILockable
    from plone.locking.interfaces import INonStealableLock
except:
    from interfaces.bbb import ILockable
    from interfaces.bbb import INonStealableLock

from events import SynchroModifiedEvent as ModifiedEvent
import config

def _indexObject(toindex):
    if toindex and hasattr(toindex, 'indexObject'):
        toindex.indexObject()
    if toindex and hasattr(toindex, 'isPrincipiaFolderish'):
        for obj in toindex.objectValues():
            _indexObject(obj)


class PluginData(object):
    __module__ = __name__
    implements(IPluginData)

    def __init__(self, data=None):
        self.data = data

    def getData(self):
        return self.data

    def __len__(self):
        return len(self.data)


class FssPluginData(PluginData):
    """
    file system storage content
    """
    __module__ = __name__
    implements(IFssPluginData)

    def __init__(self, data=[]):
        self.data = data


class ZexpPluginData(PluginData):
    """
    zexp pluggin content
    """
    __module__ = __name__
    implements(IZexpPluginData)


class DeletePluginData(PluginData):
    """
    delete plugin data
    """
    __module__ = __name__
    implements(IDeletePluginData)


class SynchroData(object):
    """
    contains all data to dispach in a remote site
    """
    __module__ = __name__
    implements(ISynchroData)

    def __init__(self, context, event=ModifiedEvent()):
        """
        export data from context
        """
        tool = getToolByName(context, config.TOOLNAME)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        self.datas = []
        for plugin_klass in tool.getPlugins(event):
            plugin = plugin_klass(context)
            data = plugin.exportData()
            if not IPluginData.providedBy(data):
                raise SynchroError('Must be an IPlugginData')
            if len(data):
                self.datas.append(data)

        portal_path = portal.getPhysicalPath()
        self.path = context.getPhysicalPath()[len(portal_path):]
        if hasattr(context.aq_base, 'UID'):
            self.uid = context.UID()
        else:
            self.uid = ''

    def __len__(self):
        """ return the number of data plugin """
        return len(self.datas)

    def getId(self):
        """ return id of exported context """
        return self.path[(-1)]

    def getImportPath(self):
        """ return the container path of object """
        return ('/').join(self.path[:-1])

    def getUid(self):
        """ return uid of the exported object """
        return self.uid

    def __call__(self, context):
        """
        import data in context
        """
        for data in self.datas:
            p = None
            try:
                p = IPluginImporter(data)
            except:
                raise SynchroError('can get the importer for data %s' % str(data))

            config.logger.info('call plugin importer %s' % str(p))
            importContext = queryMultiAdapter((context, self, p), IImportContext, default=None)
            if p is not None and importContext is not None:
                p.importData(importContext())

        object = context.restrictedTraverse(('/').join(self.path), None)
        if object:
            _indexObject(object)
        return


class SynchroError(Exception):
    __module__ = __name__


class ZexpImportContext(object):
    __module__ = __name__
    implements(IImportContext)
    adapts(Interface, ISynchroData, IZexpImporter)

    def __init__(self, context, data, importer):
        """ constructor
        @param context: context object
               data :  ISynchroData object
               importer : IZexpImporter plugin """
        self.context = context
        self.data = data
        self.importer = importer

    def __call__(self):
        """ return import context for zexp """
        context = self.context
        import_path = None
        try:
            import_path = self.data.getImportPath()
        except:
            config.logger.exception('can get synchro path fo data')
            raise SynchroError("can't get synchro path")

        container = context.unrestrictedTraverse(import_path, None)
        if container is None:
            config.logger.exception('can get synchro path %s' % import_path)
            raise SynchroError('Import path is not available')
        if self.data.getId() in container.objectIds():
            to_delete = container[self.data.getId()]
            config.logger.info('delete %s in %s' % (self.data.getId(), ('/').join(container.getPhysicalPath())))
            lockable = queryAdapter(to_delete, ILockable, default=None)
            if lockable and lockable.locked():
                noLongerProvides(to_delete, INonStealableLock)
                lockable.clear_locks()
            container.manage_delObjects([self.data.getId()])
        return container


class DeleteImportContext(object):
    __module__ = __name__
    implements(IImportContext)
    adapts(Interface, ISynchroData, IDeleteImporter)

    def __init__(self, context, data, importer):
        """ constructor
        @param context: context object
               data :  ISynchroData object
               importer : IZexpImporter plugin """
        self.context = context
        self.data = data
        self.importer = importer

    def __call__(self):
        """ return import context for zexp """
        return self.context.unrestrictedTraverse(self.data.getImportPath(), None)


class FssImportContext(object):
    __module__ = __name__
    implements(IImportContext)
    adapts(Interface, ISynchroData, IFssImporter)

    def __init__(self, context, data, importer):
        """ constructor
        @param context: context object
               data :  ISynchroData object
               importer : IZexpImporter plugin """
        self.context = context
        self.data = data
        self.importer = importer

    def __call__(self):
        """ return import context for zexp """
        return self.context.restrictedTraverse(self.data.getImportPath(), None)


class DefaultImportContext(object):
    __module__ = __name__
    implements(IImportContext)
    adapts(Interface, ISynchroData, IPluginImporter)

    def __init__(self, context, data, importer):
        """ constructor
        @param context: context object
               data :  ISynchroData object
               importer : IZexpImporter plugin """
        self.context = context
        self.data = data
        self.importer = importer

    def __call__(self):
        """ return import context for zexp """
        return self.context.restrictedTraverse(('/').join(self.data.path))