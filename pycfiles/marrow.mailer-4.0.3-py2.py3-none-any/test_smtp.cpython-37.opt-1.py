# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /test/transport/test_smtp.py
# Compiled at: 2019-09-13 21:23:39
# Size of source mod 2**32: 10611 bytes
"""

from __future__ import unicode_literals

import os
import sys
import socket
import logging
import smtplib

from unittest import TestCase
from nose.tools import ok_, eq_, raises
from nose.plugins.skip import Skip, SkipTest

try:
    from pymta.api import IMTAPolicy, PolicyDecision, IAuthenticator
    from pymta.test_util import BlackholeDeliverer, DebuggingMTA, MTAThread
except ImportError: # pragma: no cover
    raise SkipTest("PyMTA not installed; skipping SMTP tests.")

from marrow.mailer import Message
from marrow.mailer.exc import TransportException, TransportExhaustedException, MessageFailedException
from marrow.mailer.transport.smtp import SMTPTransport

log = logging.getLogger('tests')

class SMTPTestCase(TestCase):
    server = None
    Policy = IMTAPolicy
    
    class Authenticator(IAuthenticator):
        def authenticate(self, username, password, peer):
            return True
    
    @classmethod
    def setUpClass(cls):
        assert not cls.server, "Server already running?"
        
        cls.port = __import__('random').randint(9000, 40000)
        cls.collector = BlackholeDeliverer
        cls.host = DebuggingMTA('127.0.0.1', cls.port, cls.collector, policy_class=cls.Policy,
                authenticator_class=cls.Authenticator)
        cls.server = MTAThread(cls.host)
        cls.server.start()
    
    @classmethod
    def tearDownClass(cls):
        if cls.server:
            cls.server.stop()
            cls.server = None

class TestSMTPTransportBase(SMTPTestCase):
    def test_basic_config(self):
        transport = SMTPTransport(dict(port=self.port, timeout="10", tls=False, pipeline="10"))
        
        self.assertEqual(transport.sent, 0)
        self.assertEqual(transport.host, '127.0.0.1')
        self.assertEqual(transport.port, self.port)
        self.assertEqual(transport.timeout, 10)
        self.assertEqual(transport.pipeline, 10)
        self.assertEqual(transport.debug, False)
        
        self.assertEqual(transport.connected, False)
    
    def test_startup_shutdown(self):
        transport = SMTPTransport(dict(port=self.port))
        
        transport.startup()
        self.assertTrue(transport.connected)
        
        transport.shutdown()
        self.assertFalse(transport.connected)
    
    def test_authentication(self):
        transport = SMTPTransport(dict(port=self.port, username='bob', password='dole'))
        
        transport.startup()
        self.assertTrue(transport.connected)
        
        transport.shutdown()
        self.assertFalse(transport.connected)
    
    def test_bad_tls(self):
        transport = SMTPTransport(dict(port=self.port, tls='required'))
        self.assertRaises(TransportException, transport.startup)

class TransportTestCase(SMTPTestCase):
    pipeline = None
    
    def setUp(self):
        self.transport = SMTPTransport(dict(port=self.port, pipeline=self.pipeline))
        self.transport.startup()
        self.msg = self.message
    
    def tearDown(self):
        self.transport.shutdown()
        self.transport = None
        self.msg = None
    
    @property
    def message(self):
        return Message('from@example.com', 'to@example.com', 'Test subject.', plain="Test body.")

class TestSMTPTransport(TransportTestCase):
    def test_send_simple_message(self):
        self.assertRaises(TransportExhaustedException, self.transport.deliver, self.msg)
        self.assertEqual(self.collector.received_messages.qsize(), 1)
        
        message = self.collector.received_messages.get()
        self.assertEqual(message.msg_data, str(self.msg))
        self.assertEqual(message.smtp_from, self.msg.envelope)
        self.assertEqual(message.smtp_to, self.msg.recipients)
    
    def test_send_after_shutdown(self):
        self.transport.shutdown()
        
        self.assertRaises(TransportExhaustedException, self.transport.deliver, self.msg)
        self.assertEqual(self.collector.received_messages.qsize(), 1)
        
        message = self.collector.received_messages.get()
        self.assertEqual(message.msg_data, str(self.msg))
        self.assertEqual(message.smtp_from, self.msg.envelope)
        self.assertEqual(message.smtp_to, self.msg.recipients)
    
    def test_sender(self):
        self.msg.sender = "sender@example.com"
        self.assertEqual(self.msg.envelope, self.msg.sender)
        
        self.assertRaises(TransportExhaustedException, self.transport.deliver, self.msg)
        self.assertEqual(self.collector.received_messages.qsize(), 1)
        
        message = self.collector.received_messages.get()
        self.assertEqual(message.msg_data, str(self.msg))
        self.assertEqual(message.smtp_from, self.msg.envelope)
    
    def test_many_recipients(self):
        self.msg.cc = 'cc@example.com'
        self.msg.bcc = 'bcc@example.com'
        
        self.assertRaises(TransportExhaustedException, self.transport.deliver, self.msg)
        self.assertEqual(self.collector.received_messages.qsize(), 1)
        
        message = self.collector.received_messages.get()
        self.assertEqual(message.msg_data, str(self.msg))
        self.assertEqual(message.smtp_from, self.msg.envelope)
        self.assertEqual(message.smtp_to, self.msg.recipients)

class TestSMTPTransportRefusedSender(TransportTestCase):
    pipeline = 10
    
    class Policy(IMTAPolicy):
        def accept_from(self, sender, message):
            return False
    
    def test_refused_sender(self):
        self.assertRaises(MessageFailedException, self.transport.deliver, self.msg)
        self.assertEquals(self.collector.received_messages.qsize(), 0)

class TestSMTPTransportRefusedRecipients(TransportTestCase):
    pipeline = True
    
    class Policy(IMTAPolicy):
        def accept_rcpt_to(self, sender, message):
            return False
    
    def test_refused_recipients(self):
        self.assertRaises(MessageFailedException, self.transport.deliver, self.msg)
        self.assertEquals(self.collector.received_messages.qsize(), 0)

"""