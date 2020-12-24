# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: H:\workspaces\workspace-python\big-brother-bot\tests\plugins\test_geolocation.py
# Compiled at: 2015-05-27 19:37:28
import sys, time, logging
from mock import Mock
from mockito import unstub
from b3.fake import FakeClient
from b3.plugins.geolocation import GeolocationPlugin
from b3.plugins.geolocation.location import Location
from nose.plugins.attrib import attr
from tests import B3TestCase
from unittest2 import skip

class GeolocationTestCase(B3TestCase):

    def setUp(self):
        self.log = logging.getLogger('output')
        self.log.propagate = False
        B3TestCase.setUp(self)
        self.console.screen = Mock()
        self.console.time = time.time
        self.console.upTime = Mock(return_value=3)
        self.p = GeolocationPlugin(self.console)
        self.p.onLoadConfig()
        self.p.onStartup()
        self.log.propagate = True
        self.mike = FakeClient(console=self.console, name='Mike', guid='MIKEGUID', groupBits=1)

    def tearDown(self):
        B3TestCase.tearDown(self)
        unstub()

    @skip
    @attr('slow')
    def test_event_client_geolocation_success(self):
        self.mike.ip = '8.8.8.8'
        self.mike.connects('1')
        time.sleep(6)
        self.assertEqual(True, hasattr(self.mike, 'location'))
        self.assertIsNotNone(self.mike.location)
        self.assertIsInstance(self.mike.location, Location)
        print >> sys.stderr, 'IP: %s : %r' % (self.mike.ip, self.mike.location)

    @skip
    @attr('slow')
    def test_event_client_geolocation_failure(self):
        self.mike.ip = '--'
        self.mike.connects('1')
        time.sleep(6)
        self.assertIsNone(self.mike.location)
        print >> sys.stderr, 'IP: %s : %r' % (self.mike.ip, self.mike.location)

    @skip
    @attr('slow')
    def test_event_client_geolocation_success_maxmind(self):
        self.p._geolocators.pop(0)
        self.p._geolocators.pop(0)
        self.p._geolocators.pop(0)
        self.mike.ip = '8.8.8.8'
        self.mike.connects('1')
        time.sleep(2)
        self.assertGreaterEqual(len(self.p._geolocators), 1)
        self.assertIsNotNone(self.mike.location)
        self.assertIsNone(self.mike.location.isp)
        print >> sys.stderr, 'IP: %s : %r' % (self.mike.ip, self.mike.location)

    @skip
    @attr('slow')
    def test_event_client_geolocation_success_maxmind_using_event_client_update(self):
        self.p._geolocators.pop(0)
        self.p._geolocators.pop(0)
        self.p._geolocators.pop(0)
        self.mike.ip = ''
        self.mike.connects('1')
        self.mike.ip = '8.8.8.8'
        self.mike.save(self.console)
        time.sleep(4)
        self.assertGreaterEqual(len(self.p._geolocators), 1)
        self.assertEqual(True, hasattr(self.mike, 'location'))
        self.assertIsNotNone(self.mike.location)
        self.assertIsInstance(self.mike.location, Location)
        print >> sys.stderr, 'IP: %s : %r' % (self.mike.ip, self.mike.location)