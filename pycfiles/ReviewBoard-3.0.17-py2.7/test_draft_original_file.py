# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_draft_original_file.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.utils import six
from djblets.webapi.errors import DOES_NOT_EXIST, PERMISSION_DENIED
from reviewboard.scmtools.core import PRE_CREATION
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import original_file_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass
from reviewboard.webapi.tests.urls import get_draft_original_file_url

@six.add_metaclass(BasicTestsMetaclass)
class ResourceTests(BaseWebAPITestCase):
    """Testing the DraftOriginalFileResource APIs."""
    fixtures = [
     b'test_users', b'test_scmtools']
    sample_api_url = b'review-requests/<id>/draft/diffs/<id>/files/<id>/original-file/'
    resource = resources.draft_original_file
    basic_get_returns_json = False

    def setup_http_not_allowed_list_test(self, user):
        repository = self.create_repository(tool_name=b'Test')
        review_request = self.create_review_request(repository=repository, submitter=user, publish=True)
        diffset = self.create_diffset(review_request, draft=True)
        filediff = self.create_filediff(diffset)
        return get_draft_original_file_url(review_request, diffset, filediff)

    setup_http_not_allowed_item_test = setup_http_not_allowed_list_test

    def compare_item(self, data, filediff):
        self.assertEqual(data, b'Hello, world!\n')

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        repository = self.create_repository(tool_name=b'Test')
        review_request = self.create_review_request(repository=repository, with_local_site=with_local_site, submitter=user, publish=True)
        diffset = self.create_diffset(review_request, draft=True)
        filediff = self.create_filediff(diffset)
        return (
         get_draft_original_file_url(review_request, diffset, filediff, local_site_name=local_site_name),
         original_file_mimetype,
         filediff)

    def test_get_not_owner(self):
        """Testing the
        GET review-requests/<id>/draft/diffs/<id>/files/<id>/original-file/ API
        without owner
        """
        user = User.objects.get(username=b'doc')
        self.assertNotEqual(user, self.user)
        url, mimetype, item = self.setup_basic_get_test(user, False, None)
        rsp = self.api_get(url, expected_status=403)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], PERMISSION_DENIED.code)
        return

    def test_with_new_file(self):
        """Testing the
        GET review-requests/<id>/draft/diffs/<id>/files/<id>/original-file/ API
        with new file
        """
        repository = self.create_repository(tool_name=b'Test')
        review_request = self.create_review_request(repository=repository, submitter=self.user, publish=True)
        diffset = self.create_diffset(review_request, draft=True)
        filediff = self.create_filediff(diffset, source_revision=PRE_CREATION)
        rsp = self.api_get(get_draft_original_file_url(review_request, diffset, filediff), expected_status=404)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], DOES_NOT_EXIST.code)

    def test_without_draft_diff(self):
        """Testing the
        GET review-requests/<id>/draft/diffs/<id>/files/<id>/original-file/ API
        without draft diff
        """
        repository = self.create_repository(tool_name=b'Test')
        review_request = self.create_review_request(repository=repository, submitter=self.user, publish=True)
        diffset = self.create_diffset(review_request)
        filediff = self.create_filediff(diffset)
        rsp = self.api_get(get_draft_original_file_url(review_request, diffset, filediff), expected_status=404)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], DOES_NOT_EXIST.code)