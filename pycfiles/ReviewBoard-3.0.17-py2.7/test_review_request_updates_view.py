# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/tests/test_review_request_updates_view.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for ReviewRequestUpdatesView."""
from __future__ import unicode_literals
import json, struct
from datetime import datetime, timedelta
from django.core.urlresolvers import reverse
from django.utils.timezone import utc
from reviewboard.reviews.views import ReviewRequestUpdatesView
from reviewboard.testing import TestCase

class ReviewRequestUpdatesViewTests(TestCase):
    """Unit tests for ReviewRequestUpdatesView."""
    fixtures = [
     b'test_users']

    def setUp(self):
        super(ReviewRequestUpdatesViewTests, self).setUp()
        self.review_request = self.create_review_request(publish=True, time_added=datetime(2017, 9, 7, 17, 0, 0, tzinfo=utc), last_updated=datetime(2017, 9, 7, 23, 10, 0, tzinfo=utc))
        self.review1 = self.create_review(self.review_request, timestamp=self.review_request.time_added + timedelta(days=10), publish=True)
        self.general_comment = self.create_general_comment(self.review1, issue_opened=True)
        self.review2 = self.create_review(self.review_request, timestamp=self.review1.timestamp + timedelta(days=10), publish=True)
        self.review3 = self.create_review(self.review_request, timestamp=self.review2.timestamp + timedelta(days=10), publish=False)
        self.view = ReviewRequestUpdatesView.as_view()

    def test_get(self):
        """Testing ReviewRequestUpdatesView GET"""
        updates = self._get_updates()
        self.assertEqual(len(updates), 4)
        metadata, html = updates[0]
        self.assertEqual(metadata[b'type'], b'entry')
        self.assertEqual(metadata[b'entryType'], b'review')
        self.assertEqual(metadata[b'entryID'], b'1')
        self.assertEqual(metadata[b'addedTimestamp'], b'2017-09-17 17:00:00+00:00')
        self.assertEqual(metadata[b'updatedTimestamp'], b'2017-09-17 17:00:00+00:00')
        self.assertEqual(metadata[b'viewOptions'], {})
        self.assertEqual(metadata[b'modelData'], {b'reviewData': {b'id': self.review1.pk, 
                           b'public': True, 
                           b'bodyTop': self.review1.body_top, 
                           b'bodyBottom': self.review1.body_bottom, 
                           b'shipIt': self.review1.ship_it}})
        self.assertTrue(html.startswith(b'<div id="review1"'))
        self.assertTrue(html.endswith(b'\n</div>'))
        metadata, html = updates[1]
        self.assertEqual(metadata[b'type'], b'entry')
        self.assertEqual(metadata[b'entryType'], b'review')
        self.assertEqual(metadata[b'entryID'], b'2')
        self.assertEqual(metadata[b'addedTimestamp'], b'2017-09-27 17:00:00+00:00')
        self.assertEqual(metadata[b'updatedTimestamp'], b'2017-09-27 17:00:00+00:00')
        self.assertEqual(metadata[b'viewOptions'], {})
        self.assertEqual(metadata[b'modelData'], {b'reviewData': {b'id': self.review2.pk, 
                           b'public': True, 
                           b'bodyTop': self.review2.body_top, 
                           b'bodyBottom': self.review2.body_bottom, 
                           b'shipIt': self.review2.ship_it}})
        self.assertTrue(html.startswith(b'<div id="review2"'))
        self.assertTrue(html.endswith(b'\n</div>'))
        metadata, html = updates[2]
        self.assertEqual(metadata[b'type'], b'entry')
        self.assertEqual(metadata[b'entryType'], b'initial_status_updates')
        self.assertEqual(metadata[b'entryID'], b'0')
        self.assertEqual(metadata[b'addedTimestamp'], b'2017-09-07 17:00:00+00:00')
        self.assertEqual(metadata[b'updatedTimestamp'], b'2017-09-07 17:00:00+00:00')
        self.assertEqual(metadata[b'viewOptions'], {})
        self.assertEqual(metadata[b'modelData'], {b'pendingStatusUpdates': False})
        self.assertTrue(html.startswith(b'<div id="initial_status_updates"'))
        self.assertTrue(html.endswith(b'\n</div>'))
        metadata, html = updates[3]
        self.assertEqual(metadata[b'type'], b'issue-summary-table')
        self.assertTrue(html.startswith(b'<div id="issue-summary"'))
        self.assertTrue(html.endswith(b'\n</div>'))

    def test_get_with_unicode(self):
        """Testing ReviewRequestUpdatesView GET with Unicode content"""
        self.review1.body_top = b'áéíóú'
        self.review1.save(update_fields=('body_top', ))
        self.review2.body_top = b'ÄËÏÖÜŸ'
        self.review2.save(update_fields=('body_top', ))
        self.general_comment.text = b'ĀĒĪŌ'
        self.general_comment.save(update_fields=('text', ))
        updates = self._get_updates()
        self.assertEqual(len(updates), 4)
        metadata, html = updates[0]
        self.assertEqual(metadata[b'type'], b'entry')
        self.assertEqual(metadata[b'entryType'], b'review')
        self.assertEqual(metadata[b'entryID'], b'1')
        self.assertEqual(metadata[b'addedTimestamp'], b'2017-09-17 17:00:00+00:00')
        self.assertEqual(metadata[b'updatedTimestamp'], b'2017-09-17 17:00:00+00:00')
        self.assertEqual(metadata[b'viewOptions'], {})
        self.assertEqual(metadata[b'modelData'], {b'reviewData': {b'id': self.review1.pk, 
                           b'public': True, 
                           b'bodyTop': self.review1.body_top, 
                           b'bodyBottom': self.review1.body_bottom, 
                           b'shipIt': self.review1.ship_it}})
        self.assertTrue(html.startswith(b'<div id="review1"'))
        self.assertTrue(html.endswith(b'\n</div>'))
        self.assertIn(b'áéíóú', html)
        metadata, html = updates[1]
        self.assertEqual(metadata[b'type'], b'entry')
        self.assertEqual(metadata[b'entryType'], b'review')
        self.assertEqual(metadata[b'entryID'], b'2')
        self.assertEqual(metadata[b'addedTimestamp'], b'2017-09-27 17:00:00+00:00')
        self.assertEqual(metadata[b'updatedTimestamp'], b'2017-09-27 17:00:00+00:00')
        self.assertEqual(metadata[b'viewOptions'], {})
        self.assertEqual(metadata[b'modelData'], {b'reviewData': {b'id': self.review2.pk, 
                           b'public': True, 
                           b'bodyTop': self.review2.body_top, 
                           b'bodyBottom': self.review2.body_bottom, 
                           b'shipIt': self.review2.ship_it}})
        self.assertTrue(html.startswith(b'<div id="review2"'))
        self.assertTrue(html.endswith(b'\n</div>'))
        self.assertIn(b'ÄËÏÖÜŸ', html)
        metadata, html = updates[2]
        self.assertEqual(metadata[b'type'], b'entry')
        self.assertEqual(metadata[b'entryType'], b'initial_status_updates')
        self.assertEqual(metadata[b'entryID'], b'0')
        self.assertEqual(metadata[b'addedTimestamp'], b'2017-09-07 17:00:00+00:00')
        self.assertEqual(metadata[b'updatedTimestamp'], b'2017-09-07 17:00:00+00:00')
        self.assertEqual(metadata[b'viewOptions'], {})
        self.assertEqual(metadata[b'modelData'], {b'pendingStatusUpdates': False})
        self.assertTrue(html.startswith(b'<div id="initial_status_updates"'))
        self.assertTrue(html.endswith(b'\n</div>'))
        metadata, html = updates[3]
        self.assertEqual(metadata[b'type'], b'issue-summary-table')
        self.assertTrue(html.startswith(b'<div id="issue-summary"'))
        self.assertTrue(html.endswith(b'\n</div>'))
        self.assertIn(b'ĀĒĪŌ', html)

    def test_get_with_entries(self):
        """Testing ReviewRequestUpdatesView GET with ?entries=..."""
        updates = self._get_updates({b'entries': b'review:2;initial_status_updates:0'})
        self.assertEqual(len(updates), 3)
        metadata, html = updates[0]
        self.assertEqual(metadata[b'type'], b'entry')
        self.assertEqual(metadata[b'entryType'], b'review')
        self.assertEqual(metadata[b'entryID'], b'2')
        self.assertEqual(metadata[b'addedTimestamp'], b'2017-09-27 17:00:00+00:00')
        self.assertEqual(metadata[b'updatedTimestamp'], b'2017-09-27 17:00:00+00:00')
        self.assertEqual(metadata[b'viewOptions'], {})
        self.assertEqual(metadata[b'modelData'], {b'reviewData': {b'id': self.review2.pk, 
                           b'public': True, 
                           b'bodyTop': self.review2.body_top, 
                           b'bodyBottom': self.review2.body_bottom, 
                           b'shipIt': self.review2.ship_it}})
        self.assertTrue(html.startswith(b'<div id="review2"'))
        self.assertTrue(html.endswith(b'\n</div>'))
        metadata, html = updates[1]
        self.assertEqual(metadata[b'type'], b'entry')
        self.assertEqual(metadata[b'entryType'], b'initial_status_updates')
        self.assertEqual(metadata[b'entryID'], b'0')
        self.assertEqual(metadata[b'addedTimestamp'], b'2017-09-07 17:00:00+00:00')
        self.assertEqual(metadata[b'updatedTimestamp'], b'2017-09-07 17:00:00+00:00')
        self.assertEqual(metadata[b'viewOptions'], {})
        self.assertEqual(metadata[b'modelData'], {b'pendingStatusUpdates': False})
        self.assertTrue(html.startswith(b'<div id="initial_status_updates"'))
        self.assertTrue(html.endswith(b'\n</div>'))
        metadata, html = updates[2]
        self.assertEqual(metadata[b'type'], b'issue-summary-table')
        self.assertTrue(html.startswith(b'<div id="issue-summary"'))
        self.assertTrue(html.endswith(b'\n</div>'))

    def test_get_with_review_entries_adds_issue_summary_table(self):
        """Testing ReviewRequestUpdatesView GET with ?entries=review:...
        always includes the issue summary table
        """
        updates = self._get_updates({b'entries': b'review:2'})
        self.assertEqual(len(updates), 2)
        metadata, html = updates[0]
        self.assertEqual(metadata[b'type'], b'entry')
        self.assertEqual(metadata[b'entryType'], b'review')
        self.assertEqual(metadata[b'entryID'], b'2')
        self.assertEqual(metadata[b'addedTimestamp'], b'2017-09-27 17:00:00+00:00')
        self.assertEqual(metadata[b'updatedTimestamp'], b'2017-09-27 17:00:00+00:00')
        self.assertEqual(metadata[b'viewOptions'], {})
        self.assertEqual(metadata[b'modelData'], {b'reviewData': {b'id': self.review2.pk, 
                           b'public': True, 
                           b'bodyTop': self.review2.body_top, 
                           b'bodyBottom': self.review2.body_bottom, 
                           b'shipIt': self.review2.ship_it}})
        self.assertTrue(html.startswith(b'<div id="review2"'))
        self.assertTrue(html.endswith(b'\n</div>'))
        metadata, html = updates[1]
        self.assertEqual(metadata[b'type'], b'issue-summary-table')
        self.assertTrue(html.startswith(b'<div id="issue-summary"'))
        self.assertTrue(html.endswith(b'\n</div>'))

    def test_get_with_invalid_entries(self):
        """Testing ReviewRequestUpdatesView GET with invalid ?entries=...
        values
        """
        response = self.client.get(self._build_url(), {b'entries': b'review2'})
        self.assertEqual(response.status_code, 400)

    def test_get_with_since(self):
        """Testing ReviewRequestUpdatesView GET with ?since=..."""
        timestamp = self.review1.timestamp + timedelta(days=1)
        updates = self._get_updates({b'since': timestamp.isoformat()})
        self.assertEqual(len(updates), 2)
        metadata, html = updates[0]
        self.assertEqual(metadata[b'type'], b'entry')
        self.assertEqual(metadata[b'entryType'], b'review')
        self.assertEqual(metadata[b'entryID'], b'2')
        self.assertEqual(metadata[b'addedTimestamp'], b'2017-09-27 17:00:00+00:00')
        self.assertEqual(metadata[b'updatedTimestamp'], b'2017-09-27 17:00:00+00:00')
        self.assertEqual(metadata[b'viewOptions'], {})
        self.assertEqual(metadata[b'modelData'], {b'reviewData': {b'id': self.review2.pk, 
                           b'public': True, 
                           b'bodyTop': self.review2.body_top, 
                           b'bodyBottom': self.review2.body_bottom, 
                           b'shipIt': self.review2.ship_it}})
        self.assertTrue(html.startswith(b'<div id="review2"'))
        self.assertTrue(html.endswith(b'\n</div>'))
        metadata, html = updates[1]
        self.assertEqual(metadata[b'type'], b'issue-summary-table')
        self.assertTrue(html.startswith(b'<div id="issue-summary"'))
        self.assertTrue(html.endswith(b'\n</div>'))

    def test_post(self):
        """Testing ReviewRequestUpdatesView POST not allowed"""
        with self.assertNumQueries(1):
            response = self.client.post(self._build_url())
        self.assertEqual(response.status_code, 405)

    def test_put(self):
        """Testing ReviewRequestUpdatesView PUT not allowed"""
        with self.assertNumQueries(1):
            response = self.client.put(self._build_url())
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """Testing ReviewRequestUpdatesView DELETE not allowed"""
        with self.assertNumQueries(1):
            response = self.client.delete(self._build_url())
        self.assertEqual(response.status_code, 405)

    def _build_url(self):
        return reverse(b'review-request-updates', args=[
         self.review_request.display_id])

    def _get_updates(self, query={}):
        response = self.client.get(self._build_url(), query)
        self.assertEqual(response.status_code, 200)
        content = response.content
        self.assertIs(type(content), bytes)
        i = 0
        updates = []
        while i < len(content):
            metadata_len = struct.unpack_from(b'<L', content, i)[0]
            i += 4
            metadata = json.loads(content[i:i + metadata_len].decode(b'utf-8'))
            i += metadata_len
            html_len = struct.unpack_from(b'<L', content, i)[0]
            i += 4
            html = content[i:i + html_len].decode(b'utf-8')
            i += html_len
            updates.append((metadata, html))

        return updates