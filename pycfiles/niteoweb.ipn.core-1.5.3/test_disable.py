# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matej/workarea/nw1/niteoweb.ipn.core/src/niteoweb/ipn/core/tests/test_disable.py
# Compiled at: 2013-09-25 09:25:26
"""Tests for disable_member action."""
from DateTime import DateTime
from niteoweb.ipn.core.interfaces import IIPN
from niteoweb.ipn.core.interfaces import IMemberDisabledEvent
from niteoweb.ipn.core.testing import IntegrationTestCase
from plone import api
from zope.component import eventtesting
from zope.component import queryAdapter
from zope.testing.loggingsupport import InstalledHandler
import mock

class TestConstraints(IntegrationTestCase):
    """Test different constraints on disable_member() action."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.ipn = queryAdapter(self.portal, IIPN)

    def test_required_parameters(self):
        """Test that parameters are required."""
        from niteoweb.ipn.core.interfaces import MissingParamError
        with self.assertRaises(MissingParamError) as (cm):
            self.ipn.disable_member(email=None, product_id='1', trans_type='CANCEL')
        self.assertEquals(cm.exception.message, "Parameter 'email' is missing.")
        with self.assertRaises(MissingParamError) as (cm):
            self.ipn.disable_member(email='enabled@test.com', product_id='1', trans_type=None)
        self.assertEquals(cm.exception.message, "Parameter 'trans_type' is missing.")
        return

    def test_nonexistent_member(self):
        """Test disabling a non-existing member."""
        from niteoweb.ipn.core.interfaces import InvalidParamValueError
        with self.assertRaises(InvalidParamValueError) as (cm):
            self.ipn.disable_member(email='nonexistent@test.com', product_id='1', trans_type='CANCEL')
        self.assertEquals(cm.exception.message, "Cannot disable a nonexistent member: 'nonexistent@test.com'.")


class TestUseCases(IntegrationTestCase):
    """Test runtime flow through the disable_member() action for most common
    use cases.
    """

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.ipn = queryAdapter(self.portal, IIPN)
        self.log = InstalledHandler('niteoweb.ipn.core')
        eventtesting.setUp()
        api.user.create(email='enabled@test.com')
        api.group.create(groupname='ipn_1')
        api.group.add_user(username='enabled@test.com', groupname='ipn_1')

    def tearDown(self):
        """Clean up after yourself."""
        self.log.clear()
        eventtesting.clearEvents()

    @mock.patch('niteoweb.ipn.core.ipn.DateTime')
    def test_disable_enabled_member(self, DT):
        """Test default execution of the disable_member() action."""
        DT.return_value = DateTime('2012/01/01')
        self.ipn.disable_member(email='enabled@test.com', product_id='1', trans_type='CANCEL')
        self.assertIn('disabled', [ g.id for g in api.group.get_groups(username='enabled@test.com') ])
        self.assertItemsEqual([
         'disabled', 'AuthenticatedUsers'], [ g.id for g in api.group.get_groups(username='enabled@test.com') ])
        self.assertNotIn('Member', api.user.get_roles(username='enabled@test.com'))
        events = list(set(eventtesting.getEvents(IMemberDisabledEvent)))
        self.assertEquals(len(events), 1)
        self.assertEquals(events[0].username, 'enabled@test.com')
        self.assert_member_history(username='enabled@test.com', history=[
         '2012/01/01 00:00:00|disable_member|1|CANCEL|removed from groups: ipn_1, '])
        self.assertEqual(len(self.log.records), 5)
        self.assert_log_record('INFO', 'test_user_1_', "START disable_member:CANCEL for 'enabled@test.com'.")
        self.assert_log_record('INFO', 'test_user_1_', "Adding member 'enabled@test.com' to Disabled group.")
        self.assert_log_record('INFO', 'test_user_1_', "Removing member 'enabled@test.com' from group 'ipn_1'.")
        self.assert_log_record('INFO', 'test_user_1_', "Revoking member 'enabled@test.com' the Member role.")
        self.assert_log_record('INFO', 'test_user_1_', "END disable_member:CANCEL for 'enabled@test.com'.")

    @mock.patch('niteoweb.ipn.core.ipn.DateTime')
    def test_disable_disabled_member(self, DT):
        """Test disabling an already disabled member. This should not happen
        often, but it still could."""
        DT.return_value = DateTime('2012/01/01')
        self.test_disable_enabled_member()
        DT.return_value = DateTime('2012/02/01')
        self.ipn.disable_member(email='enabled@test.com', product_id='1', trans_type='CANCEL')
        events = list(set(eventtesting.getEvents(IMemberDisabledEvent)))
        self.assertEquals(len(events), 2)
        self.assertEquals(events[0].username, 'enabled@test.com')
        self.assertEquals(events[1].username, 'enabled@test.com')
        self.assert_member_history(username='enabled@test.com', history=[
         '2012/01/01 00:00:00|disable_member|1|CANCEL|removed from groups: ipn_1, ',
         '2012/02/01 00:00:00|disable_member|1|CANCEL|'])
        for record in self.log.records:
            self.assertNotIn("Adding member 'enabled@test.com' to Disabled group.", record.getMessage())
            self.assertNotIn("Revoking member 'enabled@test.com' the Member role.", record.getMessage())