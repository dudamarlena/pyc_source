# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/tests/test_bugzilla.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for the Bugzilla hosting service."""
from __future__ import unicode_literals
from reviewboard.hostingsvcs.tests.testcases import ServiceTests

class BugzillaTests(ServiceTests):
    """Unit tests for the Bugzilla hosting service."""
    service_name = b'bugzilla'
    fixtures = [b'test_scmtools']

    def test_service_support(self):
        """Testing Bugzilla service support capabilities"""
        self.assertTrue(self.service_class.supports_bug_trackers)
        self.assertFalse(self.service_class.supports_repositories)

    def test_bug_tracker_field(self):
        """Testing Bugzilla.get_bug_tracker_field"""
        self.assertFalse(self.service_class.get_bug_tracker_requires_username())
        self.assertEqual(self.service_class.get_bug_tracker_field(None, {b'bugzilla_url': b'http://bugzilla.example.com'}), b'http://bugzilla.example.com/show_bug.cgi?id=%s')
        return