# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/client/tests/test_event_system.py
# Compiled at: 2010-02-09 00:00:15
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
import unittest
from pyogp.lib.client.event_system import AppEventsHandler, AppEvent
from pyogp.lib.base.helpers import Wait
from pyogp.lib.base.exc import DataParsingError
import pyogp.lib.base.tests.config

class TestEvents(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_event_handler_no_timeout(self):
        mock = MockEvent(1)
        eventshandler = AppEventsHandler()
        handler = eventshandler.register('MockEvent')
        handler.subscribe(self.onEvent, mock)
        eventshandler.handle(mock)

    def test_event_handler_timeout(self):
        mock = MockEvent(1)
        eventshandler = AppEventsHandler()
        handler = eventshandler.register('MockEvent', 2)
        handler.subscribe(self.onEvent, None)
        Wait(3)
        return

    def test_event_handler_invalid_timeout_param(self):
        mock = MockEvent(1)
        eventshandler = AppEventsHandler()
        self.assertRaises(DataParsingError, eventshandler.register, 'MockEvent', 'two')

    def test_AppEvent_payload(self):
        event_content = AppEvent('test', {1: 'one', 2: 'two'})
        self.assertEquals(event_content.name, 'test')
        self.assertEquals(event_content.payload, {1: 'one', 2: 'two'})

    def test_AppEvent_kwdargs(self):
        kwdargs = {'thingone': 'one', 'thingtwo': 'two'}
        event_content = AppEvent('test', thingone='one', thingtwo='two')
        self.assertEquals(event_content.name, 'test')
        for key in kwdargs:
            self.assertEquals(event_content.payload[key], kwdargs[key])

    def onEvent(self, event, expected):
        self.assertEquals(event, expected)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestEvents))
    return suite


class MockEvent(object):
    """ mock event class for event system testing """
    __module__ = __name__

    def __init__(self, data):
        self.name = 'MockEvent'
        self.data = data