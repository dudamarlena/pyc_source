# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/ZScheduler/ZQueue.py
# Compiled at: 2015-07-18 19:40:58
import AccessControl
from AccessControl import ClassSecurityInfo
from Products.ZCatalog.ZCatalog import ZCatalog
from interfaces.IQueue import IQueue
from threading import Lock
from Acquisition import aq_base
from ZScheduleEvent import ZScheduleEvent
from Exceptions import ZSchedulingException
from zope.interface import implements

class ZQueue(ZCatalog):
    """
    This is a thread-safe queue of scheduled events and we're getting loads for free as
    we've set up a Date index on it's key ...
    """
    implements(IQueue)
    meta_type = 'ZQueue'
    title = 'ZQueue'
    _lock = Lock()
    manage_options = ZCatalog.manage_options[1:]
    manage_main = ZCatalog.manage_catalogView
    _security = ClassSecurityInfo()

    def all_meta_types(self):
        """ contain nothing """
        return []

    def __init__(self, id):
        ZCatalog.__init__(self, id)
        self.addIndex('time', 'DateIndex')
        self.addIndex('getPhysicalPath', 'PathIndex')
        self.addIndex('active', 'BooleanIndex')
        for name in ('time', 'meta_type'):
            self.addColumn(name)

    def pop(self, obj):
        """
        remove obj from catalog (actually just recatalog to force status change)
        """
        url = ('/').join(obj.getPhysicalPath())
        try:
            self._lock.acquire()
            self.catalog_object(obj, url)
        finally:
            self._lock.release()

    push = pop

    def get(self, url):
        try:
            self._lock.acquire()
            return self.getobject(self.getrid(url))
        finally:
            self._lock.release()

    def delete(self, url):
        try:
            self._lock.acquire()
            self.uncatalog_object(url)
        finally:
            self._lock.release()

    def reload(self, REQUEST=None):
        """
        search ZODB for all ZScheduleEvents and place them in the queue
        """
        root = self.getPhysicalRoot()
        try:
            self._lock.acquire()
            self._reschedule(root)
        finally:
            self._lock.release()

        if REQUEST:
            return self.manage_main(self, REQUEST)

    def getNext(self):
        try:
            self._lock.acquire()
            try:
                return self()[0].getObject()
            except:
                return

        finally:
            self._lock.release()

        return

    def _reschedule(self, folder):
        """
        tail-recursive ZODB rescheduler

        this function is designed to work with (i) subclasses of ZScheduleEvent;
        (ii) folder-like object attributes that aren't necessarily included in
        the _objects member ;)
        """
        try:
            objs = folder.objectValues()
        except Exception as e:
            raise ZSchedulingException, '%s\n%s' % (folder.absolute_url(), str(e))

        for e in filter(lambda x: isinstance(x, ZScheduleEvent), objs):
            try:
                e.time = e.nextEventTime()
            except:
                raise ZSchedulingException, e

            self.catalog_object(e, ('/').join(e.getPhysicalPath()))

        for sf in filter(lambda x: getattr(aq_base(x), 'objectValues', None), objs):
            try:
                self._reschedule(sf)
            except:
                continue

    def _repair(self):
        try:
            self.addIndex('getPhysicalPath', 'PathIndex')
        except:
            pass

        try:
            self.addIndex('active', 'BooleanIndex')
        except:
            pass

        try:
            self.addColumn('meta_type')
        except:
            pass

        self.manage_reindexIndex(['time', 'getPhysicalPath', 'active'])


AccessControl.class_init.InitializeClass(ZQueue)