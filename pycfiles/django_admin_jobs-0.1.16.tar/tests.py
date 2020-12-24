# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\dipap\Desktop\Projects\Orfium\project\earnings-dashboard\upload_tools\tests.py
# Compiled at: 2017-12-08 08:00:10
from __future__ import unicode_literals
from django.test import TestCase
from earnings_dashboard_project.settings import AWS_URL
from upload_tools.models import *

class AssetUploadJobTest(TestCase):

    def setUp(self):
        self.asset_upload_job_valid = AssetUploadJob.objects.create(asset_file=b'%s/test-data/assets/assets-valid.csv' % AWS_URL)
        self.asset_upload_missing_title = AssetUploadJob.objects.create(asset_file=b'%s/test-data/assets/assets-missing-title.csv' % AWS_URL)
        self.asset_upload_missing_code = AssetUploadJob.objects.create(asset_file=b'%s/test-data/assets/assets-missing-code.csv' % AWS_URL)

    def test_valid_asset_upload_job_gets_processed(self):
        self.asset_upload_job_valid.process()
        self.assertEqual(self.asset_upload_job_valid.status, b'FINISHED', b'Valid asset upload job did not finish successfully')
        self.assertTrue(self.asset_upload_job_valid.finished >= self.asset_upload_job_valid.started, b'Valid asset upload job finished with invalid timing info')
        self.assertEqual(Asset.objects.all().count(), 500, b'Valid asset upload job finished but assets were not imported')
        for id_field in [b'isrc', b'upc', b'ean', b'isan', b'iswc', b'grid']:
            self.assertEqual(Asset.objects.filter(**{id_field: b'%s-TEST' % id_field.upper()}).count(), 1, b'Asset with %s was not imported' % id_field.upper())

        self.assertEqual(Asset.objects.filter(external_id=b'9999008', external_id_source=b'ORFIUM').count(), 1, b'Asset with Orfium ID was not imported')
        self.assertEqual(Asset.objects.filter(isrc=b'ISRC-TEST-2', external_id=b'9999007', external_id_source=b'ORFIUM').count(), 1, b'Asset with both Orfium ID and ISRC was not imported')

    def test_asset_upload_job_status_is_found_on_firebase(self):
        self.asset_upload_job_valid.process()
        state = self.asset_upload_job_valid._read_state_from_firebase()
        self.assertEqual(state[b'status'], b'Finished', b'Finished upload job has incorrect state on Firebase')
        self.assertTrue(state[b'finished'] >= state[b'started'], b'Upload job time was not recorded correctly on Firebase')
        self.asset_upload_missing_title.process()
        state = self.asset_upload_missing_title._read_state_from_firebase()
        self.assertEqual(state[b'status'], b'Failed', b'Failed upload job has incorrect state on Firebase')

    def test_upload_job_with_missing_title_fails(self):
        self.asset_upload_missing_title.process()
        self.assertEqual(self.asset_upload_missing_title.status, b'FAILED', b'Asset upload job with missing title did not fail')

    def test_upload_job_with_missing_code_fails(self):
        self.asset_upload_missing_code.process()
        self.assertEqual(self.asset_upload_missing_code.status, b'FAILED', b'Asset upload job with missing title did not fail')