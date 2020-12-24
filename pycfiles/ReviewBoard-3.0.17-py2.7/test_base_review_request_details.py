# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/tests/test_base_review_request_details.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for BaseReviewRequestDetails."""
from __future__ import unicode_literals
from django.contrib.auth.models import User
from reviewboard.reviews.models import DefaultReviewer
from reviewboard.testing import TestCase

class BaseReviewRequestDetailsTests(TestCase):
    """Unit tests for BaseReviewRequestDetails."""
    fixtures = [
     b'test_scmtools']

    def test_add_default_reviewers_with_users(self):
        """Testing BaseReviewRequestDetails.add_default_reviewers with users"""
        user1 = User.objects.create_user(username=b'user1', email=b'user1@example.com')
        user2 = User.objects.create(username=b'user2', email=b'user2@example.com')
        user3 = User.objects.create(username=b'user3', email=b'user3@example.com', is_active=False)
        default_reviewer1 = DefaultReviewer.objects.create(name=b'Test 1', file_regex=b'.*')
        default_reviewer1.people.add(user1, user2, user3)
        review_request = self.create_review_request(create_repository=True, submitter=user1)
        diffset = self.create_diffset(review_request)
        self.create_filediff(diffset)
        with self.assertNumQueries(7):
            review_request.add_default_reviewers()
        self.assertEqual(list(review_request.target_people.all()), [
         user1, user2])
        self.assertEqual(list(review_request.target_groups.all()), [])

    def test_add_default_reviewers_with_groups(self):
        """Testing BaseReviewRequestDetails.add_default_reviewers with groups
        """
        user1 = User.objects.create_user(username=b'user1', email=b'user1@example.com')
        group1 = self.create_review_group(name=b'Group 1')
        group2 = self.create_review_group(name=b'Group 2')
        default_reviewer1 = DefaultReviewer.objects.create(name=b'Test 1', file_regex=b'.*')
        default_reviewer1.groups.add(group1, group2)
        review_request = self.create_review_request(create_repository=True, submitter=user1)
        diffset = self.create_diffset(review_request)
        self.create_filediff(diffset)
        with self.assertNumQueries(7):
            review_request.add_default_reviewers()
        self.assertEqual(list(review_request.target_groups.all()), [
         group1, group2])
        self.assertEqual(list(review_request.target_people.all()), [])

    def test_add_default_reviewers_with_users_and_groups(self):
        """Testing BaseReviewRequestDetails.add_default_reviewers with both
        users and groups
        """
        user1 = User.objects.create_user(username=b'user1', email=b'user1@example.com')
        user2 = User.objects.create(username=b'user2', email=b'user2@example.com')
        group1 = self.create_review_group(name=b'Group 1')
        group2 = self.create_review_group(name=b'Group 2')
        default_reviewer1 = DefaultReviewer.objects.create(name=b'Test 1', file_regex=b'.*')
        default_reviewer1.people.add(user1, user2)
        default_reviewer2 = DefaultReviewer.objects.create(name=b'Test 2', file_regex=b'.*')
        default_reviewer2.groups.add(group1, group2)
        review_request = self.create_review_request(create_repository=True, submitter=user1)
        diffset = self.create_diffset(review_request)
        self.create_filediff(diffset)
        with self.assertNumQueries(9):
            review_request.add_default_reviewers()
        self.assertEqual(list(review_request.target_people.all()), [
         user1, user2])
        self.assertEqual(list(review_request.target_groups.all()), [
         group1, group2])

    def test_add_default_reviewers_with_no_matches(self):
        """Testing BaseReviewRequestDetails.add_default_reviewers with no
        matches
        """
        user1 = User.objects.create_user(username=b'user1', email=b'user1@example.com')
        user2 = User.objects.create(username=b'user2', email=b'user2@example.com')
        group1 = self.create_review_group(name=b'Group 1')
        group2 = self.create_review_group(name=b'Group 2')
        default_reviewer1 = DefaultReviewer.objects.create(name=b'Test 1', file_regex=b'/foo')
        default_reviewer1.people.add(user1, user2)
        default_reviewer2 = DefaultReviewer.objects.create(name=b'Test 2', file_regex=b'/bar')
        default_reviewer2.groups.add(group1, group2)
        review_request = self.create_review_request(create_repository=True, submitter=user1)
        diffset = self.create_diffset(review_request)
        self.create_filediff(diffset)
        with self.assertNumQueries(3):
            review_request.add_default_reviewers()
        self.assertEqual(list(review_request.target_people.all()), [])
        self.assertEqual(list(review_request.target_groups.all()), [])

    def test_add_default_reviewers_with_no_repository(self):
        """Testing BaseReviewRequestDetails.add_default_reviewers with no
        repository
        """
        user1 = User.objects.create_user(username=b'user1', email=b'user1@example.com')
        review_request = self.create_review_request(submitter=user1)
        with self.assertNumQueries(0):
            review_request.add_default_reviewers()