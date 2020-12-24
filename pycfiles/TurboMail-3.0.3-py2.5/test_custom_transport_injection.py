# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/tests/test_custom_transport_injection.py
# Compiled at: 2009-08-24 19:48:22
"""Test the injection of custom TurboMail transports without setuptools."""
import logging, unittest
from turbomail.api import Extension, Manager, Transport
from turbomail.control import interface
from turbomail.message import Message
logging.disable(logging.WARNING)

class DummyTransport(Transport):

    def deliver(self, message):
        return True


class DummyManager(Manager):

    def deliver(self, message):
        return True


class DummyExtension(Extension):

    def __init__(self):
        self.started = False

    def start(self):
        self.started = True

    def stop(self):
        self.started = False


class TestCustomTransportInjection(unittest.TestCase):
    """Test the injection of custom TurboMail transports without setuptools."""

    def setUp(self):
        self.manager = DummyManager()
        self.transport = DummyTransport()
        self.message = Message(author=('Author', 'author@example.com'), to=('Recipient',
                                                                            'recipient@example.com'), subject='Test message subject.', plain='This is a test message.')
        self.config = {'mail.on': True}

    def tearDown(self):
        interface.stop(force=True)
        interface.config = {'mail.on': False}

    def test_provide_dict_with_additional_managers_and_transports_which_overrides_setuptools(self):
        config = self.config.copy()
        config.update({'mail.manager': 'immediate', 'mail.transport': 'foo'})
        interface.start(config, extra_classes=dict(immediate=self.manager, foo=self.transport))
        self.assertEqual(self.manager, interface.manager)
        self.assertEqual(self.transport, interface.transport)
        interface.send(self.message)

    def test_dont_fail_if_no_extra_classes_were_provided(self):
        interface.start(self.config)

    def test_can_provide_classes_for_extensions_to_override_setuptools(self):
        config = self.config.copy()
        config.update({'mail.manager': 'immediate', 'mail.transport': 'foo', 'mail.fake_ext.on': True})
        dummy_extension = DummyExtension()
        interface.start(config, extra_classes=dict(immediate=self.manager, foo=self.transport, fake_ext=dummy_extension))
        self.assertEqual(True, dummy_extension.started)

    def test_all_loaded_extensions_are_stopped(self):
        config = self.config.copy()
        config.update({'mail.manager': 'immediate', 'mail.transport': 'foo', 'mail.fake_ext.on': True})
        dummy_extension = DummyExtension()
        interface.start(config, extra_classes=dict(immediate=self.manager, foo=self.transport, fake_ext=dummy_extension))
        self.assertEqual(True, dummy_extension.started)
        interface.stop()
        self.assertEqual(False, dummy_extension.started)