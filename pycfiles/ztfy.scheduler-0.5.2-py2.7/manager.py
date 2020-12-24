# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/scheduler/manager.py
# Compiled at: 2012-10-22 12:36:40
__docformat__ = 'restructuredtext'
import zmq
from zope.intid.interfaces import IIntIds
from ztfy.scheduler.interfaces import IScheduler, ISchedulerHandler
from zope.component import queryUtility
from zope.container.folder import Folder
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.site.site import SiteManagerContainer
from ztfy.i18n.property import I18nTextProperty
from ztfy.security.property import RolePrincipalsProperty
from ztfy.utils.property import cached_property

class SchedulerHandler(object):
    """Scheduler handler utility"""
    implements(ISchedulerHandler)


class Scheduler(Folder, SiteManagerContainer):
    """Scheduler persistent class"""
    implements(IScheduler)
    title = I18nTextProperty(IScheduler['title'])
    zmq_address = FieldProperty(IScheduler['zmq_address'])
    zeo_connection = FieldProperty(IScheduler['zeo_connection'])
    managers = RolePrincipalsProperty(IScheduler['managers'], role='ztfy.SchedulerManager')
    operators = RolePrincipalsProperty(IScheduler['operators'], role='ztfy.SchedulerOperator')

    @property
    def tasks(self):
        return list(self.values())

    @property
    def history(self):
        result = []
        [ result.extend(task.history) for task in self.tasks ]
        return result

    @cached_property
    def internal_id(self):
        intids = queryUtility(IIntIds, context=self)
        if intids is not None:
            return intids.register(self)
        else:
            return

    def getTask(self, task_id, context=None):
        intids = queryUtility(IIntIds, context=context)
        return intids.queryObject(task_id)

    def _getSocket(self):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect('tcp://' + self.zmq_address)
        return socket

    def getJobs(self):
        socket = self._getSocket()
        socket.send_json(['get_jobs', {}])
        return socket.recv_json()