# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/ZScheduler/Log.py
# Compiled at: 2015-07-18 19:40:58
import AccessControl, string
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2
from Products.ZCatalog.ZCatalog import ZCatalog
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from AccessControl import ClassSecurityInfo
from AccessControl.Permissions import view_management_screens, access_contents_information, delete_objects
from Acquisition import aq_base
from DateTime import DateTime

class LogRec(PropertyManager, SimpleItem):
    """
    A simple log record class
    """
    meta_type = 'Log Record'
    property_extensible_schema__ = 0
    icon = 'misc_/ZScheduler/logrec'
    _properties = ({'id': 'timestamp', 'type': 'date', 'mode': 'r'}, {'id': 'process', 'type': 'string', 'mode': 'r'}, {'id': 'url', 'type': 'string', 'mode': 'r'}, {'id': 'title', 'type': 'string', 'mode': 'r'}, {'id': 'message', 'type': 'text', 'mode': 'r'})
    manage_options = PropertyManager.manage_options + SimpleItem.manage_options

    def __init__(self, id, title, timestamp, process, url, message):
        self.id = id
        self.title = title
        self.timestamp = timestamp
        self.url = url
        self.process = process
        self.message = message

    def event(self):
        """
        return underlying event or None if it no longer exists ...
        """
        try:
            return self.getPhysicalRoot().unrestrictedTraverse(self.url).event()
        except:
            return

        return

    def manage_afterAdd(self, item, container):
        self.aq_parent.catalog_object(self, ('/').join(self.getPhysicalPath()))

    def manage_beforeDelete(self, item, container):
        self.aq_parent.uncatalog_object(('/').join(self.getPhysicalPath()))


AccessControl.class_init.InitializeClass(LogRec)

class Logger(BTreeFolder2, ZCatalog):
    """
    A simple searcheable log message container

    We haven't yet bothered to implement a search API
    """
    meta_type = 'Logger'
    icon = 'misc_/ZScheduler/logger'
    id = '_logger'

    def __init__(self, id='_logger', title='ZSchedule Log'):
        BTreeFolder2.__init__(self, self.id)
        ZCatalog.__init__(self, self.id)
        self.title = title
        self.addIndex('timestamp', 'DateIndex')

    def all_meta_types(self):
        return []

    def log(self, timestamp, pid, url, title, msg):
        id = self.generateId()
        self._setObject(id, LogRec(id, title, timestamp, pid, url, msg))

    __call__ = ZCatalog.__call__


AccessControl.class_init.InitializeClass(Logger)

class LogSupport(SimpleItem):
    """
    ZMI support for logging
    """
    _security = ClassSecurityInfo()
    __ac_permissions__ = (
     (
      delete_objects, ('manage_clearLog', 'manage_delLogEntries')),
     (
      view_management_screens, ('manage_log', )),
     (
      access_contents_information, ('logger', ))) + SimpleItem.__ac_permissions__
    _properties = ({'id': 'log_batch_size', 'type': 'int', 'mode': 'w'},)
    manage_options = ({'label': 'Log', 'action': 'manage_log', 'help': ('ZScheduler', 'log.stx')},) + SimpleItem.manage_options
    manage_log = PageTemplateFile('zpt/log', globals())

    def __init__(self):
        self._logger = Logger()
        self.log_batch_size = 15

    _security.declarePrivate('log')

    def log(self, event, title, msg=''):
        """
        helper log method
        """
        if getattr(aq_base(self), '_logger', None) is not None:
            self._logger.log(DateTime(), event.getId(), '/%s' % event.absolute_url(1), title, msg)
        return

    def logger(self):
        """ query the log """
        results = []
        query = {'sort_on': 'timestamp', 'sort_order': 'descending'}
        for brain in self._logger.searchResults(**query):
            id = brain.getPath().split('/')[(-1)]
            results.append(self._logger._getOb(id))

        return results

    def loggerValues(self):
        """
        """
        return self._logger.objectValues()

    def manage_clearLog(self, REQUEST=None):
        """
        remove all log entries
        """
        while self._logger.objectIds():
            map(lambda x, y=self._logger: y._delObject(x), self._logger.objectIds())

        if REQUEST:
            REQUEST.set('manage_tabs_message', 'Log cleared')
            REQUEST.set('management_view', 'Log')
            return self.manage_log(self, REQUEST)

    def manage_delLogEntries(self, ids, REQUEST=None):
        """
        remove selected log entries
        """
        self._logger.manage_delObjects(ids)
        if REQUEST:
            REQUEST.set('management_view', 'Log')
            return self.manage_log(self, REQUEST)

    def manage_repair(self, REQUEST=None):
        """
        fix catalog(s)
        """
        if getattr(aq_base(self), '_logger', None):
            self._logger = Logger()
        if REQUEST:
            REQUEST.set('manage_tabs_message', 'Repaired')
            return self.manage_main(self, REQUEST)
        else:
            return


AccessControl.class_init.InitializeClass(LogSupport)