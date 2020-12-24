# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /test/test_exceptions.py
# Compiled at: 2019-09-13 21:23:39
# Size of source mod 2**32: 384 bytes
"""Test the primary configurator interface, Delivery."""
from unittest import TestCase
from marrow.mailer.exc import DeliveryFailedException

def test_delivery_failed_exception_init():
    exc = DeliveryFailedException('message', 'reason')
    assert exc.msg == 'message'
    assert exc.reason == 'reason'
    assert exc.args[0] == 'message'
    assert exc.args[1] == 'reason'