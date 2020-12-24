# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zupo/work/osha.quizzes/src/osha/quizzes/tests/test_quizzes_view.py
# Compiled at: 2012-10-18 11:02:24
"""Test @@todo BrowserView."""
from osha.quizzes.tests.base import IntegrationTestCase
from DateTime import DateTime
from plone import api
import unittest2 as unittest

class TestView(IntegrationTestCase):
    """Test the @@quizzes BrowserView."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.folder = self.portal.folder
        self.folder.setLayout('quizzes')
        self.view = api.content.get_view(name='quizzes', context=self.folder, request=self.request)

    def test_no_quizzes(self):
        """Test HTML output when there are no Quizzes in a folder."""
        output = self.view()
        self.assertIn('No quizzes found', output)
        self.assertNotIn('<table class="listing"', output)

    def test_listing_table(self):
        """Test HTML listing table output."""
        api.content.create(container=self.folder, type='FormFolder', title='Ein Über Quiz', description='An advanced and difficult quiz.', comments='The quiz is not recommended for beginners.')
        date = DateTime('2012/10/18')
        self.folder['ein-uber-quiz'].setModificationDate(date)
        self.folder['ein-uber-quiz'].reindexObject(idxs=['modified'])
        output = self.view()
        self.assertNotIn('No quizzes found', output)
        self.assertIn('class="quiz-link"', output)
        self.assertIn('href="http://nohost/plone/folder/ein-uber-quiz"', output)
        self.assertIn('>Ein Über Quiz</a>', output)
        self.assertIn('<td>Oct 18, 2012 12:00 AM</td>', output)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)