# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zupo/work/tutorial.todoapp/src/tutorial/todoapp/tests/test_todo_item.py
# Compiled at: 2012-09-05 03:54:45
"""Test Todo Item content type."""
from tutorial.todoapp.tests.base import IntegrationTestCase
from plone import api
import unittest2 as unittest

class TestRequests(IntegrationTestCase):
    """Test the Todo Item content type."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.folder = self.portal.folder

    def test_add_todo_item(self):
        """Test that we can add a Todo Item."""
        api.content.create(container=self.folder, type='todo_item', title='Try Brulé!')
        self.assertEquals(self.folder['try-brule'].title, 'Try Brulé!')


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)