# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/ZScheduler/tool.py
# Compiled at: 2015-07-18 19:40:58
import AccessControl
from AccessControl.Permissions import change_configuration
from Products.ZScheduler.config import TOOLNAME
from Products.ZScheduler.interfaces import ISchedulerTool
from OFS.SimpleItem import SimpleItem
from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFCore.utils import registerToolInterface, UniqueObject
from zope.interface import implements

class SchedulerTool(UniqueObject, ActionProviderBase, SimpleItem):
    """
    A tool to manage scheduled events in your portal
    """
    meta_type = portal_type = 'SchedulerTool'
    implements(ISchedulerTool)
    id = TOOLNAME
    title = 'Scheduled Events Tool'
    _actions = ()
    __ac_permissions__ = SimpleItem.__ac_permissions__ + ((change_configuration, ('queueValues', 'timezone', 'schedule', 'unschedule')),) + ActionProviderBase.__ac_permissions__
    manage_options = ActionProviderBase.manage_options + SimpleItem.manage_options

    def __init__(self, id=TOOLNAME):
        pass

    def queueValues(self):
        """
        """
        tool = self.getPhysicalRoot().ZSchedulerTool
        query = {'getPhysicalPath': ('/').join(self.aq_parent.getPhysicalPath())}
        return map(lambda x: x.getObject(), tool.searchResults(**query))

    def timezone(self):
        """
        """
        tool = self.getPhysicalRoot().ZSchedulerTool
        return tool.timezone

    def schedule(self, urls):
        """
        start scheduling the indicated urls
        """
        my_url = ('/').join(self.aq_parent.getPhysicalPath())
        tool = self.getPhysicalRoot().ZSchedulerTool
        tool.manage_schedule(filter(lambda x: x.startswith(my_url), urls))

    def unschedule(self, urls):
        """
        stop scheduling the indicated urls
        """
        my_url = ('/').join(self.aq_parent.getPhysicalPath())
        tool = self.getPhysicalRoot().ZSchedulerTool
        tool.manage_unschedule(filter(lambda x: x.startswith(my_url), urls))


AccessControl.class_init.InitializeClass(SchedulerTool)
registerToolInterface(TOOLNAME, ISchedulerTool)