# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ycyc/tests/tools/test_rescuekit.py
# Compiled at: 2016-07-19 10:55:32
from unittest import TestCase
import mock
from ycyc.tools import rescuekit

class TestRescue(TestCase):

    def test_usage(self):
        self.assertIsInstance(rescuekit.Rescue.catch(''), rescuekit.Rescue)
        self.assertIsInstance(rescuekit.Rescue.meet(''), rescuekit.Rescue)
        func_mock = mock.MagicMock()
        rescue = rescuekit.Rescue.catch('')
        func_mock.return_value = 0
        self.assertEqual(rescue.call(func_mock, 1, val=2), 0)
        func_mock.assert_called_once_with(1, val=2)
        func_mock = mock.MagicMock()
        func_mock.side_effect = ValueError
        self.assertEqual(rescue.call(func_mock, val=3), '')
        func_mock.assert_called_once_with(val=3)
        rescue = rescuekit.Rescue.catch('ValueError', ValueError).catch('KeyError', KeyError).meet('', None)
        func_mock = mock.MagicMock()
        func_mock.side_effect = ValueError
        self.assertEqual(rescue.call(func_mock), 'ValueError')
        func_mock = mock.MagicMock()
        func_mock.side_effect = KeyError
        self.assertEqual(rescue.call(func_mock), 'KeyError')
        func_mock = mock.MagicMock()
        func_mock.return_value = None
        self.assertEqual(rescue.call(func_mock), '')
        self.assertEqual(rescuekit.Rescue.catch('nan').call(lambda : 1 / 0), 'nan')
        return