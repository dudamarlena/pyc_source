# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matej/workarea/nw1/niteoweb.ipn.core/src/niteoweb/ipn/core/tests/test_enable.py
# Compiled at: 2014-03-07 04:26:36
"""Tests for enable_member action."""
from DateTime import DateTime
from niteoweb.ipn.core.interfaces import IIPN
from niteoweb.ipn.core.interfaces import IMemberEnabledEvent
from niteoweb.ipn.core.testing import IntegrationTestCase
from plone import api
from zope.component import eventtesting
from zope.component import queryAdapter
from zope.testing.loggingsupport import InstalledHandler
import mock

class TestConstraints(IntegrationTestCase):
    """Test different constraints on enable_member() action."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.ipn = queryAdapter(self.portal, IIPN)
        api.group.create(groupname='ipn_1')
        group = api.group.get(groupname='ipn_1')
        group.setGroupProperties(mapping={'validity': 31})

    def test_required_parameters(self):
        """Test that parameters are required."""
        from niteoweb.ipn.core.interfaces import MissingParamError
        with self.assertRaises(MissingParamError) as (cm):
            self.ipn.enable_member(email=None, product_id='1', trans_type='SALE')
        self.assertEquals(cm.exception.message, "Parameter 'email' is missing.")
        with self.assertRaises(MissingParamError) as (cm):
            self.ipn.enable_member(email='new@test.com', product_id=None, trans_type='SALE')
        self.assertEquals(cm.exception.message, "Parameter 'product_id' is missing.")
        with self.assertRaises(MissingParamError) as (cm):
            self.ipn.enable_member(email='new@test.com', product_id='1', trans_type=None)
        self.assertEquals(cm.exception.message, "Parameter 'trans_type' is missing.")
        return

    def test_product_group_parameter(self):
        """Test that product_group parameter is checked for validity."""
        from niteoweb.ipn.core.interfaces import InvalidParamValueError
        with self.assertRaises(InvalidParamValueError) as (cm):
            self.ipn.enable_member(email='new@test.com', product_id='0', trans_type='SALE')
        self.assertEquals(cm.exception.message, "Could not find group with id '0'.")

    def test_parameters_when_creating_a_new_member(self):
        """Test that 'affiliate' and 'fullname' parameters are required when
        member that is to be enabled does not exist yet."""
        from niteoweb.ipn.core.interfaces import MissingParamError
        with self.assertRaises(MissingParamError) as (cm):
            self.ipn.enable_member(email='new@test.com', product_id='1', trans_type='SALE', fullname=None, affiliate='aff@test.com')
        self.assertEquals(cm.exception.message, "Parameter 'fullname' is needed to create a new member.")
        with self.assertRaises(MissingParamError) as (cm):
            self.ipn.enable_member(email='new@test.com', product_id='1', trans_type='SALE', fullname='New Member', affiliate=None)
        self.assertEquals(cm.exception.message, "Parameter 'affiliate' is needed to create a new member.")
        return

    def test_product_validity_parameter(self):
        """Product validity, which is read from the product group, must be a
        positive integer."""
        from niteoweb.ipn.core.interfaces import InvalidParamValueError
        group = api.group.get(groupname='ipn_1')
        group.setGroupProperties(mapping={'validity': 0})
        with self.assertRaises(InvalidParamValueError) as (cm):
            self.ipn.enable_member(email='new@test.com', product_id='1', trans_type='SALE', fullname='New Member', affiliate='aff@test.com')
        self.assertEquals(cm.exception.message, "Validity for group 'ipn_1' is not a positive integer: 0")


class TestEnableMember(IntegrationTestCase):
    """Test runtime flow through the enable_member() action for most common
    use cases.
    """

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.ipn = queryAdapter(self.portal, IIPN)
        self.log = InstalledHandler('niteoweb.ipn.core')
        eventtesting.setUp()
        api.group.create(groupname='ipn_1')
        group = api.group.get(groupname='ipn_1')
        group.setGroupProperties(mapping={'validity': 31})
        api.group.create(groupname='ipn_2')
        group = api.group.get(groupname='ipn_2')
        group.setGroupProperties(mapping={'validity': 365})

    def tearDown(self):
        """Clean up after yourself."""
        self.log.clear()
        eventtesting.clearEvents()

    @mock.patch('niteoweb.ipn.core.ipn.DateTime')
    def test_enable_new_member(self, DT):
        """Test creating a new member with enable_member() action."""
        DT.return_value = DateTime('2012/01/01')
        self.ipn.enable_member(email='new@test.com', product_id='1', trans_type='SALE', fullname='New Member', affiliate='aff@test.com', note='Some test note!')
        member = api.user.get(username='new@test.com')
        self.assertTrue(member)
        self.assertEqual(member.getProperty('product_id'), '1')
        self.assertEqual(member.getProperty('fullname'), 'New Member')
        self.assertEqual(member.getProperty('affiliate'), 'aff@test.com')
        self.assertIn('new@test.com', [ user.id for user in api.user.get_users(groupname='ipn_1') ])
        self.assertEqual(api.user.get(username='new@test.com').getProperty('valid_to'), DateTime('2012/02/01'))
        events = list(set(eventtesting.getEvents(IMemberEnabledEvent)))
        self.assertEquals(len(events), 1)
        self.assertEquals(events[0].username, 'new@test.com')
        self.assert_member_history(username='new@test.com', history=[
         '2012/01/01 00:00:00|enable_member|1|SALE|Some test note!'])
        self.assertEqual(len(self.log.records), 5)
        self.assert_log_record('INFO', 'test_user_1_', "START enable_member:SALE for 'new@test.com'.")
        self.assert_log_record('INFO', 'test_user_1_', 'Creating a new member: new@test.com')
        self.assert_log_record('INFO', 'test_user_1_', "Added member 'new@test.com' to product group 'ipn_1'.")
        self.assert_log_record('INFO', 'test_user_1_', "Member's (new@test.com) valid_to date set to 2012/02/01.")
        self.assert_log_record('INFO', 'test_user_1_', "END enable_member:SALE for 'new@test.com'.")

    @mock.patch('niteoweb.ipn.core.ipn.DateTime')
    def test_enable_enabled_member(self, DT):
        """Test enabling an already enabled member, meaning extending its
        validity period."""
        DT.return_value = DateTime('2012/01/01')
        self.test_enable_new_member()
        DT.return_value = DateTime('2012/02/01')
        self.ipn.enable_member(email='new@test.com', product_id='2', trans_type='RECUR', note='Some test note!')
        self.assertEqual(api.user.get(username='new@test.com').getProperty('product_id'), '2')
        self.assertEqual(api.user.get(username='new@test.com').getProperty('valid_to'), DateTime('2013/01/31'))
        events = list(set(eventtesting.getEvents(IMemberEnabledEvent)))
        self.assertEquals(len(events), 2)
        self.assertEquals(events[0].username, 'new@test.com')
        self.assertEquals(events[1].username, 'new@test.com')
        self.assert_member_history(username='new@test.com', history=[
         '2012/01/01 00:00:00|enable_member|1|SALE|Some test note!',
         '2012/02/01 00:00:00|enable_member|2|RECUR|Some test note!'])
        self.assertEqual(len(self.log.records), 4)
        self.assert_log_record('INFO', 'test_user_1_', "START enable_member:RECUR for 'new@test.com'.")
        self.assert_log_record('INFO', 'test_user_1_', "Added member 'new@test.com' to product group 'ipn_2'.")
        self.assert_log_record('INFO', 'test_user_1_', "Member's (new@test.com) valid_to date set to 2013/01/31.")
        self.assert_log_record('INFO', 'test_user_1_', "END enable_member:RECUR for 'new@test.com'.")

    @mock.patch('niteoweb.ipn.core.ipn.DateTime')
    def test_enable_disabled_member(self, DT):
        """Test enabling a previously disabled member."""
        DT.return_value = DateTime('2012/01/01')
        api.user.create(email='disabled@test.com')
        api.group.add_user(groupname='disabled', username='disabled@test.com')
        api.user.revoke_roles(username='disabled@test.com', roles=[
         'Member'])
        self.ipn.enable_member(email='disabled@test.com', product_id='2', trans_type='UNCANCEL', note='Some test note!')
        self.assertNotIn('disabled', [ g.id for g in api.group.get_groups(username='disabled@test.com') ])
        self.assertIn('Member', api.user.get_roles(username='disabled@test.com'))
        self.assertEqual(api.user.get(username='disabled@test.com').getProperty('product_id'), '2')
        self.assertEqual(api.user.get(username='disabled@test.com').getProperty('valid_to'), DateTime('2012/12/31'))
        events = list(set(eventtesting.getEvents(IMemberEnabledEvent)))
        self.assertEquals(len(events), 1)
        self.assertEquals(events[0].username, 'disabled@test.com')
        self.assert_member_history(username='disabled@test.com', history=[
         '2012/01/01 00:00:00|enable_member|2|UNCANCEL|Some test note!'])
        self.assertEqual(len(self.log.records), 6)
        self.assert_log_record('INFO', 'test_user_1_', "START enable_member:UNCANCEL for 'disabled@test.com'.")
        self.assert_log_record('INFO', 'test_user_1_', "Removing member 'disabled@test.com' from Disabled group.")
        self.assert_log_record('INFO', 'test_user_1_', "Granting member 'disabled@test.com' the Member role.")
        self.assert_log_record('INFO', 'test_user_1_', "Added member 'disabled@test.com' to product group 'ipn_2'.")
        self.assert_log_record('INFO', 'test_user_1_', "Member's (disabled@test.com) valid_to date set to 2012/12/31.")
        self.assert_log_record('INFO', 'test_user_1_', "END enable_member:UNCANCEL for 'disabled@test.com'.")