# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/tests/test_gitorious.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for the Gitorious hosting service."""
from __future__ import unicode_literals
from reviewboard.hostingsvcs.tests.testcases import ServiceTests

class GitoriousTests(ServiceTests):
    """Unit tests for the Gitorious hosting service."""
    service_name = b'gitorious'

    def test_service_support(self):
        """Testing Gitorious service support capabilities"""
        self.assertFalse(self.service_class.supports_bug_trackers)
        self.assertTrue(self.service_class.supports_repositories)
        self.assertTrue(self.service_class.self_hosted)

    def test_get_repository_fields(self):
        """Testing Gitorious.get_repository_fields"""
        self.assertEqual(self.get_repository_fields(b'Git', fields={b'gitorious_project_name': b'myproj', 
           b'gitorious_repo_name': b'myrepo'}), {b'path': b'git://example.com/myproj/myrepo.git', 
           b'mirror_path': b'https://example.com/myproj/myrepo.git', 
           b'raw_file_url': b'https://example.com/myproj/myrepo/blobs/raw/<revision>'})