# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/khan/tests/test_notification.py
# Compiled at: 2010-05-12 10:25:54
from khan.utils.testing import *
from khan.notification import *
from khan.json import *

class E1(Exception):
    pass


class E2(Exception):
    pass


class E3(Exception):
    pass


class TestNotification(TestCase):

    def test_event(self):

        def subscriber1(ntf):
            raise E1

        def subscriber2(ntf):
            raise E2

        s1 = CallableSubscriber(subscriber1)
        s2 = CallableSubscriber(subscriber2)
        subscribe(s1, 'ev1')
        subscribe(s2, 'ev2')
        cb = lambda : try_notify('ev2')
        self.failUnlessRaises(E2, cb)
        unsubscribe(s1, 'ev1')
        unsubscribe(s2, 'ev2')

    def test_allevent(self):

        def allevent_subscriber(ntf):
            raise E1

        s1 = CallableSubscriber(allevent_subscriber)
        subscribe(s1)
        cb = lambda : try_notify('allevent')
        self.failUnlessRaises(E1, cb)
        unsubscribe(s1)

    def test_specitified_sender(self):

        def subscriber1(ntf):
            raise E1

        def subscriber2(ntf):
            raise E2

        s1 = CallableSubscriber(subscriber1)
        s2 = CallableSubscriber(subscriber2)
        subscribe(s1, 'specitified_sender', 'subscriber1')
        subscribe(s2, 'specitified_sender', 'subscriber2')
        cb1 = lambda : try_notify('specitified_sender', sender='subscriber1')
        cb2 = lambda : try_notify('specitified_sender', sender='subscriber2')
        self.failUnlessRaises(E1, cb1)
        self.failUnlessRaises(E2, cb2)
        unsubscribe(s1, 'specitified_sender', 'subscriber1')
        unsubscribe(s2, 'specitified_sender', 'subscriber2')

    def test_any_sender(self):

        def subscriber1(ntf):
            raise E1

        s1 = CallableSubscriber(subscriber1)
        subscribe(s1, 'specitified_sender', AnySender)
        cb = lambda : try_notify('specitified_sender', sender='subscriber2')
        self.failUnlessRaises(E1, cb)
        unsubscribe(s1, 'specitified_sender', AnySender)

    def test_anonymous_sender(self):

        def subscriber1(ntf):
            raise E1

        def subscriber2(ntf):
            raise E2

        s1 = CallableSubscriber(subscriber1)
        s2 = CallableSubscriber(subscriber2)
        subscribe(s1, 'specitified_sender', 'subscriber1')
        subscribe(s2, 'specitified_sender', AnonymousSender)
        cb = lambda : try_notify('specitified_sender')
        self.failUnlessRaises(E2, cb)
        cb = lambda : try_notify('specitified_sender', sender=None)
        self.failUnlessRaises(E2, cb)
        unsubscribe(s1, 'specitified_sender', 'subscriber1')
        unsubscribe(s2, 'specitified_sender', AnonymousSender)


class TestHTTPBasedEventAgent(TestCase):

    def test_httpbasedeventagent(self):
        u"""
        TODO:: 要测试 HTTPBasedEventAgent 是否真正调用了 subscriber
        """
        app = HTTPBasedEventAgent()
        app = TestApp(app)
        resp = app.post('/', 'sdaddadsa', status='*')
        self.failUnlessEqual(resp.status_int, 200)
        resp = app.post('/', JSONRPCBuilder.request('notify', ['UserCreated', {'created_raise': True}]), status='*', extra_environ={'REMOTE_ADDR': '127.0.0.1'})
        self.failUnlessEqual(resp.status_int, 200)


if __name__ == '__main__':
    unittest.main()