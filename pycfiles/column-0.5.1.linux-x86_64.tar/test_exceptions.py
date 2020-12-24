# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tests/test_exceptions.py
# Compiled at: 2017-08-02 01:06:09
from testtools import TestCase
from column import exceptions

class TestExceptions(TestCase):

    def setUp(self):
        super(TestExceptions, self).setUp()

    def test_base_exception(self):
        e = exceptions.BaseException()
        self.assertEqual('An unknown exception occurred.', e.msg)

    def test_invalid_parameter(self):
        e = exceptions.InvalidParameter(name='a', param='b')
        self.assertEqual('Invalid type of a on parameter b', e.msg)

    def test_invalid_parameter_no_params(self):
        e = exceptions.InvalidParameter()
        self.assertEqual('Invalid type of %(name)s on parameter %(param)s', e.msg)

    def test_invalid_parameter_wrong_params(self):
        e = exceptions.InvalidParameter(foo='a', bar='b')
        self.assertEqual('Invalid type of %(name)s on parameter %(param)s', e.msg)

    def test_invalid_parameter_custom_msg(self):
        e = exceptions.InvalidParameter(msg='%(name)s + %(param)s = c', name='a', param='b')
        self.assertEqual('a + b = c', e.msg)