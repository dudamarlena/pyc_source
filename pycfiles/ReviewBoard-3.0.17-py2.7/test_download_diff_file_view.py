# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/tests/test_download_diff_file_view.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for reviewboard.reviews.views.DownloadDiffFileView."""
from __future__ import unicode_literals
from reviewboard.extensions.tests import TestService
from reviewboard.hostingsvcs.models import HostingServiceAccount
from reviewboard.hostingsvcs.service import register_hosting_service, unregister_hosting_service
from reviewboard.site.urlresolvers import local_site_reverse
from reviewboard.testing import TestCase

class DownloadDiffFileViewTests(TestCase):
    """Unit tests for reviewboard.reviews.views.DownloadDiffFileView."""
    fixtures = [
     b'test_users', b'test_scmtools']

    @classmethod
    def setUpClass(cls):
        super(DownloadDiffFileViewTests, cls).setUpClass()
        register_hosting_service(TestService.hosting_service_id, TestService)

    @classmethod
    def tearDownClass(cls):
        super(DownloadDiffFileViewTests, cls).tearDownClass()
        unregister_hosting_service(TestService.hosting_service_id)

    def setUp(self):
        super(DownloadDiffFileViewTests, self).setUp()
        self.account = HostingServiceAccount.objects.create(service_name=TestService.name, hosting_url=b'http://example.com/', username=b'foo')
        self.repository = self.create_repository(hosting_account=self.account)
        self.review_request = self.create_review_request(repository=self.repository, publish=True)
        self.diffset = self.create_diffset(review_request=self.review_request)
        self.filediff = self.create_filediff(self.diffset, source_file=b'/invalid-path', dest_file=b'/invalid-path')

    def testing_download_orig_file_404(self):
        """Testing DownloadDiffFileView with original file when the file
        cannot be found upstream
        """
        rsp = self.client.get(local_site_reverse(b'download-orig-file', kwargs={b'review_request_id': self.review_request.display_id, 
           b'revision': self.diffset.revision, 
           b'filediff_id': self.filediff.pk}))
        self.assertEquals(rsp.status_code, 404)

    def testing_download_modified_file_404(self):
        """Testing DownloadDiffFileView with modified file when the file
        cannot be found upstream
        """
        rsp = self.client.get(local_site_reverse(b'download-modified-file', kwargs={b'review_request_id': self.review_request.display_id, 
           b'revision': self.diffset.revision, 
           b'filediff_id': self.filediff.pk}))
        self.assertEquals(rsp.status_code, 404)