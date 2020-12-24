# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ycyc/tests/ycollections/test_namedict.py
# Compiled at: 2016-07-19 10:55:32
from unittest import TestCase
import mock, time
from ycyc.ycollections.namedict import namedict, RequireFieldsMissError

class TestNamedDict(TestCase):

    def test_usage(self):
        cur_time = time.time()
        Params = namedict('InvokeParams', requires=('sender', 'callback'), fields={'value': None, 
           'time': cur_time})
        self.assertEqual(Params.__name__, 'InvokeParams')
        with self.assertRaisesRegexp(RequireFieldsMissError, (', ').join({'sender', 'callback'})):
            Params()
        with self.assertRaisesRegexp(RequireFieldsMissError, 'sender'):
            Params(callback=None)
        with self.assertRaisesRegexp(RequireFieldsMissError, 'callback'):
            Params(sender=None)
        params = Params('test', 1)
        self.assertIsInstance(params, dict)
        self.assertEqual(params.sender, 'test')
        self.assertEqual(params.callback, 1)
        self.assertEqual(params.value, None)
        self.assertEqual(params.time, cur_time)
        params = Params(sender='test', callback=2)
        self.assertIsInstance(params, dict)
        self.assertEqual(params.sender, 'test')
        self.assertEqual(params.callback, 2)
        self.assertEqual(params.value, None)
        self.assertEqual(params.time, cur_time)
        params = Params('test', None, value=1)
        self.assertIsInstance(params, dict)
        self.assertEqual(params.sender, 'test')
        self.assertEqual(params.callback, None)
        self.assertEqual(params.value, 1)
        self.assertEqual(params.time, cur_time)
        params = Params('test', None, value=1, time=2)
        self.assertIsInstance(params, dict)
        self.assertEqual(params.sender, 'test')
        self.assertEqual(params.callback, None)
        self.assertEqual(params.value, 1)
        self.assertEqual(params.time, 2)
        Params = namedict('InvokeParams', requires=('sender', 'callback'), fields=(
         ('value', None),
         (
          'time', cur_time)))
        params = Params('test', None, 1)
        self.assertIsInstance(params, dict)
        self.assertEqual(params.sender, 'test')
        self.assertEqual(params.callback, None)
        self.assertEqual(params.value, 1)
        self.assertEqual(params.time, cur_time)
        params = Params('test', None, 1, 2)
        self.assertIsInstance(params, dict)
        self.assertEqual(params.sender, 'test')
        self.assertEqual(params.callback, None)
        self.assertEqual(params.value, 1)
        self.assertEqual(params.time, 2)
        params = Params('test', None, 1, value=2)
        self.assertIsInstance(params, dict)
        self.assertEqual(params.sender, 'test')
        self.assertEqual(params.callback, None)
        self.assertEqual(params.value, 1)
        self.assertEqual(params.time, cur_time)
        params = Params('test', None, 1, value=2, nothing=3)
        self.assertIsInstance(params, dict)
        self.assertEqual(params.sender, 'test')
        self.assertEqual(params.callback, None)
        self.assertEqual(params.value, 1)
        self.assertEqual(params.time, cur_time)
        with self.assertRaises(AttributeError):
            params.nothing
        Params = namedict('Params', ['key', 'value'])
        params = Params('test', value=2)
        self.assertEqual(params.key, 'test')
        self.assertEqual(params.value, 2)
        return

    def test_logging(self):
        with mock.patch('ycyc.ycollections.namedict.logger'):
            from ycyc.ycollections.namedict import logger
            TestDict = namedict('TestDict', {'val': None})
            tdict = TestDict(1)
            self.assertEqual(tdict.val, 1)
            self.assertEqual(logger.warning.call_count, 0)
            tdict = TestDict(1, 2)
            self.assertEqual(tdict.val, 1)
            self.assertEqual(logger.warning.call_count, 1)
            self.assertListEqual(logger.warning.call_args[0][1], [2])
            tdict = TestDict(1, nothing=2)
            self.assertEqual(tdict.val, 1)
            self.assertEqual(logger.warning.call_count, 2)
            self.assertSetEqual(logger.warning.call_args[0][1], {'nothing'})
        return