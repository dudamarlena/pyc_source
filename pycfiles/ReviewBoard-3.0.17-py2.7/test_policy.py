# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/scmtools/tests/test_policy.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import os
from django.contrib.auth.models import AnonymousUser, User
from reviewboard.reviews.models import Group
from reviewboard.scmtools.forms import RepositoryForm
from reviewboard.scmtools.models import Repository, Tool
from reviewboard.site.models import LocalSite
from reviewboard.testing.testcase import TestCase

class PolicyTests(TestCase):
    """Unit tests for access policies."""
    fixtures = [
     b'test_scmtools']

    def setUp(self):
        self.user = User.objects.create_user(username=b'testuser', password=b'', email=b'user@example.com')
        self.anonymous = AnonymousUser()
        self.repo = Repository.objects.create(name=b'test', path=b'example.com:/cvsroot/test', username=b'anonymous', tool=Tool.objects.get(name=b'CVS'))

    def test_repository_public(self):
        """Testing access to a public repository"""
        self.assertTrue(self.repo.is_accessible_by(self.user))
        self.assertTrue(self.repo.is_accessible_by(self.anonymous))
        self.assertIn(self.repo, Repository.objects.accessible(self.user))
        self.assertTrue(self.repo in Repository.objects.accessible(self.anonymous))

    def test_repository_private_access_denied(self):
        """Testing no access to an inaccessible private repository"""
        self.repo.public = False
        self.repo.save()
        self.assertFalse(self.repo.is_accessible_by(self.user))
        self.assertFalse(self.repo.is_accessible_by(self.anonymous))
        self.assertNotIn(self.repo, Repository.objects.accessible(self.user))
        self.assertFalse(self.repo in Repository.objects.accessible(self.anonymous))

    def test_repository_private_access_allowed_by_user(self):
        """Testing access to a private repository accessible by user"""
        self.repo.users.add(self.user)
        self.repo.public = False
        self.repo.save()
        self.assertTrue(self.repo.is_accessible_by(self.user))
        self.assertFalse(self.repo.is_accessible_by(self.anonymous))
        self.assertIn(self.repo, Repository.objects.accessible(self.user))
        self.assertFalse(self.repo in Repository.objects.accessible(self.anonymous))

    def test_repository_private_access_allowed_by_review_group(self):
        """Testing access to a private repository accessible by review group"""
        group = Group.objects.create(name=b'test-group')
        group.users.add(self.user)
        self.repo.public = False
        self.repo.review_groups.add(group)
        self.repo.save()
        self.assertTrue(self.repo.is_accessible_by(self.user))
        self.assertFalse(self.repo.is_accessible_by(self.anonymous))
        self.assertIn(self.repo, Repository.objects.accessible(self.user))
        self.assertFalse(self.repo in Repository.objects.accessible(self.anonymous))

    def test_repository_form_with_local_site_and_bad_group(self):
        """Testing adding a Group to a RepositoryForm with the wrong LocalSite
        """
        test_site = LocalSite.objects.create(name=b'test')
        tool = Tool.objects.get(name=b'Subversion')
        group = Group.objects.create(name=b'test-group')
        svn_repo_path = b'file://' + os.path.join(os.path.dirname(__file__), b'..', b'testdata', b'svn_repo')
        form = RepositoryForm({b'name': b'test', 
           b'path': svn_repo_path, 
           b'hosting_type': b'custom', 
           b'bug_tracker_type': b'custom', 
           b'review_groups': [
                            group.pk], 
           b'local_site': test_site.pk, 
           b'tool': tool.pk})
        self.assertFalse(form.is_valid())
        group.local_site = test_site
        group.save()
        form = RepositoryForm({b'name': b'test', 
           b'path': svn_repo_path, 
           b'hosting_type': b'custom', 
           b'bug_tracker_type': b'custom', 
           b'review_groups': [
                            group.pk], 
           b'tool': tool.pk})
        self.assertFalse(form.is_valid())

    def test_repository_form_with_local_site_and_bad_user(self):
        """Testing adding a User to a RepositoryForm with the wrong LocalSite
        """
        test_site = LocalSite.objects.create(name=b'test')
        tool = Tool.objects.get(name=b'Subversion')
        svn_repo_path = b'file://' + os.path.join(os.path.dirname(__file__), b'..', b'testdata', b'svn_repo')
        form = RepositoryForm({b'name': b'test', 
           b'path': svn_repo_path, 
           b'hosting_type': b'custom', 
           b'bug_tracker_type': b'custom', 
           b'users': [
                    self.user.pk], 
           b'local_site': test_site.pk, 
           b'tool': tool.pk})
        self.assertFalse(form.is_valid())