# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/unit/testDispatch.py
# Compiled at: 2009-12-08 17:43:28
import unittest
from netlogger.dispatch import *
from netlogger.tests import shared

class Test:

    def __init__(self):
        self.event = None
        return

    def got_event(self, event):
        self.event = event


class TestCase(unittest.TestCase):

    def test_dispatch(self):
        d = Dispatcher()
        h1 = RegexMatchHandler({'color': '.e.'}, search=False)
        t1 = Test()
        h1.set_method(t1.got_event)
        h2 = RegexMatchHandler({'color': '.e.'}, search=True)
        t2 = Test()
        h2.set_method(t2.got_event)
        d.register(h1)
        d.register(h2)
        event = {'color': 'red'}
        d.dispatch(event)
        self.failUnless(t1.event == event)
        self.failUnless(t2.event == event)
        event = {'color': 'green'}
        d.dispatch(event)
        self.failUnless(t1.event != event)
        self.failUnless(t2.event == event)
        event = {'color': 'tan'}
        d.dispatch(event)
        self.failUnless(t1.event != event)
        self.failUnless(t2.event != event)

    def test_remove(self):
        d = Dispatcher()
        h1 = RegexMatchHandler({'color': '.e.'}, search=False)
        t1 = Test()
        h1.set_method(t1.got_event)
        id_ = d.register(h1)
        self.failUnless(d.remove(id_))
        self.failIf(d.remove(id_))
        self.failIf(d.remove(h1))
        id_ = d.register(h1)
        self.failUnless(d.remove(h1))
        self.failIf(d.remove(h1))
        self.failIf(d.remove(id_))


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()