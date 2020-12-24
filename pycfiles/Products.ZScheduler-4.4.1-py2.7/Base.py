# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/ZScheduler/timers/Base.py
# Compiled at: 2015-07-18 19:40:58
import Globals, zLOG
from AccessControl.Permissions import change_configuration
from AccessControl import SecurityManagement, User, class_init
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager
from Products.ZScheduler.interfaces.ITimer import ITimer
from threading import Thread, Event
from ZPublisher.HTTPRequest import HTTPRequest
from ZPublisher.HTTPResponse import HTTPResponse
from ZPublisher.BaseRequest import RequestContainer
worker = None

class BaseTimer(PropertyManager, SimpleItem):
    """
    Basic timer implementation (ZMI + start/stop)
    """
    __implements__ = (
     ITimer,)
    id = 'timer'
    _stop_event = Event()
    icon = 'misc_/ZScheduler/timer'
    _properties = ({'id': 'is_active', 'mode': 'w', 'type': 'boolean'},)
    manage_options = PropertyManager.manage_options + ({'label': 'Restart', 'action': 'manage_restart'},) + SimpleItem.manage_options
    manage_main = PropertyManager.manage_propertiesForm
    property_extensible_schema__ = 0
    __ac_permissions__ = PropertyManager.__ac_permissions__ + ((change_configuration, ('manage_restart', )),) + SimpleItem.__ac_permissions__

    def __init__(self):
        self.is_active = False

    def title(self):
        return self.meta_type

    def _start(self, scheduler=None):
        """
        start timer

        essentially just clears the stop semaphore causing the main loop to run
        """
        self._stop_event.clear()

    def _stop(self, scheduler=None):
        """
        stop timer

        essentially just flags the stop semaphore and the main loop should drop out
        """
        self._stop_event.set()
        scheduler = scheduler or self.aq_parent
        scheduler.semaphore.set()

    def isActive(self):
        """
        hard-core function testing underlying timer mechanism's status
        """
        return False

    def _load(self):
        """
        load underlying timer
        """
        pass

    def _unload(self):
        """
        unload underlying timer
        """
        pass

    def manage_restart(self, scheduler=None, REQUEST=None):
        """
        stop/start the timer
        """
        self._stop(scheduler or self.aq_parent)
        self._start(scheduler or self.aq_parent)
        if REQUEST:
            REQUEST.set('manage_tabs_message', 'Restarted')
            return self.manage_main(self, REQUEST)


class_init.InitializeClass(BaseTimer)

class ThreadedTimer(BaseTimer):
    """
    A timer that manages load/reload in a separate thread

    Note that Zope connections do not play well with threads - the connection
    is in another thread.  However, since we're not doing any writes/commits
    in our worker thread, this doesn't affect us.

    Refer to http://www.zopelabs.com/cookbook/1058719806 for a discussion
    about Zope Threads.
    """

    def _start(self, scheduler=None):
        """
        kick off a listener to refresh crontab's as event's change or are added
        and removed
        """
        zLOG.LOG('ZScheduler.timer.%s' % self.meta_type, zLOG.INFO, 'starting...')
        if not self.is_active:
            return
        else:
            if not getattr(self, 'REQUEST', None):
                self = self._getContext(self)
            scheduler = scheduler or self.aq_parent
            BaseTimer._start(self, scheduler)
            worker = Thread(None, self._run)
            worker.setName('ZScheduler')
            worker.setDaemon(1)
            worker.start()
            scheduler.semaphore.set()
            return

    def _run(self):
        """
        this is our reload procedure
        """
        zLOG.LOG('ZScheduler.timer.%s' % self.meta_type, zLOG.INFO, 'starting listener')
        SecurityManagement.newSecurityManager(None, User.system)
        while 1:
            if self._stop_event.isSet():
                zLOG.LOG('ZScheduler.timer.%s' % self.meta_type, zLOG.INFO, 'stopping listener')
                return
            conn = Globals.DB.open()
            app = self._getContext(conn.root()['Application'])
            scheduler = app.ZSchedulerTool
            scheduler.timer._unload()
            scheduler.timer._load()
            scheduler.semaphore.wait()
            if scheduler.semaphore.isSet():
                scheduler.semaphore.clear()
            conn.close()

        return

    def _stop(self, scheduler):
        """
        remove crontab
        """
        zLOG.LOG('ZScheduler.timer.%s' % self.meta_type, zLOG.INFO, 'stopping...')
        BaseTimer._stop(self, scheduler)
        if not self.is_active:
            return
        self._unload()

    def _getContext(self, app):
        """
        set up a Zope context
        """
        resp = HTTPResponse(stdout=None)
        from asyncore import socket_map
        http = filter(lambda x: x.__class__.__name__ == 'zhttp_server', socket_map.values())[0]
        env = {'SERVER_NAME': http.server_name, 
           'SERVER_PORT': str(http.server_port), 
           'REQUEST_METHOD': 'GET'}
        req = HTTPRequest(None, env, resp)
        return app.__of__(RequestContainer(REQUEST=req))


class_init.InitializeClass(ThreadedTimer)