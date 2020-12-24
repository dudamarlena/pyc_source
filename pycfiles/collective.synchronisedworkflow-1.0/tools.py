# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/synchro/tools.py
# Compiled at: 2008-12-16 18:21:21
from zope.interface import implements
from zope.tales.tales import CompilerError
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.PageTemplates.Expressions import getEngine
from Products.CMFCore.Expression import Expression
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.utils import UniqueObject
try:
    from Products.CMFCore.utils import registerToolInterface
except ImportError:

    def registerToolInterface(*args):
        pass


from Products.CMFPlone.PloneBaseTool import PloneBaseTool
from permissions import SynchronizeContent
from interfaces.tool import ISynchronisationTool
from interfaces import IPluginExporter
from interfaces.events import ISynchroModifiedEvent
from interfaces.events import ISynchroDeletedEvent
from events import SynchroModifiedEvent as ModifiedEvent
from data import SynchroData
from queues import Queue
from plugins import ZexpExporter
from plugins import DeleteExporter
from utils import notify_modified
from utils import notify_deleted
import config

def validate_expression(function):

    def _validate_expression(self):
        if self.expression == '':
            return ''
        try:
            getEngine().compile(self.expression)
        except CompilerError, e:
            __traceback_info__ = (
             self, self.expression)
            config.logger.exception('Please fix your expression')
            return ''
        except:
            raise

        return function(self)

    return _validate_expression


class SynchronisationTool(PloneBaseTool, UniqueObject, PropertyManager, SimpleItem):
    __module__ = __name__
    implements(ISynchronisationTool)
    security = ClassSecurityInfo()
    id = config.TOOLNAME
    meta_type = config.TOOLNAME
    toolicon = config.ICON
    security = ClassSecurityInfo()
    plone_tool = 1
    expression = ''
    queues = []
    manage_options = PropertyManager.manage_options + SimpleItem.manage_options
    _properties = PropertyManager._properties + ({'id': 'queues', 'type': 'lines', 'mode': 'w'}, {'id': 'expression', 'type': 'string', 'mode': 'w'})

    def __init__(self, id):
        self.id = config.TOOLNAME
        self.plugins = {}
        self.registerPlugin('zexp', ZexpExporter, 0)
        self.registerPlugin('del', DeleteExporter, 0, ISynchroDeletedEvent)
        if config.HAS_FSS:
            from plugins import FssExporter
            self.registerPlugin('fss', FssExporter, 10)
        self._p_changed = 1

    security.declareProtected(SynchronizeContent, 'importContent')

    def importContent(self, context):
        """ import data from file queue
            @param file:file name in queue
        """
        pass

    security.declareProtected(ManagePortal, 'addQueue')

    def addQueue(self, path):
        self.queues += (path,)

    security.declarePublic('getQueues')

    def getQueues(self):
        return [ Queue(path) for path in self.queues ]

    _queues = property(fget=getQueues)
    security.declareProtected(SynchronizeContent, 'exportContent')

    def exportContent(self, synchro_data):
        """ export data to file queue
            @param context:the context in queue
        """
        if len(synchro_data):
            for queue in self.getQueues():
                queue.put(synchro_data)

        else:
            config.logger.info('there is no data in synchro_data : no plugin available %s' % str(self.getPlugins()))

    security.declareProtected(SynchronizeContent, 'notifyModified')

    def notifyModified(self, context):
        """ notify context , for use in script """
        notify_modified(context)

    security.declareProtected(SynchronizeContent, 'notifyDeleted')

    def notifyDeleted(self, context):
        """ notify context , for use in script """
        notify_deleted(context)

    security.declarePublic('getExpression')

    @validate_expression
    def getExpression(self):
        """ return a valid expression """
        return Expression(self.expression)

    _expression = property(fget=getExpression)
    security.declareProtected(ManagePortal, 'registerPlugin')

    def registerPlugin(self, id, klass, priority, event=ISynchroModifiedEvent):
        """ register an plugin for import export data
            @param id: identifier of plugin
                   klass: class name of the plugin
                   priority : priority of the plugin
        """
        if id not in self.plugins.keys():
            if IPluginExporter.implementedBy(klass):
                self.plugins[id] = {'klass': klass, 'priority': int(priority), 'event': event}
                self._p_changed = 1
            else:
                raise AssertionError("%s doesn't implement IPluginExporter interface" % str(klass))

    security.declareProtected(ManagePortal, 'unregisterPlugin')

    def unregisterPlugin(self, id):
        """ unregister plugin
            @param id: identifier of plugin
        """
        if id not in self.plugins.keys():
            raise AssertionError('There is no pluggin with id : <%s>' % id)
        del self.plugins[id]
        self._p_changed = 1

    security.declareProtected(ManagePortal, 'getPlugins')

    def getPlugins(self, event=ModifiedEvent()):
        """return the list of plugin exporter sorted by priority
           @return : [klass,klass]
        """
        pids = self.plugins.keys()
        pids.sort(lambda x, y: cmp(self.plugins[x]['priority'], self.plugins[y]['priority']))
        return [ self.plugins[pid]['klass'] for pid in pids if self.plugins[pid]['event'].providedBy(event) ]


InitializeClass(SynchronisationTool)
registerToolInterface(config.TOOLNAME, ISynchronisationTool)