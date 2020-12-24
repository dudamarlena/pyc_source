# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: H:\workspaces\workspace-python\big-brother-bot\tests\plugins\test_location.py
# Compiled at: 2015-05-27 19:37:28
import time, logging, unittest2
from mock import Mock
from mockito import when, unstub
from b3.config import MainConfig
from b3.config import CfgConfigParser
from b3.plugins.admin import AdminPlugin
from b3.plugins.location import LocationPlugin
from textwrap import dedent
LOCATION_MIKE = Mock()
LOCATION_MIKE.country = 'Italy'
LOCATION_MIKE.region = 'Lazio'
LOCATION_MIKE.city = 'Rome'
LOCATION_MIKE.cc = 'IT'
LOCATION_MIKE.rc = '07'
LOCATION_MIKE.isp = 'Fastweb'
LOCATION_MIKE.timezone = 'Europe/Rome'
LOCATION_MIKE.lat = 41.9
LOCATION_MIKE.lon = 12.4833
LOCATION_MIKE.zipcode = 64
LOCATION_BILL = Mock()
LOCATION_BILL.country = 'United States'
LOCATION_BILL.region = 'California'
LOCATION_BILL.city = 'Mountain View'
LOCATION_BILL.cc = 'US'
LOCATION_BILL.rc = 'CA'
LOCATION_BILL.isp = 'Google Inc.'
LOCATION_BILL.timezone = 'America/Los_Angeles'
LOCATION_BILL.lat = 37.386
LOCATION_BILL.lon = -122.0838
LOCATION_BILL.zipcode = 94035

class logging_disabled(object):
    """
    Context manager that temporarily disable logging.

    USAGE:
        with logging_disabled():
            # do stuff
    """
    DISABLED = False

    def __init__(self):
        self.nested = logging_disabled.DISABLED

    def __enter__(self):
        if not self.nested:
            logging.getLogger('output').propagate = False
            logging_disabled.DISABLED = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.nested:
            logging.getLogger('output').propagate = True
            logging_disabled.DISABLED = False


class LocationTestCase(unittest2.TestCase):

    def setUp(self):
        parser_ini_conf = CfgConfigParser()
        parser_ini_conf.loadFromString('')
        self.parser_main_conf = MainConfig(parser_ini_conf)
        with logging_disabled():
            from b3.fake import FakeConsole
            self.console = FakeConsole(self.parser_main_conf)
        with logging_disabled():
            self.adminPlugin = AdminPlugin(self.console, '@b3/conf/plugin_admin.ini')
            self.adminPlugin._commands = {}
            self.adminPlugin.onStartup()
        when(self.console).getPlugin('admin').thenReturn(self.adminPlugin)
        self.console.createEvent('EVT_CLIENT_GEOLOCATION_SUCCESS', 'Event client geolocation success')
        self.console.screen = Mock()
        self.console.time = time.time
        self.console.upTime = Mock(return_value=1000)
        self.console.cron.stop()
        self.conf = CfgConfigParser()
        self.conf.loadFromString(dedent("\n            [settings]\n            announce: yes\n\n            [messages]\n            client_connect: ^7$name ^3from ^7$city ^3(^7$country^3) connected\n            cmd_locate: ^7$name ^3is connected from ^7$city ^3(^7$country^3)\n            cmd_locate_failed: ^7Could not locate ^1$name\n            cmd_distance: ^7$name ^3is ^7$distance ^3km away from you\n            cmd_distance_self: ^7Sorry, I'm not that smart...meh!\n            cmd_distance_failed: ^7Could not compute distance with ^1$name\n            cmd_isp: ^7$name ^3is using ^7$isp ^3as isp\n            cmd_isp_failed: ^7Could not determine ^1$name ^7isp\n\n            [commands]\n            locate: user\n            distance: user\n            isp: mod\n        "))
        self.p = LocationPlugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()
        with logging_disabled():
            from b3.fake import FakeClient
        self.mike = FakeClient(console=self.console, name='Mike', guid='MIKEGUID', groupBits=1)
        self.bill = FakeClient(console=self.console, name='Bill', guid='BILLGUID', groupBits=16)
        self.mike.location = LOCATION_MIKE
        self.bill.location = LOCATION_BILL

    def tearDown(self):
        unstub()

    def test_event_client_geolocation_success(self):
        self.mike.connects('1')
        self.console.say = Mock()
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_GEOLOCATION_SUCCESS', client=self.mike))
        self.console.say.assert_called_with('^7Mike ^3from ^7Rome ^3(^7Italy^3) connected')

    def test_cmd_locate_no_arguments(self):
        self.mike.connects('1')
        self.bill.connects('2')
        self.mike.clearMessageHistory()
        self.mike.says('!locate')
        self.assertListEqual(['missing data, try !help locate'], self.mike.message_history)

    def test_cmd_locate_failed(self):
        self.mike.connects('1')
        self.bill.connects('2')
        self.bill.location = None
        self.mike.clearMessageHistory()
        self.mike.says('!locate bill')
        self.assertListEqual(['Could not locate Bill'], self.mike.message_history)
        return

    def test_cmd_locate(self):
        self.mike.connects('1')
        self.bill.connects('2')
        self.mike.clearMessageHistory()
        self.mike.says('!locate bill')
        self.assertListEqual(['Bill is connected from Mountain View (United States)'], self.mike.message_history)

    def test_cmd_distance_no_arguments(self):
        self.mike.connects('1')
        self.bill.connects('2')
        self.mike.clearMessageHistory()
        self.mike.says('!distance')
        self.assertListEqual(['missing data, try !help distance'], self.mike.message_history)

    def test_cmd_distance_self(self):
        self.mike.connects('1')
        self.bill.connects('2')
        self.mike.clearMessageHistory()
        self.mike.says('!distance mike')
        self.assertListEqual(["Sorry, I'm not that smart...meh!"], self.mike.message_history)

    def test_cmd_distance_failed(self):
        self.mike.connects('1')
        self.bill.connects('2')
        self.bill.location = None
        self.mike.clearMessageHistory()
        self.mike.says('!distance bill')
        self.assertListEqual(['Could not compute distance with Bill'], self.mike.message_history)
        return

    def test_cmd_distance(self):
        self.mike.connects('1')
        self.bill.connects('2')
        self.mike.clearMessageHistory()
        self.mike.says('!distance bill')
        self.assertListEqual(['Bill is 10068.18 km away from you'], self.mike.message_history)

    def test_cmd_isp_no_arguments(self):
        self.mike.connects('1')
        self.bill.connects('2')
        self.bill.clearMessageHistory()
        self.bill.says('!isp')
        self.assertListEqual(['missing data, try !help isp'], self.bill.message_history)

    def test_cmd_isp_failed(self):
        self.mike.connects('1')
        self.bill.connects('2')
        self.mike.location = None
        self.bill.clearMessageHistory()
        self.bill.says('!isp mike')
        self.assertListEqual(['Could not determine Mike isp'], self.bill.message_history)
        return

    def test_cmd_isp(self):
        self.mike.connects('1')
        self.bill.connects('2')
        self.bill.clearMessageHistory()
        self.bill.says('!isp mike')
        self.assertListEqual(['Mike is using Fastweb as isp'], self.bill.message_history)