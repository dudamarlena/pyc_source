# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/boduch/test/event.py
# Compiled at: 2009-08-14 17:29:28
"""This module provides a test case class for testing events called
TestEvent and a test suite which contains the event test case class."""
import unittest
from boduch.interface import IEvent
from boduch.event import EventManager, Event, publish, subscribe, unsubscribe
from boduch.handle import Handle

class TestEvent(unittest.TestCase):
    """This class is derived from the TestCase class which is part of the
    builtin unittest Python module.  There are several methods defined by
    this class each representing some area of event testing."""

    def setUp(self):
        """This method is invoked before any tests are run.  Here we create
        a test event instance which is a attribute of the TestEvent class.
        This instance is then available to the remaining methods defined in
        this class."""
        self.test_event_obj = Event()

    def test_A_interface(self):
        """Testing the Event interface"""
        self.assertTrue(IEvent.implementedBy(Event), 'IEvent not implemented by Event.')
        self.assertTrue(IEvent.providedBy(self.test_event_obj), 'IEvent not provided by Event instance.')

    def test_B_subscribe(self):
        """Testing event subscribing"""
        subscribe(Event, Handle)
        self.assertTrue(EventManager.subscriptions.has_key(Event), 'Event not in EventManager.subscriptions')
        self.assertTrue(Handle in EventManager.subscriptions[Event], 'Handle not in EventManager.subscriptions')

    def test_C_unsubscribe(self):
        """Testing event unsubscribing"""
        subscribe(Event, Handle)
        unsubscribe(Event, Handle)
        self.assertTrue(Handle not in EventManager.subscriptions[Event], 'Handle in EventManager.subscriptions')

    def test_D_publish(self):
        """Testing event publishing"""
        try:
            publish(Event)
        except NotImplementedError:
            pass
        except Exception, e:
            self.fail(str(e))


SuiteEvent = unittest.TestLoader().loadTestsFromTestCase(TestEvent)
__all__ = [
 'TestEvent', 'SuiteEvent']