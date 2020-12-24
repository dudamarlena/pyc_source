# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Products\PloneBooking\tests\PloneBookingTestCase.py
# Compiled at: 2008-11-19 15:29:07
"""PloneBooking tests

$Id: PloneBookingTestCase.py,v 1.8 2006/02/16 11:31:53 cbosse Exp $
"""
__author__ = ''
__docformat__ = 'restructuredtext'
import time
from Testing import ZopeTestCase
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from Acquisition import aq_base
from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.utils import getToolByName
from Products.PloneBooking.Extensions.Install import install as installPloneBooking
from Products.CMFPlone.tests import PloneTestCase
portal_name = PloneTestCase.portal_name
portal_owner = PloneTestCase.portal_owner
portal_member = 'portal_member'
portal_member2 = 'portal_member2'

class PloneBookingTestCase(PloneTestCase.PloneTestCase):
    """ PloneBooking test case based on a plone site"""
    __module__ = __name__

    def afterSetUp(self):
        self.ttool = getToolByName(self.portal, 'portal_types')
        self.wftool = getToolByName(self.portal, 'portal_workflow')
        self.mbtool = getToolByName(self.portal, 'portal_membership')
        self.btool = getToolByName(self.portal, 'portal_booking')
        self.member_folder = self.mbtool.getHomeFolder(portal_member)
        self.member_folder.manage_addLocalRoles(portal_member, roles=['Reviewer'])

    def createEmptyBookableObject(self, container, content_id='booking', wf_action=None):
        container.invokeFactory(type_name='BookableObject', id=content_id)
        self.failUnless(content_id in container.objectIds())
        self.bookable_object = getattr(container, content_id)
        self.assertEqual(self.bookable_object.title, '')
        self.assertEqual(self.bookable_object.getId(), content_id)
        if wf_action is not None:
            self.wftool.doActionFor(self.bookable_object, wf_action)
        return self.bookable_object

    def createEmptyBooking(self, container, content_id='booking'):
        container.invokeFactory(type_name='Booking', id=content_id)
        self.failUnless(content_id in container.objectIds())
        self.booking = getattr(container, content_id)
        self.assertEqual(self.booking.title, '')
        self.assertEqual(self.booking.getId(), content_id)
        return self.booking

    def createEmptyBookingCenter(self, container, content_id='booking_center'):
        container.invokeFactory(type_name='BookingCenter', id=content_id)
        self.failUnless(content_id in container.objectIds())
        self.booking_center = getattr(container, content_id)
        self.assertEqual(self.booking_center.Title(), '')
        self.assertEqual(self.booking_center.getId(), content_id)
        return self.booking_center

    def createBookingStructure(self, container, center_id='booking_center', object_id='bookable_object', booking_id='booking'):
        self.booking_center = self.createEmptyBookingCenter(container, content_id=center_id)
        self.bookable_object = self.createEmptyBookableObject(self.booking_center, content_id=object_id)
        self.wftool.doActionFor(self.bookable_object, 'publish')
        self.booking = self.createEmptyBooking(self.bookable_object, content_id=booking_id)

    def doBooking(self, booking, bookable_object, start_date, end_date):
        """
          Booking a bookable object
        """
        booking.edit(startDate=start_date, endDate=end_date)
        self.failUnless(booking.getStartDate() == start_date, 'Value is %s' % booking.getStartDate())
        self.failUnless(booking.getEndDate() == end_date, 'Value is %s' % booking.getEndDate())
        booking.addReference(bookable_object, 'is_booking')
        self.failUnless(booking.getStartDate() == start_date, 'Value is %s' % booking.getStartDate())
        self.failUnless(booking.getEndDate() == end_date, 'Value is %s' % booking.getEndDate())
        self.failUnless(bookable_object.UID() == booking.getBookedObjectUID(), 'Uid of bookable obj (%s) not in  %s' % (bookable_object.UID(), booking.getBookedObjectUID()))

    def beforeTearDown(self):
        noSecurityManager()

    def loginAsPortalMember(self):
        """Use if you need to manipulate an object as member."""
        uf = self.portal.acl_users
        user = uf.getUserById(portal_member).__of__(uf)
        newSecurityManager(None, user)
        return

    def loginAsPortalMember2(self):
        """Use if you need to manipulate an object as member."""
        uf = self.portal.acl_users
        user = uf.getUserById(portal_member2).__of__(uf)
        newSecurityManager(None, user)
        return

    def loginAsPortalOwner(self):
        """Use if you need to manipulate an object as portal owner."""
        uf = self.app.acl_users
        user = uf.getUserById(portal_owner).__of__(uf)
        newSecurityManager(None, user)
        return


def setupPloneBooking(app, quiet=0):
    get_transaction().begin()
    _start = time.time()
    portal = app.portal
    if not quiet:
        ZopeTestCase._print('Installing PloneBooking ... ')
    user = app.acl_users.getUserById(portal_owner).__of__(app.acl_users)
    newSecurityManager(None, user)
    if hasattr(aq_base(portal), 'portal_booking'):
        ZopeTestCase._print('PloneBooking already installed ... ')
    else:
        installPloneBooking(portal)
    portal.portal_registration.addMember(portal_member, 'azerty', ['Member'])
    portal.portal_registration.addMember(portal_member2, 'azerty', ['Member'])
    noSecurityManager()
    get_transaction().commit()
    if not quiet:
        ZopeTestCase._print('done (%.3fs)\n' % (time.time() - _start,))
    return


app = ZopeTestCase.app()
setupPloneBooking(app)
ZopeTestCase.close(app)