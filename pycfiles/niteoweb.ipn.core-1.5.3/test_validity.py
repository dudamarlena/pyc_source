# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matej/workarea/nw1/niteoweb.ipn.core/src/niteoweb/ipn/core/tests/test_validity.py
# Compiled at: 2013-09-25 09:25:26
"""Tests for @@validity view."""
from DateTime import DateTime
from niteoweb.ipn.core.interfaces import IIPN
from niteoweb.ipn.core.interfaces import IMemberDisabledEvent
from niteoweb.ipn.core.testing import IntegrationTestCase
from plone import api
from plone.app.testing import logout
from plone.app.testing import TEST_USER_ID
from zope.component import eventtesting
from zope.component import queryAdapter
from zope.testing.loggingsupport import InstalledHandler
import mock

class TestValidity(IntegrationTestCase):
    """Test @@validity view."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.ipn = queryAdapter(self.portal, IIPN)
        self.log = InstalledHandler('niteoweb.ipn.core')
        eventtesting.setUp()
        test_user = api.user.get(username=TEST_USER_ID)
        test_user.setMemberProperties(mapping={'valid_to': DateTime('2020/01/01')})

    def tearDown(self):
        """Clean up after yourself."""
        self.log.clear()
        eventtesting.clearEvents()

    def test_wrong_secret(self):
        """Test secret is required to access @@validity."""
        view = self.portal.restrictedTraverse('validity')
        err_msg = 'Wrong secret. Please configure it in control panel.'
        self.assertEquals(view.render(), err_msg)
        self.request['secret'] = 'wrong secret'
        self.assertEquals(view.render(), err_msg)

    @mock.patch('niteoweb.ipn.core.ipn.DateTime')
    def test_dry_run(self, DT):
        """Test that member is not disabled if dry-run is set to True."""
        DT.return_value = DateTime('2012/01/01')
        api.group.create(groupname='ipn_1')
        group = api.group.get(groupname='ipn_1')
        group.setGroupProperties(mapping={'validity': 31})
        self.ipn.enable_member(email='new@test.com', product_id='1', trans_type='SALE', fullname='New Member', affiliate='aff@test.com')
        DT.return_value = DateTime('2012/02/02')
        self.request['secret'] = 'secret'
        self.request['dry-run'] = True
        view = self.portal.restrictedTraverse('validity')
        view.render()
        self.assertIn('Member', api.user.get_roles(username='new@test.com'))
        self.assertNotIn('disabled', [ g.id for g in api.group.get_groups(username='new@test.com') ])

    def test_skip_disabled_members(self):
        """Test that disabled members are skipped."""
        api.group.add_user(groupname='disabled', username=TEST_USER_ID)
        self.request['secret'] = 'secret'
        view = self.portal.restrictedTraverse('validity')
        view.render()
        self.assertEqual(self.log.records, [])

    @mock.patch('niteoweb.ipn.core.ipn.DateTime')
    def test_validity(self, DT):
        """Integration test of @@validity view."""
        DT.return_value = DateTime('2012/01/01')
        api.group.create(groupname='ipn_1')
        group = api.group.get(groupname='ipn_1')
        group.setGroupProperties(mapping={'validity': 31})
        self.ipn.enable_member(email='new@test.com', product_id='1', trans_type='SALE', fullname='New Member', affiliate='aff@test.com')
        self.log.clear()
        eventtesting.clearEvents()
        logout()
        DT.return_value = DateTime('2012/02/02')
        self.request['secret'] = 'secret'
        view = self.portal.restrictedTraverse('validity')
        html = view.render()
        self.assertIn('disabled', [ g.id for g in api.group.get_groups(username='new@test.com') ])
        self.assertItemsEqual([
         'disabled', 'AuthenticatedUsers'], [ g.id for g in api.group.get_groups(username='new@test.com') ])
        self.assertNotIn('Member', api.user.get_roles(username='new@test.com'))
        events = list(set(eventtesting.getEvents(IMemberDisabledEvent)))
        self.assertEquals(len(events), 1)
        self.assertEquals(events[0].username, 'new@test.com')
        self.assert_member_history(username='new@test.com', history=[
         '2012/01/01 00:00:00|enable_member|1|SALE|',
         '2012/02/02 00:00:00|disable_member|1|cronjob|removed from groups: ipn_1, '])
        self.assertEquals(html.split('\n'), [
         'START validity check.',
         "Disabling member 'new@test.com' (2012/02/01)."])
        self.assertEqual(len(self.log.records), 5)
        self.assert_log_record('INFO', 'Anonymous User', "START disable_member:cronjob for 'new@test.com'.")
        self.assert_log_record('INFO', 'Anonymous User', "Adding member 'new@test.com' to Disabled group.")
        self.assert_log_record('INFO', 'Anonymous User', "Removing member 'new@test.com' from group 'ipn_1'.")
        self.assert_log_record('INFO', 'Anonymous User', "Revoking member 'new@test.com' the Member role.")
        self.assert_log_record('INFO', 'Anonymous User', "END disable_member:cronjob for 'new@test.com'.")