# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_repository_commits.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.utils import six
from djblets.testing.decorators import add_fixtures
from reviewboard.webapi.resources import resources
from reviewboard.webapi.errors import REPO_NOT_IMPLEMENTED
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import repository_commits_item_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass
from reviewboard.webapi.tests.urls import get_repository_commits_url
import nose

@six.add_metaclass(BasicTestsMetaclass)
class ResourceTests(BaseWebAPITestCase):
    """Testing the RepositoryCommitsResource APIs."""
    fixtures = [
     b'test_users', b'test_scmtools']
    sample_api_url = b'repositories/<id>/commits/'
    resource = resources.repository_commits
    test_http_methods = ('DELETE', 'POST', 'PUT')

    def setup_http_not_allowed_list_test(self, user):
        repository = self.create_repository(tool_name=b'Test')
        return get_repository_commits_url(repository)

    def setup_http_not_allowed_item_test(self, user):
        repository = self.create_repository(tool_name=b'Test')
        return get_repository_commits_url(repository)

    def test_get(self):
        """Testing the GET repositories/<id>/commits/ API"""
        repository = self.create_repository(tool_name=b'Test')
        rsp = self.api_get(get_repository_commits_url(repository), query={b'start': 5}, expected_mimetype=repository_commits_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(len(rsp[b'commits']), 5)
        self.assertEqual(rsp[b'commits'][0][b'message'], b'Commit 5')
        self.assertEqual(rsp[b'commits'][3][b'author_name'], b'user2')

    @add_fixtures([b'test_site'])
    def test_get_with_site(self):
        """Testing the GET repositories/<id>/commits/ API with a local site"""
        self._login_user(local_site=True)
        repository = self.create_repository(with_local_site=True, tool_name=b'Test')
        rsp = self.api_get(get_repository_commits_url(repository, self.local_site_name), query={b'start': 7}, expected_mimetype=repository_commits_item_mimetype)
        self.assertEqual(len(rsp[b'commits']), 7)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'commits'][0][b'id'], b'7')
        self.assertEqual(rsp[b'commits'][1][b'message'], b'Commit 6')

    @add_fixtures([b'test_site'])
    def test_get_with_site_no_access(self):
        """Testing the GET repositories/<id>/commits/ API
        with a local site and Permission Denied error
        """
        repository = self.create_repository(with_local_site=True)
        self.api_get(get_repository_commits_url(repository, self.local_site_name), expected_status=403)

    def test_get_with_no_support(self):
        """Testing the GET repositories/<id>/commits/ API
        with a repository that does not implement it
        """
        repository = self.create_repository(tool_name=b'CVS')
        repository.save()
        try:
            rsp = self.api_get(get_repository_commits_url(repository), query={b'start': b''}, expected_status=501)
        except ImportError:
            raise nose.SkipTest(b'cvs binary not found')

        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], REPO_NOT_IMPLEMENTED.code)