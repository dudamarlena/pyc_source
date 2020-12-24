# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/tests/test_callback.py
# Compiled at: 2019-12-17 19:37:11
# Size of source mod 2**32: 4598 bytes
from django.test import TestCase
from . import fixtures
from . import mocks
from djconnectwise.callbacks import CallbacksHandler
NEEDED_CALLBACKS = [
 {'type':'ticket', 
  'description':'Kanban application ticket callback', 
  'url':None, 
  'objectId':1, 
  'level':'owner'},
 {'type':'project', 
  'description':'Kanban application project callback', 
  'url':None, 
  'objectId':1, 
  'level':'owner'},
 {'type':'company', 
  'description':'Kanban application company callback', 
  'url':None, 
  'objectId':1, 
  'level':'owner'}]

class TestCallBackHandler(TestCase):

    def setUp(self):
        super().setUp()
        self.handler = CallbacksHandler()

    def test_calculate_no_changes(self):
        needed = NEEDED_CALLBACKS.copy()
        current = needed.copy()
        add, remove = self.handler._calculate_missing_unneeded_callbacks(needed, current)
        self.assertEqual(add, [])
        self.assertEqual(remove, [])

    def test_calculate_callback_needs_adding(self):
        needed = NEEDED_CALLBACKS.copy()
        current = [
         {'type':'ticket', 
          'description':'Kanban application ticket callback', 
          'url':None, 
          'objectId':1, 
          'level':'owner'},
         {'type':'company', 
          'description':'Kanban application company callback', 
          'url':None, 
          'objectId':1, 
          'level':'owner'}]
        add, remove = self.handler._calculate_missing_unneeded_callbacks(needed, current)
        self.assertEqual(add, [
         {'type':'project', 
          'description':'Kanban application project callback', 
          'url':None, 
          'objectId':1, 
          'level':'owner'}])
        self.assertEqual(remove, [])

    def test_calculate_callback_needs_removing(self):
        needed = NEEDED_CALLBACKS.copy()
        current = needed.copy()
        current.insert(1, {'type':'opportunity', 
         'description':'Kanban application opportunity callback', 
         'url':None, 
         'objectId':1, 
         'level':'owner'})
        add, remove = self.handler._calculate_missing_unneeded_callbacks(needed, current)
        self.assertEqual(add, [])
        self.assertEqual(remove, [
         {'type':'opportunity', 
          'description':'Kanban application opportunity callback', 
          'url':None, 
          'objectId':1, 
          'level':'owner'}])

    def test_calculate_callback_field_changed(self):
        """
        A field is different between a current and needed callback, resulting
        in one CB to add and one CB to delete.
        """
        needed = NEEDED_CALLBACKS.copy()
        current = needed.copy()
        current[0] = {'type':'ticket', 
         'description':'wrong description!', 
         'url':None, 
         'objectId':1, 
         'level':'owner'}
        add, remove = self.handler._calculate_missing_unneeded_callbacks(needed, current)
        self.assertEqual(add, [
         {'type':'ticket', 
          'description':'Kanban application ticket callback', 
          'url':None, 
          'objectId':1, 
          'level':'owner'}])
        self.assertEqual(remove, [
         {'type':'ticket', 
          'description':'wrong description!', 
          'url':None, 
          'objectId':1, 
          'level':'owner'}])

    def test_get_callbacks(self):
        fixture = [
         fixtures.API_SYSTEM_CALLBACK_ENTRY]
        mocks.system_api_get_callbacks_call(fixture)
        callbacks = self.handler.get_callbacks()
        self.assertEqual(callbacks, fixture)