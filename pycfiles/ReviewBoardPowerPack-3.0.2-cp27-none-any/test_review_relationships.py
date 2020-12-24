# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/reports/tests/test_review_relationships.py
# Compiled at: 2019-06-17 15:11:31
"""Tests for the Review Relationships report."""
from __future__ import unicode_literals
import datetime
from django.contrib.auth.models import User
from reviewboard.site.urlresolvers import local_site_reverse
from rbpowerpack.testing.testcases import PowerPackExtensionTestCase

class ReviewRelationshipsTestCase(PowerPackExtensionTestCase):
    """Tests for the Review Relationships report."""
    fixtures = [
     b'test_users']

    def test_csv_with_missing_user(self):
        """Testing Review Relationships CSV with missing user"""
        self.extension.license_settings.add_licensed_users([
         User.objects.get(username=b'doc')])
        review_request = self.create_review_request(publish=True)
        self.create_review(review_request, publish=True)
        url = local_site_reverse(b'powerpack-reports-report-data', local_site=None, kwargs={b'report_id': b'review-relationships'})
        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=1)
        self.client.login(username=b'doc', password=b'doc')
        self.client.get(url, data={b'users': b'doc', 
           b'groups': b'', 
           b'start': yesterday.strftime(b'%Y-%m-%d'), 
           b'end': now.strftime(b'%Y-%m-%d'), 
           b'csv': 1})
        return