# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zupo/work/osha.quizzes/src/osha/quizzes/tests/test_content.py
# Compiled at: 2012-10-18 11:02:24
"""Test custom content types."""
from osha.quizzes.tests.base import IntegrationTestCase
from plone import api
from plone.api.exc import InvalidParameterError
from Products.statusmessages.interfaces import IStatusMessage
import unittest2 as unittest

class TestContent(IntegrationTestCase):
    """Test custom content types."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_create(self):
        """See if we can create custom content types without error."""
        with self.assertRaises(InvalidParameterError):
            api.content.create(container=self.portal, type='PFGCorrectAnswersAdapter', id='correct-answers')
        api.content.create(container=self.portal, type='FormFolder', id='quiz')
        api.content.create(container=self.portal.quiz, type='PFGCorrectAnswersAdapter', id='adapter')
        adapter = self.portal.quiz.get('adapter')
        self.assertEqual(adapter.id, 'adapter')
        self.assertEqual(adapter.portal_type, 'PFGCorrectAnswersAdapter')

    def test_points_calculation(self):
        """Test that points are correctly calculated.

        Also confirm that the result is nicely printed to a portal
        message.

        """
        api.content.create(container=self.portal, type='FormFolder', id='quiz')
        api.content.create(container=self.portal.quiz, type='PFGCorrectAnswersAdapter', id='adapter')
        api.content.create(container=self.portal.quiz, type='FormSelectionField', id='question-1', correct_answer='5')
        api.content.create(container=self.portal.quiz, type='FormSelectionField', id='question-2', correct_answer='7')
        self.request.form['question-1'] = '5'
        self.request.form['question-2'] = '13'
        self.portal.quiz.adapter.onSuccess(self.portal.quiz.values(), self.request)
        messages = IStatusMessage(self.request).show()
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, 'Your score is: 50%')


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)