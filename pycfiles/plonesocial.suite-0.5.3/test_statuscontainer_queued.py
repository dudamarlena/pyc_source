# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gyst/plonesocial.buildout/src/plonesocial.microblog/plonesocial/microblog/tests/test_statuscontainer_queued.py
# Compiled at: 2013-04-12 05:54:49
import time, Queue, unittest2 as unittest
from zope.interface import implements
from zope.interface.verify import verifyClass
from plonesocial.microblog.interfaces import IStatusContainer
from plonesocial.microblog.interfaces import IStatusUpdate
from plonesocial.microblog import statuscontainer
from plonesocial.microblog import statusupdate
from plonesocial.microblog.statuscontainer import STATUSQUEUE
import plonesocial.microblog.statuscontainer
plonesocial.microblog.statuscontainer.MAX_QUEUE_AGE = 50

class StatusContainer(statuscontainer.QueuedStatusContainer):
    """Override actual implementation with unittest features"""
    implements(IStatusContainer)

    def _check_permission(self, perm='read'):
        pass


class StatusUpdate(statusupdate.StatusUpdate):
    """Override actual implementation with unittest features"""
    implements(IStatusUpdate)

    def __init__(self, text, userid, creator=None):
        statusupdate.StatusUpdate.__init__(self, text)
        self.userid = userid
        if creator:
            self.creator = creator
        else:
            self.creator = userid

    def _init_userid(self):
        pass

    def _init_creator(self):
        pass


class TestQueueStatusContainer(unittest.TestCase):

    def setUp(self):
        self.container = StatusContainer()
        self.container._mtime = int(time.time() * 1000)

    def tearDown(self):
        try:
            self.container._v_timer.cancel()
            time.sleep(1)
        except AttributeError:
            pass

        while True:
            try:
                STATUSQUEUE.get(block=False)
            except Queue.Empty:
                break

    def test_verify_interface(self):
        self.assertTrue(verifyClass(IStatusContainer, StatusContainer))

    def test_add_queued(self):
        """Test the queueing"""
        container = self.container
        sa = StatusUpdate('test a', 'arnold')
        container.add(sa)
        values = [ x for x in container.values() ]
        self.assertEqual([], values)
        self.assertFalse(STATUSQUEUE.empty())

    def test_add_scheduled(self):
        """Test the thread scheduler"""
        container = self.container
        sa = StatusUpdate('test a', 'arnold')
        container.add(sa)
        values = [ x for x in container.values() ]
        self.assertEqual([], values)
        time.sleep(2)
        values = [ x for x in container.values() ]
        self.assertEqual([sa], values)

    def test_add_scheduled_disabled(self):
        """Test disabling of thread scheduler"""
        container = self.container
        sa = StatusUpdate('test a', 'arnold')
        container.add(sa)
        self.container._v_timer.cancel()
        values = [ x for x in container.values() ]
        self.assertEqual([], values)
        time.sleep(1)
        values = [ x for x in container.values() ]
        self.assertEqual([], values)

    def test_add_multi(self):
        container = self.container
        sa = StatusUpdate('test a', 'arnold')
        container.add(sa)
        self.container._v_timer.cancel()
        sb = StatusUpdate('test b', 'bernard')
        time.sleep(0.2)
        container.add(sb)
        values = [ x for x in container.values() ]
        self.assertEqual([sb, sa], values)