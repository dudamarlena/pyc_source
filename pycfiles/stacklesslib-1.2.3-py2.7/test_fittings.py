# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\stacklesslib\test\test_fittings.py
# Compiled at: 2017-12-11 20:12:50
import unittest, logging, stackless, stacklesslib.fittings, stacklesslib.app, stacklesslib.errors
from stacklesslib.util import QueueChannel
from .support import timesafe
DELAY = 0.001
HALF_DELAY = DELAY / 2

def call_back(callback, args=(), kwds={}):

    def helper():
        return callback(*args, **kwds)

    stacklesslib.app.event_queue.call_later(DELAY, helper)


class AsyncAPI(object):

    def call_ok(self, a, b, c, kw=None, on_success=None, on_failure=None):
        if on_success:
            call_back(on_success, (a, b, c), {'kw': kw})

    def call_fail(self, a, b, c, kw=None, on_success=None, on_failure=None):
        if on_failure:
            call_back(on_failure, (a, b, c), {'kw': kw})

    def call_immediate(self, a, b, c, kw=None, on_success=None, on_failure=None):
        if on_success:
            on_success(a, b, c, kw=kw)


class TestCallBack(unittest.TestCase):
    """Tests for the helper function"""

    @timesafe()
    def test_call_back(self):
        c = stackless.channel()

        def meh(*args):
            c.send(args)

        call_back(meh, (1, 2, 3))
        r = c.receive()
        self.assertEqual(r, (1, 2, 3))


class TestAsyncAPI(unittest.TestCase):
    """Tests for the test class """

    def setUp(self):
        self.api = AsyncAPI()
        self.c = stackless.channel()

    @timesafe()
    def test_call_ok(self):
        c = stackless.channel()

        def meh(*args, **kwds):
            self.c.send((args, kwds))

        self.api.call_ok(1, 2, 3, on_success=meh)
        r = self.c.receive()
        self.assertEqual(r, ((1, 2, 3), {'kw': None}))
        self.api.call_ok(1, 2, 3, 4, on_success=meh)
        r = self.c.receive()
        self.assertEqual(r, ((1, 2, 3), {'kw': 4}))
        return

    @timesafe()
    def test_call_fail(self):

        def meh(*args, **kwds):
            self.c.send((args, kwds))

        self.api.call_fail(1, 2, 3, on_failure=meh)
        r = self.c.receive()
        self.assertEqual(r, ((1, 2, 3), {'kw': None}))
        self.api.call_fail(1, 2, 3, 4, on_failure=meh)
        r = self.c.receive()
        self.assertEqual(r, ((1, 2, 3), {'kw': 4}))
        return

    @timesafe()
    def test_call_immediate(self):
        c = [None]

        def meh(*args, **kwds):
            c[0] = (args, kwds)

        self.api.call_immediate(1, 2, 3, on_success=meh)
        r = c[0]
        self.assertEqual(r, ((1, 2, 3), {'kw': None}))
        self.api.call_immediate(1, 2, 3, 4, on_success=meh)
        r = c[0]
        self.assertEqual(r, ((1, 2, 3), {'kw': 4}))
        return


class TestSyncToAsync(unittest.TestCase):

    def setUp(self):
        self.a = AsyncAPI()

    def testCreaeteInstance(self):
        i = stacklesslib.fittings.SyncToAsync()

    def test_default_not_implemented(self):
        i = stacklesslib.fittings.SyncToAsync()
        self.assertRaises(NotImplementedError, i)

    @timesafe()
    def test_simple_api(self):
        i = stacklesslib.fittings.SyncToAsync()

        def initiate_call(args, kwds):
            self.a.call_ok(on_success=i.on_success_vakw, *args, **kwds)

        i.initiate_call = initiate_call
        r = i(1, 2, 3)
        self.assertEqual(r, ((1, 2, 3), {'kw': None}))
        return

    @timesafe()
    def test_simple_api_fail(self):
        i = stacklesslib.fittings.SyncToAsync()

        def initiate_call(args, kwds):
            self.a.call_fail(on_failure=i.on_failure_vakw, *args, **kwds)

        i.initiate_call = initiate_call
        self.assertRaises(stacklesslib.fittings.AsyncCallFailed, i, 1, 2, 3)

    @timesafe()
    def test_simple_api_immediate(self):
        i = stacklesslib.fittings.SyncToAsync()

        def initiate_call(args, kwds):
            self.a.call_immediate(on_success=i.on_success_vakw, *args, **kwds)

        i.initiate_call = initiate_call
        r = i(1, 2, 3)
        self.assertEqual(r, ((1, 2, 3), {'kw': None}))
        return

    @timesafe()
    def test_simple_api_inherited(self):

        class STA(stacklesslib.fittings.SyncToAsync):

            def initiate_call(self, args, kwds):
                self.api.call_ok(on_success=i.on_success_vakw, *args, **kwds)

        i = STA()
        i.api = self.a
        r = i(1, 2, 3)
        self.assertEqual(r, ((1, 2, 3), {'kw': None}))
        return

    @timesafe()
    def test_simple_api_cancel(self):
        i = stacklesslib.fittings.SyncToAsync()

        def initiate_call(args, kwds):
            self.a.call_ok(on_success=i.on_success_vakw, *args, **kwds)

            def cancel():
                i.cancel('dude')

            stacklesslib.app.event_queue.call_later(HALF_DELAY, cancel)

        v = [False]

        def abandoned(value):
            v[0] = value

        i.initiate_call = initiate_call
        i.abandoned_success = abandoned
        self.assertRaises(stacklesslib.errors.CancelledError, i, 1, 2, 3)
        stacklesslib.app.sleep(HALF_DELAY)
        self.assertNotEqual(v[0], False)

    @timesafe()
    def test_simple_api_abandoned(self):
        i = stacklesslib.fittings.SyncToAsync()

        def initiate_call(args, kwds):
            self.a.call_ok(on_success=i.on_success_vakw, *args, **kwds)

            def cancel():
                i.cancel('dude')

            stacklesslib.app.event_queue.call_later(HALF_DELAY, cancel)

        v = [False]

        def abandoned(value):
            v[0] = value

        i.initiate_call = initiate_call
        i.abandoned_success = abandoned
        self.assertRaises(stacklesslib.errors.CancelledError, i, 1, 2, 3)
        stacklesslib.app.sleep(HALF_DELAY)
        self.assertEqual(v[0], ((1, 2, 3), {'kw': None}))
        return

    @timesafe()
    def test_simple_api_abandoned_failure_inherit(self):
        i = stacklesslib.fittings.SyncToAsync()

        def initiate_call(args, kwds):
            self.a.call_fail(on_failure=i.on_failure_vakw, *args, **kwds)

            def cancel():
                i.cancel('dude')

            stacklesslib.app.event_queue.call_later(HALF_DELAY, cancel)

        v = [None]

        def abandoned(value):
            v[0] = value

        i.initiate_call = initiate_call
        i.abandoned_success = abandoned
        self.assertRaises(stacklesslib.errors.CancelledError, i, 1, 2, 3)
        stacklesslib.app.sleep(HALF_DELAY)
        self.assertEqual(v[0], ((1, 2, 3), {'kw': None}))
        return

    @timesafe()
    def test_simple_api_abandoned_failure_explicit(self):
        i = stacklesslib.fittings.SyncToAsync()

        def initiate_call(args, kwds):
            self.a.call_fail(on_failure=i.on_failure_vakw, *args, **kwds)

            def cancel():
                i.cancel('dude')

            stacklesslib.app.event_queue.call_later(HALF_DELAY, cancel)

        v = [None]

        def abandoned(value):
            v[0] = value

        i.initiate_call = initiate_call
        i.abandoned_success = self.fail
        i.abandoned_failure = abandoned
        self.assertRaises(stacklesslib.errors.CancelledError, i, 1, 2, 3)
        stacklesslib.app.sleep(HALF_DELAY)
        self.assertEqual(v[0], ((1, 2, 3), {'kw': None}))
        return


class SyncAPI(object):

    def call_ok(self, a, b, c, kw=None):
        stacklesslib.app.sleep(DELAY)
        return ((a, b, c), {'kw': kw})

    def call_fail(self, a, b, c, kw=None):
        stacklesslib.app.sleep(DELAY)
        raise ZeroDivisionError(((a, b, c), {'kw': kw}))

    def call_immediate(self, a, b, c, kw=None):
        stacklesslib.app.sleep(DELAY)
        return ((a, b, c), {'kw': kw})


class TestAsyncToSync(unittest.TestCase):

    def test_create(self):
        a = SyncAPI()
        c = stacklesslib.fittings.AsyncToSync(a.call_ok)

    @timesafe()
    def test_call(self):
        a = SyncAPI()
        c2 = stacklesslib.fittings.SyncToAsync()
        c = stacklesslib.fittings.AsyncToSync(a.call_ok, c2.on_success, c2.on_failure)
        c2.initiate_call = c.initiate_call
        r = c2(2, 3, 4)
        self.assertEqual(r, ((2, 3, 4), {'kw': None}))
        return

    def test_call_immediate(self):
        a = SyncAPI()
        c2 = stacklesslib.fittings.SyncToAsync()
        c = stacklesslib.fittings.AsyncToSync(a.call_immediate, c2.on_success, c2.on_failure)
        c2.initiate_call = c.initiate_call
        r = c2(2, 3, 4)
        self.assertEqual(r, ((2, 3, 4), {'kw': None}))
        return

    @timesafe()
    def test_call_fail(self):
        a = SyncAPI()
        c2 = stacklesslib.fittings.SyncToAsync()
        c = stacklesslib.fittings.AsyncToSync(a.call_fail, c2.on_success, c2.on_failure)
        c2.initiate_call = c.initiate_call
        try:
            r = c2(2, 3, 4)
        except stacklesslib.errors.AsyncCallFailed as e:
            i = e.args[1]
            self.assertTrue(isinstance(i, ZeroDivisionError))
            self.assertEqual(i.args[0], ((2, 3, 4), {'kw': None}))
        else:
            self.fail('exception not raised')

        return

    @timesafe()
    def test_call_dispatcher(self):
        a = SyncAPI()
        c2 = stacklesslib.fittings.SyncToAsync()
        c = stacklesslib.fittings.AsyncToSync(a.call_immediate, c2.on_success, c2.on_failure, dispatcher=stacklesslib.util.tasklet_run)
        c2.initiate_call = c.initiate_call
        r = c2(2, 3, 4)
        self.assertEqual(r, ((2, 3, 4), {'kw': None}))
        return

    @timesafe()
    def test_call_dispatcher2(self):
        a = SyncAPI()
        c2 = stacklesslib.fittings.SyncToAsync()
        c = stacklesslib.fittings.AsyncToSync(a.call_immediate, c2.on_success, c2.on_failure, dispatcher=stacklesslib.util.tasklet_new)
        c2.initiate_call = c.initiate_call
        r = c2(2, 3, 4)
        self.assertEqual(r, ((2, 3, 4), {'kw': None}))
        return


from .support import load_tests
if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    unittest.main()