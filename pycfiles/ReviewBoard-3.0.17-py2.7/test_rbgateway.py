# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/tests/test_rbgateway.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for the ReviewBoardGateway hosting service."""
from __future__ import unicode_literals
import hashlib, hmac, logging
from djblets.testing.decorators import add_fixtures
from reviewboard.hostingsvcs.testing import HostingServiceTestCase
from reviewboard.reviews.models import ReviewRequest
from reviewboard.scmtools.core import Branch, Commit
from reviewboard.scmtools.crypto_utils import encrypt_password
from reviewboard.site.models import LocalSite
from reviewboard.site.urlresolvers import local_site_reverse

class ReviewBoardGatewayTestCase(HostingServiceTestCase):
    """Base test case for the ReviewBoardGateway hosting service."""
    service_name = b'rbgateway'
    default_use_hosting_url = True
    default_account_data = {b'private_token': encrypt_password(b'abc123')}
    default_repository_extra_data = {b'rbgateway_repo_name': b'myrepo'}


class ReviewBoardGatewayTests(ReviewBoardGatewayTestCase):
    """Unit tests for the ReviewBoardGateway hosting service."""

    def test_service_support(self):
        """Testing ReviewBoardGateway service support capabilities"""
        self.assertTrue(self.service_class.supports_repositories)
        self.assertTrue(self.service_class.supports_post_commit)
        self.assertFalse(self.service_class.supports_bug_trackers)
        self.assertFalse(self.service_class.supports_ssh_key_association)

    def test_repo_field_values(self):
        """Testing ReviewBoardGateway.get_repository_fields for Git"""
        self.assertEqual(self.get_repository_fields(b'Git', fields={b'hosting_url': b'https://example.com', 
           b'rbgateway_repo_name': b'myrepo'}), {b'path': b'https://example.com/repos/myrepo/path'})

    def test_authorize(self):
        """Testing ReviewBoardGateway.authorize"""
        hosting_account = self.create_hosting_account(data={})
        self.assertFalse(hosting_account.is_authorized)
        with self.setup_http_test(payload=b'{"private_token": "abc123"}', hosting_account=hosting_account, expected_http_calls=1) as (ctx):
            ctx.service.authorize(username=b'myuser', password=b'mypass', hosting_url=b'https://example.com')
        self.assertTrue(hosting_account.is_authorized)
        ctx.assertHTTPCall(0, url=b'https://example.com/session', method=b'POST', body=b'', headers={b'Content-Length': b'0'})

    def test_check_repository(self):
        """Testing ReviewBoardGateway.check_repository"""
        with self.setup_http_test(payload=b'{}', expected_http_calls=1) as (ctx):
            ctx.service.check_repository(path=b'https://example.com/repos/myrepo/path')
        ctx.assertHTTPCall(0, url=b'https://example.com/repos/myrepo/path', username=None, password=None, headers={b'PRIVATE-TOKEN': b'abc123'})
        return

    def test_get_branches_git(self):
        """Testing ReviewBoardGateway.get_branches for a Git repository"""
        payload = self.dump_json([
         {b'name': b'master', 
            b'id': b'c272edcac05b00e15440d6274723b639e3acbd7c'},
         {b'name': b'im_a_branch', 
            b'id': b'83904e6acb60e7ec0dcaae6c09a579ab44d0cf38'}])
        with self.setup_http_test(payload=payload, expected_http_calls=1) as (ctx):
            repository = ctx.create_repository()
            branches = ctx.service.get_branches(repository)
        ctx.assertHTTPCall(0, url=b'https://example.com/repos/myrepo/branches', username=None, password=None, headers={b'PRIVATE-TOKEN': b'abc123'})
        self.assertEqual(branches, [
         Branch(id=b'master', commit=b'c272edcac05b00e15440d6274723b639e3acbd7c', default=True),
         Branch(id=b'im_a_branch', commit=b'83904e6acb60e7ec0dcaae6c09a579ab44d0cf38')])
        return

    def test_get_branches_hg(self):
        """Testing ReviewBoardGateway.get_branches for an Hg repository"""
        payload = self.dump_json([
         {b'name': b'default', 
            b'id': b'9b1153b8a8eb2f7b1661ed7695c432f5a2b25729'},
         {b'name': b'some-bookmark', 
            b'id': b'0731875ed7a14bdd53503b27b30a08a0452068cf'}])
        with self.setup_http_test(payload=payload, expected_http_calls=1) as (ctx):
            repository = ctx.create_repository(tool_name=b'Mercurial')
            branches = ctx.service.get_branches(repository)
        ctx.assertHTTPCall(0, url=b'https://example.com/repos/myrepo/branches', username=None, password=None, headers={b'PRIVATE-TOKEN': b'abc123'})
        self.assertEqual(branches, [
         Branch(id=b'default', commit=b'9b1153b8a8eb2f7b1661ed7695c432f5a2b25729', default=True),
         Branch(id=b'some-bookmark', commit=b'0731875ed7a14bdd53503b27b30a08a0452068cf')])
        return

    def test_get_commits(self):
        """Testing ReviewBoardGateway.get_commits"""
        payload = self.dump_json([
         {b'author': b'Author 1', 
            b'id': b'bfdde95432b3af879af969bd2377dc3e55ee46e6', 
            b'date': b'2015-02-13 22:34:01 -0700', 
            b'message': b'Message 1', 
            b'parent_id': b'304c53c163aedfd0c0e0933776f09c24b87f5944'},
         {b'author': b'Author 2', 
            b'id': b'304c53c163aedfd0c0e0933776f09c24b87f5944', 
            b'date': b'2015-02-13 22:32:42 -0700', 
            b'message': b'Message 2', 
            b'parent_id': b'fa1330719893098ae397356e8125c2aa45b49221'},
         {b'author': b'Author 3', 
            b'id': b'fa1330719893098ae397356e8125c2aa45b49221', 
            b'date': b'2015-02-12 16:01:48 -0700', 
            b'message': b'Message 3', 
            b'parent_id': b''}])
        with self.setup_http_test(payload=payload, expected_http_calls=1) as (ctx):
            repository = ctx.create_repository()
            commits = ctx.service.get_commits(repository=repository, branch=b'bfdde95432b3af879af969bd2377dc3e55ee46e6')
        ctx.assertHTTPCall(0, url=b'https://example.com/repos/myrepo/branches/bfdde95432b3af879af969bd2377dc3e55ee46e6/commits', username=None, password=None, headers={b'PRIVATE-TOKEN': b'abc123'})
        self.assertEqual(commits, [
         Commit(author_name=b'Author 1', date=b'2015-02-13 22:34:01 -0700', id=b'bfdde95432b3af879af969bd2377dc3e55ee46e6', message=b'Message 1', parent=b'304c53c163aedfd0c0e0933776f09c24b87f5944'),
         Commit(author_name=b'Author 2', date=b'2015-02-13 22:32:42 -0700', id=b'304c53c163aedfd0c0e0933776f09c24b87f5944', message=b'Message 2', parent=b'fa1330719893098ae397356e8125c2aa45b49221'),
         Commit(author_name=b'Author 3', date=b'2015-02-12 16:01:48 -0700', id=b'fa1330719893098ae397356e8125c2aa45b49221', message=b'Message 3', parent=b'')])
        for commit in commits:
            self.assertIsNone(commit.diff)

        return

    def test_get_change(self):
        """Testing ReviewBoardGateway.get_change"""
        diff = b'diff --git a/test b/test\nindex 9daeafb9864cf43055ae93beb0afd6c7d144bfa4..dced80a85fe1e8f13dd5ea19923e5d2e8680020d 100644\n--- a/test\n+++ b/test\n@@ -1 +1,3 @@\n test\n+\n+test\n'
        payload = self.dump_json({b'author': b'Some Author', 
           b'id': b'bfdde95432b3af879af969bd2377dc3e55ee46e6', 
           b'date': b'2015-02-13 22:34:01 -0700', 
           b'message': b'My Message', 
           b'parent_id': b'304c53c163aedfd0c0e0933776f09c24b87f5944', 
           b'diff': diff})
        with self.setup_http_test(payload=payload, expected_http_calls=1) as (ctx):
            repository = ctx.create_repository()
            change = ctx.service.get_change(repository=repository, revision=b'bfdde95432b3af879af969bd2377dc3e55ee46e6')
        ctx.assertHTTPCall(0, url=b'https://example.com/repos/myrepo/commits/bfdde95432b3af879af969bd2377dc3e55ee46e6', username=None, password=None, headers={b'PRIVATE-TOKEN': b'abc123'})
        self.assertEqual(change, Commit(author_name=b'Some Author', date=b'2015-02-13 22:34:01 -0700', id=b'bfdde95432b3af879af969bd2377dc3e55ee46e6', message=b'My Message', parent=b'304c53c163aedfd0c0e0933776f09c24b87f5944'))
        self.assertEqual(change.diff, diff.encode(b'utf-8'))
        return


class CloseSubmittedHookTests(ReviewBoardGatewayTestCase):
    """Unit tests for ReviewBoardGateway's close-submitted hook."""
    fixtures = [
     b'test_users', b'test_scmtools']

    def test_close_submitted_hook_git(self):
        """Testing the ReviewBoardGateway close-submitted hook with a Git
        repository
        """
        self._test_post_commit_hook(tool_name=b'Git')

    def test_close_submiteed_hook_git_unpublished(self):
        """Testing the ReviewBoardGateway close-submitted hook with an
        unpublished review request in a Git repository
        """
        self._test_post_commit_hook(tool_name=b'Git', publish=False)

    @add_fixtures([b'test_site'])
    def test_close_submiteed_hook_git_local_site_unpublished(self):
        """Testing the ReviewBoardGateway close-submitted hook with an
        unpublished review request in a Git repository on a Local Site
        """
        self._test_post_commit_hook(tool_name=b'Git', local_site=LocalSite.objects.get(name=self.local_site_name), publish=False)

    def test_close_submitted_hook_git_tag_target(self):
        """Testing the ReviewBoardGateway close-submitted hook with an
        Git repository and a tag target
        """
        self._test_post_commit_hook(tool_name=b'Git', expected_close_msg=b'Pushed to release-1.0.7 (bbbbbbb)', target_tags=[
         b'release-1.0.7', b'some-tag'])

    def test_close_submitted_hook_git_no_target(self):
        """Testing the ReviewBoardGateway close-submitted hook with an
        Git repository and no target information
        """
        self._test_post_commit_hook(tool_name=b'Git', expected_close_msg=b'Pushed to bbbbbbb', target_branch=None)
        return

    def test_close_submitted_hook_hg(self):
        """Testing the ReviewBoardGateway close-submitted hook with an
        Mercurial repository
        """
        self._test_post_commit_hook(tool_name=b'Mercurial')

    @add_fixtures([b'test_site'])
    def test_close_submitted_hook_hg_local_site(self):
        """Testing the ReviewBoardGateway close-submitted hook with an
        Mercurial repository on a Local Site
        """
        self._test_post_commit_hook(tool_name=b'Mercurial', local_site=LocalSite.objects.get(name=self.local_site_name))

    def test_close_submitted_hook_hg_unpublished(self):
        """Testing the ReviewBoardGateway close-submitted hook with an
        unpublished review request in a Mercurial repository
        """
        self._test_post_commit_hook(tool_name=b'Mercurial', publish=False)

    @add_fixtures([b'test_site'])
    def test_close_submitted_hook_hg_local_site_unpublished(self):
        """Testing the ReviewBoardGateway close-submitted hook with an
        unpublished review request in a Mercurial repository on a Local Site
        """
        self._test_post_commit_hook(tool_name=b'Mercurial', local_site=LocalSite.objects.get(name=self.local_site_name), publish=False)

    def test_close_submitted_hook_hg_bookmark_target(self):
        """Testing the ReviewBoardGateway close-submitted hook with an
        Mercurial repository and a bookmark target
        """
        self._test_post_commit_hook(tool_name=b'Mercurial', expected_close_msg=b'Pushed to dev-work (bbbbbbb)', target_bookmarks=[
         b'dev-work'])

    def test_close_submitted_hook_hg_tag_target(self):
        """Testing the ReviewBoardGateway close-submitted hook with an
        Mercurial repository and a tag target
        """
        self._test_post_commit_hook(tool_name=b'Mercurial', expected_close_msg=b'Pushed to @ (bbbbbbb)', target_branch=b'default', target_tags=[
         b'@', b'tip'])

    def test_close_submitted_hook_hg_no_target(self):
        """Testing the ReviewBoardGateway close-submitted hook with an
        Mercurial repository and no target information
        """
        self._test_post_commit_hook(tool_name=b'Mercurial', expected_close_msg=b'Pushed to bbbbbbb', target_branch=None)
        return

    def test_close_submitted_hook_invalid_signature(self):
        """Testing the ReviewBoardGateway close-submitted hook with an invalid
        signature
        """
        account = self.create_hosting_account()
        repository = self.create_repository(tool_name=b'Git', hosting_account=account)
        url = local_site_reverse(b'rbgateway-hooks-close-submitted', local_site=None, kwargs={b'repository_id': repository.pk, 
           b'hosting_service_id': b'rbgateway'})
        payload = self.dump_json({b'event': b'push', 
           b'commits': []})
        signature = hmac.new(b'this is not the secret key', payload, hashlib.sha1).hexdigest()
        rsp = self.client.post(url, payload, content_type=b'application/x-www-form-urlencoded', HTTP_X_RBG_SIGNATURE=signature, HTTP_X_RBG_EVENT=b'push')
        self.assertEqual(rsp.status_code, 400)
        self.assertEqual(rsp.content, b'Bad signature.')
        return

    def test_close_submitted_hook_malformed_payload(self):
        """Testing the ReviewBoardGateway close-submitted hook with a malformed
        signature
        """
        account = self.create_hosting_account()
        repository = self.create_repository(tool_name=b'Git', hosting_account=account)
        url = local_site_reverse(b'rbgateway-hooks-close-submitted', local_site=None, kwargs={b'repository_id': repository.pk, 
           b'hosting_service_id': b'rbgateway'})
        payload = b'event=push&commit_id=bbbbbbb&branch=master'
        signature = hmac.new(bytes(repository.get_or_create_hooks_uuid()), payload, hashlib.sha1).hexdigest()
        rsp = self.client.post(url, payload, content_type=b'application/x-www-form-urlencoded', HTTP_X_RBG_SIGNATURE=signature, HTTP_X_RBG_EVENT=b'push')
        self.assertEqual(rsp.status_code, 400)
        self.assertEqual(rsp.content, b'Invalid payload format.')
        return

    def test_close_submitted_hook_incomplete_payload(self):
        account = self.create_hosting_account()
        repository = self.create_repository(tool_name=b'Git', hosting_account=account)
        url = local_site_reverse(b'rbgateway-hooks-close-submitted', local_site=None, kwargs={b'repository_id': repository.pk, 
           b'hosting_service_id': b'rbgateway'})
        payload = self.dump_json({b'event': b'push'})
        signature = hmac.new(bytes(repository.get_or_create_hooks_uuid()), payload, hashlib.sha1).hexdigest()
        rsp = self.client.post(url, payload, content_type=b'application/json', HTTP_X_RBG_SIGNATURE=signature, HTTP_X_RBG_EVENT=b'push')
        self.assertEqual(rsp.status_code, 400)
        self.assertEqual(rsp.content, b'Invalid payload; expected "commits".')
        return

    def test_close_submitted_hook_invalid_event(self):
        """Testing the ReviewBoardGateway close-submitted hook endpoint with an
        invalid event
        """
        account = self.create_hosting_account()
        repository = self.create_repository(tool_name=b'Git', hosting_account=account)
        url = local_site_reverse(b'rbgateway-hooks-close-submitted', local_site=None, kwargs={b'repository_id': repository.pk, 
           b'hosting_service_id': b'rbgateway'})
        payload = self.dump_json({b'event': b'unknown-event', 
           b'repository': b'foo'})
        signature = hmac.new(bytes(repository.get_or_create_hooks_uuid()), payload, hashlib.sha1).hexdigest()
        rsp = self.client.post(url, payload, content_type=b'application/json', HTTP_X_RBG_SIGNATURE=signature, HTTP_X_RBG_EVENT=b'unknown-event')
        self.assertEqual(rsp.status_code, 400)
        self.assertEqual(rsp.content, b'Only "ping" and "push" events are supported.')
        return

    def test_close_submitted_hook_with_invalid_review_request(self):
        """Testing the ReviewBoardGateway close-submitted hook endpoint with an
        invalid review request
        """
        self.spy_on(logging.error)
        account = self.create_hosting_account()
        repository = self.create_repository(tool_name=b'Git', hosting_account=account)
        review_request = self.create_review_request(repository=repository, publish=True)
        url = local_site_reverse(b'rbgateway-hooks-close-submitted', local_site=None, kwargs={b'repository_id': repository.pk, 
           b'hosting_service_id': b'rbgateway'})
        response = self._post_commit_hook_payload(post_url=url, review_request_url=b'/r/9999/', repository_name=repository.name, secret=repository.get_or_create_hooks_uuid())
        self.assertEqual(response.status_code, 200)
        review_request = ReviewRequest.objects.get(pk=review_request.pk)
        self.assertTrue(review_request.public)
        self.assertEqual(review_request.status, review_request.PENDING_REVIEW)
        self.assertEqual(review_request.changedescs.count(), 0)
        self.assertTrue(logging.error.called_with(b'close_all_review_requests: Review request #%s does not exist.', 9999))
        return

    def test_ping_event(self):
        """Testing the ReviewBoardGateway close submitted hook endpoint with
        event=ping
        """
        account = self.create_hosting_account()
        repository = self.create_repository(tool_name=b'Git', hosting_account=account)
        url = local_site_reverse(b'rbgateway-hooks-close-submitted', local_site=None, kwargs={b'repository_id': repository.pk, 
           b'hosting_service_id': b'rbgateway'})
        payload = self.dump_json({b'event': b'ping', 
           b'repository': b'foo'})
        signature = hmac.new(bytes(repository.get_or_create_hooks_uuid()), payload, hashlib.sha1).hexdigest()
        rsp = self.client.post(url, payload, content_type=b'application/json', HTTP_X_RBG_SIGNATURE=signature, HTTP_X_RBG_EVENT=b'ping')
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(rsp.content, b'')
        return

    def _test_post_commit_hook(self, tool_name, local_site=None, publish=True, expected_close_msg=b'Pushed to master (bbbbbbb)', **kwargs):
        """Testing posting to a commit hook.

        This will simulate pushing a commit and posting the resulting webhook
        payload from RB Gateway to the handler for the hook.

        Args:
            tool_name (unicode):
                The name of the SCM tool to use.

            local_site (reviewboard.site.models.LocalSite, optional):
                The Local Site owning the review request.

            publish (bool):
                Whether or not to use a published review request.
        """
        account = self.create_hosting_account(local_site=local_site)
        repository = self.create_repository(tool_name=tool_name, hosting_account=account, local_site=local_site)
        review_request = self.create_review_request(repository=repository, local_site=local_site, publish=publish)
        self.assertEqual(review_request.status, review_request.PENDING_REVIEW)
        url = local_site_reverse(b'rbgateway-hooks-close-submitted', local_site=local_site, kwargs={b'repository_id': repository.pk, 
           b'hosting_service_id': b'rbgateway'})
        response = self._post_commit_hook_payload(post_url=url, review_request_url=review_request.get_absolute_url(), repository_name=repository.name, secret=repository.get_or_create_hooks_uuid(), **kwargs)
        self.assertEqual(response.status_code, 200)
        review_request = ReviewRequest.objects.get(pk=review_request.pk)
        self.assertTrue(review_request.public)
        self.assertEqual(review_request.status, review_request.SUBMITTED)
        self.assertEqual(review_request.changedescs.count(), 1)
        changedesc = review_request.changedescs.get()
        self.assertEqual(changedesc.text, expected_close_msg)

    def _post_commit_hook_payload(self, post_url, repository_name, review_request_url, secret, event=b'push', target_branch=b'master', target_bookmarks=None, target_tags=None):
        """Post a payload for a hook for testing.

        Args:
            post_url (unicode):
                The URL to post to.

            repository_name (unicode):
                The name of the repository.

            review_request_url (unicode):
                The URL of the review request being represented in the
                payload.

            secret (unicode):
                The HMAC secret for the message.

            event (unicode, optional):
                The webhook event.

            target_branch (unicode, optional):
                The target branch to include in the payload.

            target_bookmarks (unicode, optional):
                The target Mercurial bookmarks to include in the payload.

            target_tags (unicode, optional):
                The target tags to include in the payload.

        Results:
            django.core.handlers.wsgi.WSGIRequest:
            The post request.
        """
        target = {}
        if target_branch is not None:
            target[b'branch'] = target_branch
        if target_bookmarks is not None:
            target[b'bookmarks'] = target_bookmarks
        if target_tags is not None:
            target[b'tags'] = target_tags
        payload = self.dump_json({b'event': event, 
           b'repository': repository_name, 
           b'commits': [
                      {b'id': b'b' * 40, 
                         b'message': b'Commit message.\n\nReviewed at http://example.com%s' % review_request_url, 
                         b'target': target}]})
        signature = hmac.new(bytes(secret), payload, hashlib.sha1).hexdigest()
        return self.client.post(post_url, payload, content_type=b'application/json', HTTP_X_RBG_EVENT=event, HTTP_X_RBG_SIGNATURE=signature)