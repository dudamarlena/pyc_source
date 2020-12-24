# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matej/workarea/plone.hud/plone.app.hud/src/plone/app/hud/tests/test_security_advisories.py
# Compiled at: 2013-09-17 12:38:08
"""Tests for security advisories panel."""
from plone.app.hud.testing import IntegrationTestCase
import mock, os, tempfile

class TestSecurityAdvisories(IntegrationTestCase):
    """Integration tests for security advisories panel."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.security_advisories = self.portal.unrestrictedTraverse('@@hud_security')
        self.feed_contents = '\n<?xml version="1.0" encoding="utf-8" ?>\n<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n         xmlns:dc="http://purl.org/dc/elements/1.1/"\n         xmlns:syn="http://purl.org/rss/1.0/modules/syndication/"\n         xmlns="http://purl.org/rss/1.0/">\n\n<channel rdf:about="http://some.link.xyz/RSS">\n  <title>Plone Security Advisories</title>\n  <link>http://some.link.xyz</link>\n  <description></description>\n  <image rdf:resource="http://some.link.xyz/logo.png"/>\n\n  <items>\n    <rdf:Seq>\n        <rdf:li rdf:resource="http://some.link.xyz/hotfix-update-posted"/>\n        <rdf:li rdf:resource="http://some.link.xyz/security-patch"/>\n    </rdf:Seq>\n  </items>\n\n</channel>\n\n  <item rdf:about="http://some.link.xyz/hotfix-update-posted">\n    <title>20130618 Hotfix update posted</title>\n    <link>http://some.link.xyz/hotfix-update-posted</link>\n    <description>Version 1.3 of 20130618 released.</description>\n\n    <dc:publisher>No publisher</dc:publisher>\n    <dc:creator></dc:creator>\n    <dc:rights></dc:rights>\n    <dc:date>2013-07-02T13:50:09Z</dc:date>\n    <dc:type>News Item</dc:type>\n  </item>\n\n\n  <item rdf:about="http://some.link.xyz/security-patch">\n    <title>Security Patch Delayed until 2013-06-18</title>\n    <link>http://some.link.xyz/security-patch</link>\n    <description>download.zope.org server issues delaying hotfix</description>\n\n    <dc:publisher>No publisher</dc:publisher>\n    <dc:creator></dc:creator>\n    <dc:rights></dc:rights>\n    <dc:date>2013-06-11T14:23:24Z</dc:date>\n    <dc:type>News Item</dc:type>\n  </item>\n\n</rdf:RDF>\n        '
        self.feed_fd, self.feed_abs_path = tempfile.mkstemp()
        os.write(self.feed_fd, self.feed_contents)
        os.close(self.feed_fd)
        self.security_advisories.FEED_URL = self.feed_abs_path

    def tearDown(self):
        os.remove(self.feed_abs_path)

    def prepare_security_advisories_env(self, request_form={}):
        """Prepare all the variables for various tests.

        Also, optionally you can set 'request_form' (it must be dict type),
        this updates the values in the view.request.form,
        it does not remove any keys.
        """
        with mock.patch('plone.app.hud.hud_security_advisories.SecurityAdvisoriesView.panel_template'):
            self.security_advisories.request.form.update(request_form)
            self.security_advisories.render()

    def test_parsed_feed(self):
        self.prepare_security_advisories_env()
        for entry in self.security_advisories.feed_data:
            if entry['hash'] == '455ca55fc73efe03fad82a6180f4002d557c507e':
                self.assertEqual(entry['link'], 'http://some.link.xyz/hotfix-update-posted')
                self.assertIsNotNone(entry['localized_time'])
                self.assertEqual(entry['marked_as_read'], False)
                self.assertEqual(entry['summary'], 'Version 1.3 of 20130618 released.')
                self.assertEqual(entry['title'], '20130618 Hotfix update posted')
                self.assertIsNotNone(entry['updated'])
            elif entry['hash'] == '0b9cbb1288b35a0f750d426f18d80d59d7df9e95':
                self.assertEqual(entry['link'], 'http://some.link.xyz/security-patch')
                self.assertIsNotNone(entry['localized_time'])
                self.assertEqual(entry['marked_as_read'], False)
                self.assertEqual(entry['summary'], 'download.zope.org server issues delaying hotfix')
                self.assertEqual(entry['title'], 'Security Patch Delayed until 2013-06-18')
                self.assertIsNotNone(entry['updated'])
            else:
                self.fail("This shouldn't happed, it means that feed entry is changed or added.")

    def test_marked_as_read(self):
        self.prepare_security_advisories_env({'toggle_mark': '455ca55fc73efe03fad82a6180f4002d557c507e'})
        correct_entry = None
        for entry in self.security_advisories.feed_data:
            if entry['hash'] == '455ca55fc73efe03fad82a6180f4002d557c507e':
                correct_entry = entry
                break

        self.assertIsNotNone(correct_entry)
        self.assertTrue(correct_entry['marked_as_read'])
        return