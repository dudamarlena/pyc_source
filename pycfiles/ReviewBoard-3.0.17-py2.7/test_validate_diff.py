# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_validate_diff.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import six
from djblets.testing.decorators import add_fixtures
from djblets.webapi.errors import INVALID_FORM_DATA
from djblets.webapi.testing.decorators import webapi_test_template
from kgb import SpyAgency
from reviewboard import scmtools
from reviewboard.diffviewer.models import DiffSet
from reviewboard.webapi.errors import DIFF_PARSE_ERROR, INVALID_REPOSITORY, REPO_FILE_NOT_FOUND
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import validate_diff_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass
from reviewboard.webapi.tests.urls import get_validate_diff_url

@six.add_metaclass(BasicTestsMetaclass)
class ResourceTests(SpyAgency, BaseWebAPITestCase):
    """Testing the ValidateDiffResource APIs."""
    fixtures = [
     b'test_users', b'test_scmtools']
    sample_api_url = b'validation/diffs/'
    test_http_methods = ('DELETE', 'PUT')
    resource = resources.validate_diff
    VALID_GIT_DIFF = b'diff --git a/readme b/readmeindex d6613f5..5b50866 100644--- a/readme+++ b/readme@@ -1 +1,3 @@ Hello there++Oh hi!'

    def setup_http_not_allowed_item_test(self, user):
        return get_validate_diff_url()

    def test_get(self):
        """Testing the GET validation/diffs/ API"""
        self.api_get(get_validate_diff_url(), expected_mimetype=validate_diff_mimetype)

    @add_fixtures([b'test_site'])
    def test_get_with_site(self):
        """Testing the GET validation/diffs/ API with access to local site"""
        self._login_user(local_site=True)
        self.api_get(get_validate_diff_url(self.local_site_name), expected_mimetype=validate_diff_mimetype)

    @add_fixtures([b'test_site'])
    def test_get_with_site_no_access(self):
        """Testing the GET validation/diffs/ API
        without access to local site
        """
        self.api_get(get_validate_diff_url(self.local_site_name), expected_status=403)

    def test_post(self):
        """Testing the POST validation/diffs/ API"""
        repository = self.create_repository(tool_name=b'Test')
        diff_filename = os.path.join(os.path.dirname(scmtools.__file__), b'testdata', b'git_readme.diff')
        f = open(diff_filename, b'r')
        self.api_post(get_validate_diff_url(), {b'repository': repository.pk, 
           b'path': f, 
           b'basedir': b'/trunk'}, expected_status=200, expected_mimetype=validate_diff_mimetype)
        f.close()

    @add_fixtures([b'test_site'])
    def test_post_with_site(self):
        """Testing the POST validation/diffs/ API
        with access to a local site
        """
        repository = self.create_repository(with_local_site=True, tool_name=b'Test')
        self._login_user(local_site=True)
        diff_filename = os.path.join(os.path.dirname(scmtools.__file__), b'testdata', b'git_readme.diff')
        with open(diff_filename, b'r') as (fp):
            self.api_post(get_validate_diff_url(self.local_site_name), {b'repository': repository.pk, 
               b'path': fp, 
               b'basedir': b'/trunk'}, expected_status=200, expected_mimetype=validate_diff_mimetype)

    @add_fixtures([b'test_site'])
    def test_post_with_site_no_access(self):
        """Testing the POST validation/diffs/ API
        without access to a local site
        """
        repository = self.create_repository(with_local_site=True, tool_name=b'Test')
        diff_filename = os.path.join(os.path.dirname(scmtools.__file__), b'testdata', b'git_readme.diff')
        with open(diff_filename, b'r') as (fp):
            self.api_post(get_validate_diff_url(self.local_site_name), {b'repository': repository.pk, 
               b'path': fp, 
               b'basedir': b'/trunk'}, expected_status=403)

    def test_post_with_base_commit_id(self):
        """Testing the POST validation/diffs/ API with base_commit_id"""
        self.spy_on(DiffSet.objects.create_from_upload, call_original=True)
        repository = self.create_repository(tool_name=b'Test')
        diff_filename = os.path.join(os.path.dirname(scmtools.__file__), b'testdata', b'git_readme.diff')
        f = open(diff_filename, b'r')
        self.api_post(get_validate_diff_url(), {b'repository': repository.pk, 
           b'path': f, 
           b'basedir': b'/trunk', 
           b'base_commit_id': b'1234'}, expected_status=200, expected_mimetype=validate_diff_mimetype)
        f.close()
        last_call = DiffSet.objects.create_from_upload.last_call
        self.assertEqual(last_call.kwargs.get(b'base_commit_id'), b'1234')

    def test_post_with_missing_basedir(self):
        """Testing the POST validations/diffs/ API with a missing basedir"""
        repository = self.create_repository(tool_name=b'Test')
        diff_filename = os.path.join(os.path.dirname(scmtools.__file__), b'testdata', b'git_readme.diff')
        f = open(diff_filename, b'r')
        rsp = self.api_post(get_validate_diff_url(), {b'repository': repository.pk, 
           b'path': f}, expected_status=400)
        f.close()
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], INVALID_FORM_DATA.code)
        self.assertIn(b'basedir', rsp[b'fields'])

    def test_post_with_files_not_found(self):
        """Testing the POST validation/diffs/ API
        with source files not found
        """
        repository = self.create_repository(tool_name=b'Test')
        diff_filename = os.path.join(os.path.dirname(scmtools.__file__), b'testdata', b'git_file_not_found.diff')
        f = open(diff_filename, b'r')
        rsp = self.api_post(get_validate_diff_url(), {b'repository': repository.pk, 
           b'path': f, 
           b'basedir': b''}, expected_status=400)
        f.close()
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], REPO_FILE_NOT_FOUND.code)
        self.assertEqual(rsp[b'file'], b'missing-file')
        self.assertEqual(rsp[b'revision'], b'd6613f0')

    def test_post_with_parse_error(self):
        """Testing the POST validation/diffs/ API with a malformed diff file"""
        repository = self.create_repository(tool_name=b'Test')
        diff_filename = os.path.join(os.path.dirname(scmtools.__file__), b'testdata', b'stunnel.pem')
        with open(diff_filename, b'rb') as (f):
            rsp = self.api_post(get_validate_diff_url(), {b'repository': repository.pk, 
               b'path': f, 
               b'basedir': b'/trunk'}, expected_status=400)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], DIFF_PARSE_ERROR.code)
        self.assertEqual(rsp[b'reason'], b'This does not appear to be a git diff')
        self.assertEqual(rsp[b'linenum'], 0)

    def test_post_with_conflicting_repos(self):
        """Testing the POST validations/diffs/ API with conflicting
        repositories
        """
        repository = self.create_repository(tool_name=b'Test')
        self.create_repository(tool_name=b'Test', name=b'Test 2', path=b'blah', mirror_path=repository.path)
        rsp = self.api_post(get_validate_diff_url(), {b'repository': repository.path, 
           b'path': SimpleUploadedFile(b'readme.diff', self.VALID_GIT_DIFF, content_type=b'text/x-patch'), 
           b'basedir': b'/trunk'}, expected_status=400)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], INVALID_REPOSITORY.code)
        self.assertEqual(rsp[b'err'][b'msg'], b'Too many repositories matched "%s". Try specifying the repository by name instead.' % repository.path)
        self.assertEqual(rsp[b'repository'], repository.path)

    @webapi_test_template
    def test_post_repository_private(self):
        """Testing the POST <URL> API without access to the requested
        repository
        """
        repository = self.create_repository(tool_name=b'Test', public=False)
        rsp = self.api_post(get_validate_diff_url(), {b'repository': repository.path, 
           b'path': SimpleUploadedFile(b'readme.diff', self.VALID_GIT_DIFF, content_type=b'text/x-patch'), 
           b'basedir': b'/trunk'}, expected_status=400)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], INVALID_REPOSITORY.code)