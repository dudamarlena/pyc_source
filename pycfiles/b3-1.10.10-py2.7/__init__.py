# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\__init__.py
# Compiled at: 2016-03-08 18:42:10
import logging, threading, sys
from b3.config import CfgConfigParser
from b3.config import MainConfig
from contextlib import contextmanager
logging.raiseExceptions = False
import b3.output
log = logging.getLogger('output')
log.setLevel(logging.WARNING)
from mock import Mock, patch
import time, unittest2 as unittest
from b3.events import Event
testcase_lock = threading.Lock()

class logging_disabled(object):
    """
    context manager that temporarily disable logging.

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


def flush_console_streams():
    sys.stderr.flush()
    sys.stdout.flush()


class B3TestCase(unittest.TestCase):

    def setUp(self):
        testcase_lock.acquire()
        flush_console_streams()
        self.parser_conf = MainConfig(CfgConfigParser(allow_no_value=True))
        self.parser_conf.loadFromString('')
        with logging_disabled():
            from b3.fake import FakeConsole
            self.console = FakeConsole(self.parser_conf)
        self.console.screen = Mock()
        self.console.time = time.time
        self.console.upTime = Mock(return_value=3)
        self.console.cron.stop()

        def myError(msg, *args, **kwargs):
            print 'ERROR: %s' % msg % args

        self.console.error = myError

    def tearDown(self):
        flush_console_streams()
        testcase_lock.release()

    @contextmanager
    def assertRaiseEvent(self, event_type, event_client=None, event_data=None, event_target=None):
        """
        USAGE:
            def test_team_change(self):
            # GIVEN
            self.client._team = TEAM_RED
            # THEN
            with self.assertRaiseEvent(
                event_type='EVT_CLIENT_TEAM_CHANGE',
                event_data=24,
                event_client=self.client,
                event_target=None):
                # WHEN
                self.client.team = 24
        """
        if type(event_type) is basestring:
            event_type_name = event_type
        else:
            event_type_name = self.console.getEventName(event_type)
            self.assertIsNotNone(event_type_name, "could not find event with name '%s'" % event_type)
        with patch.object(self.console, 'queueEvent') as (queueEvent):
            yield
            if event_type is None:
                assert not queueEvent.called
                return
            assert queueEvent.called, 'No event was fired'

        def assertEvent(queueEvent_call_args):
            eventraised = queueEvent_call_args[0][0]
            return type(eventraised) == Event and self.console.getEventName(eventraised.type) == event_type_name and eventraised.data == event_data and eventraised.target == event_target and eventraised.client == event_client

        assert any(map(assertEvent, queueEvent.call_args_list)), 'Event %s(%r) not fired' % (self.console.getEventName(event_type),
         {'event_client': event_client, 
            'event_data': event_data, 
            'event_target': event_target})
        return


class InstantTimer(object):

    def __init__(self, interval, function, args=[], kwargs={}):
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def cancel(self):
        pass

    def start(self):
        self.run()

    def run(self):
        self.function(*self.args, **self.kwargs)