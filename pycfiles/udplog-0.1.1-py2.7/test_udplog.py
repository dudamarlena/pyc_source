# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/udplog/test/test_udplog.py
# Compiled at: 2013-11-07 08:00:01
"""
Tests for L{udplog.udplog}.
"""
from __future__ import division, absolute_import
import errno, logging, socket, sys, time, StringIO
from twisted.trial import unittest
from udplog import udplog

class UDPLoggerTest(unittest.TestCase):
    """
    Tests for {udplog.udplog.UDPLogger}.
    """
    MAX_DATAGRAM_SIZE = 8192

    def setUp(self):
        self.output = []

    def send(self, data):
        """
        Fake socket.send that records all log events.
        """
        if len(data) > self.MAX_DATAGRAM_SIZE:
            raise socket.error(errno.EMSGSIZE, 'Message too long')
        else:
            self.output.append(data)

    def _catchOutput(self, logger):
        self.patch(logger.socket, 'send', self.send)
        return logger

    def test_log(self):
        """
        A log event is serialized and sent out over UDP.
        """
        logger = udplog.UDPLogger()
        self._catchOutput(logger)
        logger.log('test', {'message': 'test'})
        self.assertEqual(1, len(self.output))
        msg = self.output[0]
        self.assertRegexpMatches(msg, '^test:\\t{.*}$')
        category, eventDict = udplog.unserialize(msg)
        self.assertEqual('test', category)
        self.assertIn('message', eventDict)
        self.assertEqual('test', eventDict['message'])

    def test_logNotDict(self):
        """
        If eventDict is not a dict, TypeError is raised.
        """
        logger = udplog.UDPLogger()
        self.assertRaises(AttributeError, logger.log, 'acategory', 1)

    def test_logObjects(self):
        """
        Arbitrary objects do not choke the JSON encoding.
        """

        class Something(object):
            pass

        something = Something()
        logger = udplog.UDPLogger()
        self._catchOutput(logger)
        logger.log('atest', {'something': something})
        category, eventDict = udplog.unserialize(self.output[0])
        self.assertEqual(repr(something), eventDict['something'])

    def test_logNonUnicode(self):
        """
        Non-utf8-encodable dicts raise a UnicodeDecodeError.

        Ensure passing an *utf8 encodable* dict to udplog, otherwise you will
        make simplejson cry.
        """
        logger = udplog.UDPLogger()
        self.assertRaises(UnicodeDecodeError, logger.log, 'atest', {'good': 'abc', 'bad': b'\x80abc'})

    def test_logTooLong(self):
        """
        If the log event is too long to fit in a UDP datagram, send regrets.
        """
        logger = udplog.UDPLogger()
        self._catchOutput(logger)
        logger.log('atest', {'message': 'a' * self.MAX_DATAGRAM_SIZE, 'timestamp': 1357328823.75116})
        self.assertEqual(1, len(self.output))
        category, eventDict = udplog.unserialize(self.output[0])
        self.assertEqual('udplog', category)
        self.assertEqual('Failed to send udplog message', eventDict['message'])
        self.assertEqual('socket.error', eventDict['excType'])
        self.assertEqual('[Errno %d] Message too long' % errno.EMSGSIZE, eventDict['excValue'])
        self.assertIn('excText', eventDict)
        self.assertEqual('WARNING', eventDict['logLevel'])
        original = eventDict['original']
        self.assertEqual('atest', original['category'])
        self.assertEqual(1357328823.75116, original['timestamp'])
        self.assertEqual('a' * (udplog.MAX_TRIMMED_MESSAGE_SIZE - 4) + '[..]', original['message'])
        self.assertEqual(self.MAX_DATAGRAM_SIZE, eventDict['original_message_size'])
        self.assertLess(self.MAX_DATAGRAM_SIZE, eventDict['original_size'])

    def test_logTooLongAdditionalFields(self):
        """
        If the log event is too long, keep several fields.
        """
        logger = udplog.UDPLogger()
        self._catchOutput(logger)
        eventDict = {'message': 'a' * self.MAX_DATAGRAM_SIZE, 
           'timestamp': 1357328823.75116, 
           'logLevel': 'ERROR', 
           'logName': __name__, 
           'excType': 'exceptions.ValueError', 
           'excValue': 'Oops', 
           'excText': 'exceptions.ValueError: Oops', 
           'filename': __file__, 
           'lineno': 4, 
           'funcName': 'test_log_too_long_additional_fields', 
           'foo': 'bar'}
        logger.log('atest', eventDict)
        self.assertEqual(1, len(self.output))
        category, failEventDict = udplog.unserialize(self.output[0])
        original = failEventDict['original']
        self.assertEqual(eventDict['logLevel'], original['logLevel'])
        self.assertEqual(eventDict['logName'], original['logName'])
        self.assertEqual(eventDict['excType'], original['excType'])
        self.assertEqual(eventDict['excValue'], original['excValue'])
        self.assertEqual(eventDict['excText'], original['excText'])
        self.assertEqual(eventDict['filename'], original['filename'])
        self.assertEqual(eventDict['lineno'], original['lineno'])
        self.assertEqual(eventDict['funcName'], original['funcName'])
        self.assertNotIn('foo', original)

    def test_logTooLongCategory(self):
        """
        If the log category is way too long, an exception is printed to stderr.
        """
        logger = udplog.UDPLogger()
        self._catchOutput(logger)
        eventDict = {'message': 'a' * self.MAX_DATAGRAM_SIZE, 
           'timestamp': 1357328823.75116}
        self.addCleanup(setattr, sys, 'stderr', sys.stderr)
        sys.stderr = StringIO.StringIO()
        logger.log('a' * self.MAX_DATAGRAM_SIZE, eventDict)
        self.assertEqual(0, len(self.output))
        self.assertRegexpMatches(sys.stderr.getvalue(), '^Failed to send udplog message\\n.*Message too long')

    def test_logTooLongTimestamp(self):
        """
        If the log event is too long, the warning has a timestamp.
        """
        logger = udplog.UDPLogger()
        self._catchOutput(logger)
        logger.log('atest', {'message': 'a' * self.MAX_DATAGRAM_SIZE, 'timestamp': 1357328823.75116})
        self.assertEqual(1, len(self.output))
        category, eventDict = udplog.unserialize(self.output[0])
        self.assertIn('timestamp', eventDict)

    def test_logTooLongDefault(self):
        """
        If the log event is too long, the warning has default fields.
        """
        logger = udplog.UDPLogger(defaultFields={'foo': 'bar'})
        self._catchOutput(logger)
        logger.log('atest', {'message': 'a' * self.MAX_DATAGRAM_SIZE, 'timestamp': 1357328823.75116})
        self.assertEqual(1, len(self.output))
        category, eventDict = udplog.unserialize(self.output[0])
        self.assertIn('foo', eventDict)

    def test_augmentTimestamp(self):
        """
        Every log event gets a timestamp if not already set.
        """
        logger = udplog.UDPLogger()
        self._catchOutput(logger)
        before = time.time()
        logger.log('test', {'message': 'test'})
        after = time.time()
        category, eventDict = udplog.unserialize(self.output[0])
        self.assertIn('timestamp', eventDict)
        timestamp = eventDict['timestamp']
        self.assertGreaterEqual(timestamp, before)
        self.assertLessEqual(timestamp, after)

    def test_augmentDefaultFields(self):
        """
        Every log event gets default fields.
        """
        defaultFields = {'hostname': 'foo.example.org'}
        logger = udplog.UDPLogger(defaultFields=defaultFields)
        self._catchOutput(logger)
        logger.log('test', {'message': 'test'})
        category, eventDict = udplog.unserialize(self.output[0])
        self.assertIn('hostname', eventDict)
        self.assertEqual('foo.example.org', eventDict['hostname'])

    def test_augmentDefaultFieldsOverride(self):
        """
        Default fields can be overridden in individual events.
        """
        defaultFields = {'hostname': 'foo.example.org'}
        logger = udplog.UDPLogger(defaultFields=defaultFields)
        self._catchOutput(logger)
        logger.log('test', {'message': 'test', 'hostname': 'bar.example.org'})
        category, eventDict = udplog.unserialize(self.output[0])
        self.assertIn('hostname', eventDict)
        self.assertEqual('bar.example.org', eventDict['hostname'])


class UDPLogHandlerTest(unittest.TestCase):
    """
    Tests for L{udplog.logging.UDPLogHandler}.
    """

    def setUp(self):
        self.udplogger = udplog.MemoryLogger()
        self.handler = udplog.UDPLogHandler(self.udplogger, category='test')
        self.logger = logging.Logger('test_logger')
        self.logger.addHandler(self.handler)

    def test_emit(self):
        """
        A message logged through python logging is sent out over udp.
        """
        self.logger.debug('Hello')
        self.assertEqual(1, len(self.udplogger.logged))
        category, eventDict = self.udplogger.logged[(-1)]
        self.assertEqual('Hello', eventDict.get('message'))
        self.assertEqual('DEBUG', eventDict.get('logLevel'))
        self.assertEqual('test_logger', eventDict.get('logName'))
        self.assertIn('timestamp', eventDict)

    def test_emitFormatted(self):
        """
        Messages are formatted and arguments are included in the event.
        """
        self.logger.debug('Hello, %(object)s!', {'object': 'world'})
        self.assertEqual(1, len(self.udplogger.logged))
        category, eventDict = self.udplogger.logged[(-1)]
        self.assertEqual('Hello, world!', eventDict.get('message'))
        self.assertEqual('world', eventDict.get('object'))

    def test_emitException(self):
        """
        Logging an exception renders the traceback.
        """
        try:
            {}['something']
        except Exception:
            self.logger.exception('Oops')

        self.assertEqual(1, len(self.udplogger.logged))
        _, eventDict = self.udplogger.logged[(-1)]
        self.assertEqual('Oops', eventDict.get('message'))
        self.assertEqual('ERROR', eventDict.get('logLevel'))
        self.assertEqual('exceptions.KeyError', eventDict.get('excType'))
        self.assertEqual("'something'", eventDict.get('excValue'))
        self.assertTrue(eventDict.get('excText').startswith('Traceback'))

    def test_emitExceptionWithoutContext(self):
        """
        Logging an exception without context succeeds.

        If L{logging.Logger.exception} is called outside of an C{except} block,
        exception context might be lost. The result of the internal call to
        C{sys.exc_info} then yields a tuple of three C{None}s, which should
        simply result in the C{excValue} being C{'None'}.
        """
        self.logger.exception('Oops')
        self.assertEqual(1, len(self.udplogger.logged))
        _, eventDict = self.udplogger.logged[(-1)]
        self.assertEqual('Oops', eventDict.get('message'))
        self.assertEqual('ERROR', eventDict.get('logLevel'))
        self.assertIdentical('NoneType', eventDict.get('excType'))
        self.assertEqual('None', eventDict.get('excValue'))
        self.assertIdentical(None, eventDict['excText'])
        return

    def test_emit_extra(self):
        """
        Values passed in the extra keyword argument are added to the eventDict.
        """
        self.logger.debug('Hello', extra={'foo': 'bar'})
        category, eventDict = self.udplogger.logged[(-1)]
        self.assertIn('foo', eventDict)
        self.assertEqual('bar', eventDict['foo'])


class UDPLogHandlerFactoryTest(unittest.TestCase):
    """
    Tests for L{udplog.ConfigurableUDPLogHandler}.
    """

    def test_argsDefaults(self):
        """
        Without arguments, the logger and handler have their defaults.
        """
        handler = udplog.ConfigurableUDPLogHandler()
        logger = handler.logger
        self.assertEquals('python_logging', handler.category)
        self.assertEquals(('127.0.0.1', 55647), logger.socket.getpeername())
        self.assertEquals({'hostname': socket.gethostname()}, logger.defaultFields)

    def test_args(self):
        """
        All arguments are passed on.
        """
        handler = udplog.ConfigurableUDPLogHandler({'foo': 'bar'}, 'test', '10.0.0.1', 55648, False)
        logger = handler.logger
        self.assertEquals('test', handler.category)
        self.assertEquals(('10.0.0.1', 55648), logger.socket.getpeername())
        self.assertNotIn('hostname', logger.defaultFields)
        self.assertEquals('bar', logger.defaultFields['foo'])