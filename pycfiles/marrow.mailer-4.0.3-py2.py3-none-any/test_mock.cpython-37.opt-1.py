# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /test/transport/test_mock.py
# Compiled at: 2019-09-13 21:23:39
# Size of source mod 2**32: 1242 bytes
"""

from __future__ import unicode_literals

import logging

from unittest import TestCase
from nose.tools import ok_, eq_, raises
from nose.plugins.skip import Skip, SkipTest

from marrow.mailer import Message
from marrow.mailer.exc import TransportFailedException, TransportExhaustedException
from marrow.mailer.transport.mock import MockTransport

from marrow.util.bunch import Bunch

log = logging.getLogger('tests')

class TestMockTransport(TestCase):
    def test_success(self):
        transport = MockTransport(dict(success=1.1))
        self.assertTrue(transport.deliver(None))
    
    def test_failure(self):
        transport = MockTransport(dict(success=0.0))
        self.assertFalse(transport.deliver(None))
        
        transport = MockTransport(dict(success=0.0, failure=1.0))
        self.assertRaises(TransportFailedException, transport.deliver, None)
    
    def test_death(self):
        transport = MockTransport(dict())
        self.assertRaises(ZeroDivisionError, transport.deliver, Bunch(die=True))
    
    def test_exhaustion(self):
        transport = MockTransport(dict(success=0.0, exhaustion=1.0))
        self.assertRaises(TransportExhaustedException, transport.deliver, None)

"""