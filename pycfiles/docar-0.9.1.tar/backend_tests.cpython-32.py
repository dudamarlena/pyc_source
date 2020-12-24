# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/crito/Work/docar/tests/backend_tests.py
# Compiled at: 2012-09-26 10:57:35
import unittest
from nose.tools import eq_, ok_
from docar.backends import DummyBackend, Backend, BackendManager
from docar import Document, fields

class when_a_backend_gets_declared(unittest.TestCase):

    def setUp(self):
        self.backends_copy = BackendManager.backends
        BackendManager.backends = []

    def tearDown(self):
        BackendManager.backends = self.backends_copy

    def it_stores_the_backend_in_the_backend_manager(self):
        """Using a metaclass, backends are registered with the backend
        manager."""

        class NewBackend(Backend):
            backend_type = 'new'

        eq_(1, len(BackendManager.backends))
        eq_(NewBackend, BackendManager.backends[0])

    def it_can_be_retrieved_by_the_backend_manager(self):
        """The backend manager returns requested backend manager instances."""

        class NewBackend(Backend):
            backend_type = 'new'

        eq_(True, isinstance(BackendManager('new'), NewBackend))


class when_a_backend_gets_instantiated(unittest.TestCase):

    def it_takes_the_backend_type_as_an_argument(self):
        manager = BackendManager('dummy')
        eq_('dummy', manager.backend_type)

    def it_defaults_to_the_django_backend_type(self):
        manager = BackendManager()
        eq_('dummy', manager.backend_type)

    def it_can_specify_the_backend_type_as_a_meta_option(self):

        class Doc(Document):
            id = fields.NumberField()

            class Meta:
                backend_type = 'dummy'

        doc = Doc()
        ok_(isinstance(doc._backend_manager, DummyBackend))