# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/extension/tests/test_can_post_hook.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
import json
from django.contrib.auth.models import User
from django.utils.six.moves.urllib.request import OpenerDirector, build_opener
from kgb import SpyAgency
from reviewboard.admin.siteconfig import load_site_config
from reviewboard.hostingsvcs.models import HostingServiceAccount
from reviewboard.reviews.models import ReviewRequest
from reviewboard.scmtools.models import Repository, Tool
from rbpowerpack.extension.hooks import CannotPostReviewRequestError
from rbpowerpack.testing.testcases import PowerPackExtensionTestCase

class CanPostReviewRequestHookTests(SpyAgency, PowerPackExtensionTestCase):
    """Unit tests for CanPostReviewRequestHook."""
    fixtures = [
     b'test_scmtools']

    def setUp(self):
        super(CanPostReviewRequestHookTests, self).setUp()
        load_site_config()
        self.user = User.objects.create_user(username=b'test123', password=b'test123')

    def test_api_create_github_enterprise_valid(self):
        """Testing HostingServiceCanPostHook with API review request creation,
        GitHub Enterprise, and licensed user
        """
        hosting_account = self._get_github_enterprise_account()
        repository = self._create_git_repository(hosting_account)
        self.extension.license_settings.add_licensed_users([self.user])
        status_code, rsp = self._api_post(repository)
        self.assertEqual(status_code, 201)
        self.assertIn(b'review_request', rsp)

    def test_api_create_github_enterprise_unlicensed(self):
        """Testing HostingServiceCanPostHook with API review request creation,
        GitHub Enterprise, and unlicensed user
        """
        hosting_account = self._get_github_enterprise_account()
        repository = self._create_git_repository(hosting_account)
        status_code, rsp = self._api_post(repository)
        self.assertEqual(status_code, 403)
        self.assertEqual(rsp[b'err'][b'msg'], b'You are not licensed to post review requests against GitHub Enterprise repositories. Please contact your system administrator.')

    def test_review_request_create_github_enterprise_valid(self):
        """Testing HostingServiceCanPostHook with review request creation,
        GitHub Enterprise, and licensed user
        """
        hosting_account = self._get_github_enterprise_account()
        self.spy_on(hosting_account.service.can_user_post)
        repository = self._create_git_repository(hosting_account)
        self.extension.license_settings.add_licensed_users([self.user])
        review_request = ReviewRequest.objects.create(self.user, repository)
        self.assertIsNotNone(review_request)
        self.assertTrue(hosting_account.service.can_user_post.called)

    def test_review_request_create_github_enterprise_unlicensed(self):
        """Testing HostingServiceCanPostHook with review request creation,
        GitHub Enterprise, and unlicensed user
        """
        hosting_account = self._get_github_enterprise_account()
        self.spy_on(hosting_account.service.can_user_post)
        repository = self._create_git_repository(hosting_account)
        self.assertRaisesMessage(CannotPostReviewRequestError, b'You are not licensed to post review requests against GitHub Enterprise repositories. Please contact your system administrator.', lambda : ReviewRequest.objects.create(self.user, repository))
        self.assertTrue(hosting_account.service.can_user_post.called)

    def test_api_create_tfs_valid(self):
        """Testing HostingServiceCanPostHook with API review request creation,
        TFS, and licensed user
        """
        repository = self._create_tfs_repository()
        self.extension.license_settings.add_licensed_users([self.user])
        status_code, rsp = self._api_post(repository)
        self.assertEqual(status_code, 201)
        self.assertIn(b'review_request', rsp)

    def test_api_create_tfs_unlicensed(self):
        """Testing HostingServiceCanPostHook with API review request creation,
        TFS, and unlicensed user
        """
        repository = self._create_tfs_repository()
        status_code, rsp = self._api_post(repository)
        self.assertEqual(status_code, 403)
        self.assertEqual(rsp[b'err'][b'msg'], b'You are not licensed to post review requests against Team Foundation Server repositories. Please contact your system administrator.')

    def test_review_request_create_tfs_valid(self):
        """Testing HostingServiceCanPostHook with review request creation,
        TFS, and licensed user
        """
        repository = self._create_tfs_repository()
        scmtool = repository.get_scmtool()
        self.spy_on(scmtool.can_user_post)
        self.spy_on(repository.get_scmtool, call_fake=lambda self: scmtool)
        self.extension.license_settings.add_licensed_users([self.user])
        review_request = ReviewRequest.objects.create(self.user, repository)
        self.assertIsNotNone(review_request)
        self.assertTrue(scmtool.can_user_post.called)

    def test_review_request_create_tfs_unlicensed(self):
        """Testing HostingServiceCanPostHook with review request creation,
        TFS, and unlicensed user
        """
        repository = self._create_tfs_repository()
        scmtool = repository.get_scmtool()
        self.spy_on(scmtool.can_user_post)
        self.spy_on(repository.get_scmtool, call_fake=lambda self: scmtool)
        self.assertRaisesMessage(CannotPostReviewRequestError, b'You are not licensed to post review requests against Team Foundation Server repositories. Please contact your system administrator.', lambda : ReviewRequest.objects.create(self.user, repository))
        self.assertTrue(scmtool.can_user_post.called)

    def test_api_create_tfs_git_valid(self):
        """Testing HostingServiceCanPostHook with API review request creation,
        TFS-Git, and licensed user
        """
        repository = self._create_tfs_git_repository()
        self.extension.license_settings.add_licensed_users([self.user])
        status_code, rsp = self._api_post(repository)
        self.assertEqual(status_code, 201)
        self.assertIn(b'review_request', rsp)

    def test_api_create_tfs_git_git_unlicensed(self):
        """Testing HostingServiceCanPostHook with API review request creation,
        TFS-Git, and unlicensed user
        """
        repository = self._create_tfs_git_repository()
        status_code, rsp = self._api_post(repository)
        self.assertEqual(status_code, 403)
        self.assertEqual(rsp[b'err'][b'msg'], b'You are not licensed to post review requests against Team Foundation Server (git) repositories. Please contact your system administrator.')

    def test_review_request_create_tfs_git_git_valid(self):
        """Testing HostingServiceCanPostHook with review request creation,
        TFS-Git, and licensed user
        """
        repository = self._create_tfs_git_repository()
        scmtool = repository.get_scmtool()
        self.spy_on(scmtool.can_user_post)
        self.spy_on(repository.get_scmtool, call_fake=lambda self: scmtool)
        self.extension.license_settings.add_licensed_users([self.user])
        review_request = ReviewRequest.objects.create(self.user, repository)
        self.assertIsNotNone(review_request)
        self.assertTrue(scmtool.can_user_post.called)

    def test_review_request_create_tfs_git_git_unlicensed(self):
        """Testing HostingServiceCanPostHook with review request creation,
        TFS-Git, and unlicensed user
        """
        repository = self._create_tfs_git_repository()
        scmtool = repository.get_scmtool()
        self.spy_on(scmtool.can_user_post)
        self.spy_on(repository.get_scmtool, call_fake=lambda self: scmtool)
        self.assertRaisesMessage(CannotPostReviewRequestError, b'You are not licensed to post review requests against Team Foundation Server (git) repositories. Please contact your system administrator.', lambda : ReviewRequest.objects.create(self.user, repository))
        self.assertTrue(scmtool.can_user_post.called)

    def test_review_request_create_service_not_powerpack(self):
        """Testing HostingServiceCanPostHook with review request creation
        with non-Power Pack hosting service
        """
        hosting_account = self._get_github_account()
        repository = self._create_git_repository(hosting_account)
        review_request = ReviewRequest.objects.create(self.user, repository)
        self.assertIsNotNone(review_request)

    def test_review_request_create_plain_repo(self):
        """Testing HostingServiceCanPostHook with review request creation
        with plain repository
        """
        repository = self._create_git_repository(None)
        review_request = ReviewRequest.objects.create(self.user, repository)
        self.assertIsNotNone(review_request)
        return

    def test_review_request_create_after_shutdown(self):
        """Testing HostingServiceCanPostHook with review request creation
        after shutdown
        """
        hosting_account = self._get_github_enterprise_account()
        self.spy_on(hosting_account.service.can_user_post)
        repository = self._create_git_repository(hosting_account)
        self.extension.shutdown()
        review_request = ReviewRequest.objects.create(self.user, repository)
        self.assertIsNotNone(review_request)
        self.assertFalse(hosting_account.service.can_user_post.called)

    def _create_git_repository(self, hosting_account):
        return Repository.objects.create(name=b'Test', path=b'git@github.example.com', tool=Tool.objects.get(name=b'Git'), hosting_account=hosting_account)

    def _create_tfs_repository(self):
        return Repository.objects.create(name=b'Test', path=b'http://tfs:8080/tfs/DefaultCollection/', tool=Tool.objects.get(name=b'Team Foundation Server'))

    def _create_tfs_git_repository(self):

        class Opener(OpenerDirector):

            def open(s, url):
                self.assertEqual(url, path + b'_apis/git/repositories?api-version=1.0')

                class Response(object):
                    code = 200
                    headers = {}

                    def read(self):
                        return b'{  "count": 0,  "value": []}'

                return Response()

        self.spy_on(build_opener, call_fake=lambda *args: Opener())
        path = b'http://tfs:8080/tfs/DefaultCollection/'
        repo = Repository.objects.create(name=b'Test', path=path + b'_git/', tool=Tool.objects.get(name=b'Team Foundation Server (git)'))
        self.assertFalse(build_opener.spy.called)
        return repo

    def _get_github_enterprise_account(self):
        return HostingServiceAccount.objects.create(service_name=b'github-enterprise', hosting_url=b'https://github.example.com', username=b'test-user')

    def _get_github_account(self):
        return HostingServiceAccount.objects.create(service_name=b'github', username=b'test-user')

    def _api_post(self, repository):
        username = self.user.username
        self.assertTrue(self.client.login(username=username, password=username))
        rsp = self.client.post(b'/api/review-requests/', {b'repository': repository.pk})
        return (
         rsp.status_code, json.loads(rsp.content))