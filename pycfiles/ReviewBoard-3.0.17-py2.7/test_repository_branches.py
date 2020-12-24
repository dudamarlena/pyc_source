# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_repository_branches.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.utils import six
from reviewboard.webapi.errors import REPO_NOT_IMPLEMENTED
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import repository_branches_item_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass
from reviewboard.webapi.tests.urls import get_repository_branches_url
import nose

@six.add_metaclass(BasicTestsMetaclass)
class ResourceTests(BaseWebAPITestCase):
    """Testing the RepositoryBranchesResource list APIs."""
    fixtures = [
     b'test_users', b'test_scmtools']
    sample_api_url = b'repositories/<id>/branches/'
    resource = resources.repository_branches

    def setup_http_not_allowed_list_test(self, user):
        repository = self.create_repository(tool_name=b'Test')
        return get_repository_branches_url(repository)

    def setup_http_not_allowed_item_test(self, user):
        repository = self.create_repository(tool_name=b'Test')
        return get_repository_branches_url(repository)

    def compare_item(self, item_rsp, branch):
        self.assertEqual(item_rsp, branch)

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        repository = self.create_repository(tool_name=b'Test', with_local_site=with_local_site)
        return (
         get_repository_branches_url(repository, local_site_name),
         repository_branches_item_mimetype,
         [
          {b'id': b'trunk', 
             b'name': b'trunk', 
             b'commit': b'5', 
             b'default': True},
          {b'id': b'branch1', 
             b'name': b'branch1', 
             b'commit': b'7', 
             b'default': False}])

    def test_get_with_no_support(self):
        """Testing the GET repositories/<id>/branches/ API
        with a repository that does not implement it
        """
        repository = self.create_repository(tool_name=b'CVS')
        try:
            rsp = self.api_get(get_repository_branches_url(repository), expected_status=501)
        except ImportError:
            raise nose.SkipTest(b'cvs binary not found')

        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], REPO_NOT_IMPLEMENTED.code)