# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\PloneBooking\tests\testPloneBooking.py
# Compiled at: 2008-11-19 15:29:07
__doc__ = '\nPloneBooking base test\n\n$Id: testPloneBooking.py,v 1.14 2006/02/16 11:30:40 cbosse Exp $\n'
from DateTime import DateTime
from common import *
from Products.CMFCore.utils import getToolByName
tests = []

class TestPloneBooking(PloneBookingTestCase):
    __module__ = __name__

    def testCreateBookingCenter(self):
        """
        """
        self.loginAsPortalMember()
        self.booking_center = self.createEmptyBookingCenter(self.member_folder)

    def testEditBookingCenter(self):
        """
        Editing Booking Center
        """
        self.loginAsPortalMember()
        self.createEmptyBookingCenter(self.member_folder)
        title = 'A dummy Booking Center'
        description = 'A dummy description'
        self.booking_center.edit(title=title, description=description)
        self.failUnless(self.booking_center.Title() == title, 'Value is %s' % self.booking_center.Title())
        self.failUnless(self.booking_center.Description() == description, 'Value is %s' % self.booking_center.Description())

    def testCreateBookableObject(self):
        """
        """
        self.loginAsPortalMember()
        self.createEmptyBookingCenter(self.member_folder)
        self.createEmptyBookableObject(self.booking_center)

    def testEditBookableObject(self):
        """
        Editing Bookable Object
        """
        self.loginAsPortalMember()
        self.createEmptyBookingCenter(self.member_folder)
        self.createEmptyBookableObject(self.booking_center)
        title = 'A dummy Bookable Object'
        description = 'A dummy description'
        category = 'Dummy Category'
        self.bookable_object.edit(title=title, description=description, category=category)
        self.failUnless(self.bookable_object.Title() == title, 'Value is %s' % self.bookable_object.Title())
        self.failUnless(self.bookable_object.Description() == description, 'Value is %s' % self.bookable_object.Description())
        self.failUnless(self.bookable_object.getCategory() == category, 'Value is %s' % self.bookable_object.getCategory())

    def testCreateBooking(self):
        """
        """
        self.loginAsPortalMember()
        self.booking_center = self.createEmptyBookingCenter(self.member_folder)
        self.bookable_object = self.createEmptyBookableObject(self.booking_center, wf_action='publish')
        self.booking = self.createEmptyBooking(self.bookable_object)

    def testEditBooking(self):
        """
        Editing Booking
        """
        self.loginAsPortalMember()
        self.createEmptyBookingCenter(self.member_folder)
        self.createEmptyBookableObject(self.booking_center, wf_action='publish')
        self.createEmptyBooking(self.bookable_object)
        title = 'A dummy title'
        description = 'A dummy description'
        name = 'dummy name'
        phone = '0666996699'
        mail = 'dummy@dummy.com'
        bookedObjects = ''
        startDate = DateTime()
        endDate = DateTime()
        self.booking.edit(title=title, description=description, fullName=name, phone=phone, mail=mail, startDate=startDate, endDate=endDate)
        self.failUnless(self.booking.Title() == title, 'Value is %s' % self.booking.Title())
        self.failUnless(self.booking.Description() == description, 'Value is %s' % self.booking.Description())
        self.failUnless(self.booking.getFullName() == name, 'Value is %s' % self.booking.getFullName())
        self.failUnless(self.booking.getPhone() == phone, 'Value is %s' % self.booking.getPhone())
        self.failUnless(self.booking.start() == startDate, 'Value is %s' % self.booking.getStartDate())
        self.failUnless(self.booking.end() == endDate, 'Value is %s' % self.booking.getEndDate())

    def testBookingStructure(self):
        """
          Create booking center, object and booking
        """
        self.loginAsPortalMember()
        self.createBookingStructure(self.member_folder)

    def testDoBooking(self):
        """
          Book an object from startDate to endDate
        """
        self.loginAsPortalMember()
        self.createBookingStructure(self.member_folder)
        self.doBooking(booking=self.booking, bookable_object=self.bookable_object, start_date=DateTime(), end_date=DateTime())

    def testGetBookedObject(self):
        """
        """
        self.loginAsPortalMember()
        self.createBookingStructure(self.member_folder)
        self.doBooking(booking=self.booking, bookable_object=self.bookable_object, start_date=DateTime(), end_date=DateTime())
        self.failUnless(self.booking.getBookedObject().UID() == self.bookable_object.UID(), 'Value is %s' % self.booking.getBookedObject().UID())

    def testHasBookedObject(self):
        """
        """
        self.loginAsPortalMember()
        self.createBookingStructure(self.member_folder)
        object_uid = self.bookable_object.UID()
        start_date = DateTime('1981/02/08')
        end_date = DateTime('1981/02/10')
        self.failUnless(self.booking.hasBookedObject(start_date, end_date) == False, 'WTF ?! Object is booked and it should not !')
        self.doBooking(booking=self.booking, bookable_object=self.bookable_object, start_date=start_date, end_date=end_date)
        self.booking.addReference(self.bookable_object, 'is_booking')
        self.failUnless(self.booking.hasBookedObject(start_date, end_date) == True, 'Object is not booked between %s and %s' % (self.booking.getStartDate(), self.booking.getEndDate()))
        start_date = DateTime('1981/02/07')
        end_date = DateTime('1981/02/10')
        self.failUnless(self.booking.hasBookedObject(start_date, end_date) == True, 'Gosh ! Object is not booked between %s and %s' % (self.booking.getStartDate(), self.booking.getEndDate()))
        start_date = DateTime('1981/02/09')
        end_date = DateTime('1981/02/12')
        self.failUnless(self.booking.hasBookedObject(start_date, end_date) == True, 'Gosh ! Object is not booked between %s and %s' % (self.booking.getStartDate(), self.booking.getEndDate()))
        start_date = DateTime('1981/02/07')
        end_date = DateTime('1981/02/12')
        self.failUnless(self.booking.hasBookedObject(start_date, end_date) == True, 'Gosh ! Object is not booked between %s and %s' % (self.booking.getStartDate(), self.booking.getEndDate()))
        start_date = DateTime('1981/03/09')
        end_date = DateTime('1981/03/12')
        self.failUnless(self.booking.hasBookedObject(start_date, end_date) == False, 'Gosh ! Object is booked !')

    def createBookingCenter2(self, container, content_id='content_id', title=''):
        """
        """
        container.invokeFactory(type_name='BookingCenter', id=content_id)
        self.failUnless(content_id in container.objectIds())
        booking_center = getattr(container, content_id)
        self.assertEqual(booking_center.Title(), '')
        self.assertEqual(booking_center.getId(), content_id)
        return booking_center

    def createBookableObject2(self, container, content_id='bookable_obj', title='', wf_action=None):
        container.invokeFactory(type_name='BookableObject', id=content_id)
        self.failUnless(content_id in container.objectIds())
        bookable_object = getattr(container, content_id)
        self.assertEqual(bookable_object.getId(), content_id)
        self.assertEqual(bookable_object.Title(), '')
        if wf_action is not None:
            self.wftool.doActionFor(bookable_object, wf_action)
        return bookable_object

    def createBooking2(self, container, content_id='booking', title='', description='', name='', phone='', mail='toto@toto.com', bookable_objects=(), start_date=DateTime(), end_date=DateTime(), wf_action=None):
        """
        """
        container.invokeFactory(type_name='Booking', id=content_id)
        self.failUnless(content_id in container.objectIds())
        booking = getattr(container, content_id)
        self.assertEqual(booking.title, '')
        self.assertEqual(booking.getId(), content_id)
        booking.edit(title=title, description=description, fullName=name, phone=phone, mail=mail, startDate=start_date, endDate=end_date)
        self.failUnless(booking.Title() == title, 'Value is %s' % booking.Title())
        self.failUnless(booking.Description() == description, 'Value is %s' % booking.Description())
        self.failUnless(booking.getFullName() == name, 'Value is %s' % booking.getFullName())
        self.failUnless(booking.getPhone() == phone, 'Value is %s' % booking.getPhone())
        self.failUnless(booking.start() == start_date, 'Value is %s' % booking.getStartDate())
        self.failUnless(booking.end() == end_date, 'Value is %s' % booking.getEndDate())
        return booking

    def testBookingCreation2(self):
        """
        """
        self.loginAsPortalMember()
        booking_center = self.createBookingCenter2(self.member_folder)
        bookable_object = self.createBookableObject2(booking_center, wf_action='publish')
        start_date = DateTime('2005/02/08')
        end_date = DateTime('2005/02/14')
        booking = self.createBooking2(bookable_object, title='Resa1', description='pas de description', name='Toto', phone='88666666', mail='toto@toto.com', start_date=start_date, end_date=end_date, wf_action='booked')
        start_date = DateTime('2005/01/08')
        end_date = DateTime('2005/01/14')
        brains = booking_center.getBookingBrains(start_date=start_date, end_date=end_date)
        self.failUnless(len(brains) == 0, '%s is already booked. Brains Count : %s ' % (bookable_object.title_or_id(), len(brains)))
        start_date = DateTime('2006/01/08')
        end_date = DateTime('2006/01/14')
        brains = booking_center.getBookingBrains(start_date=start_date, end_date=end_date)
        self.failUnless(len(brains) == 0, '%s is already booked. Brains Count : %s ' % (bookable_object.title_or_id(), len(brains)))
        start_date = DateTime('2005/02/07')
        end_date = DateTime('2005/02/12')
        brains = booking_center.getBookingBrains(start_date=start_date, end_date=end_date)
        self.failUnless(len(brains) == 1, '%s is already booked. Brains Count : %s ' % (bookable_object.title_or_id(), len(brains)))
        start_date = DateTime('2005/02/09')
        end_date = DateTime('2005/02/15')
        brains = booking_center.getBookingBrains(start_date=start_date, end_date=end_date)
        self.failUnless(len(brains) == 1, '%s is already booked. Brains Count : %s ' % (bookable_object.title_or_id(), len(brains)))
        start_date = DateTime('2005/02/07')
        end_date = DateTime('2005/02/15')
        brains = booking_center.getBookingBrains(start_date=start_date, end_date=end_date)
        self.failUnless(len(brains) == 1, '%s is already booked. Brains Count : %s ' % (bookable_object.title_or_id(), len(brains)))
        start_date = DateTime('2005/02/09')
        end_date = DateTime('2005/02/12')
        brains = booking_center.getBookingBrains(start_date=start_date, end_date=end_date)
        self.failUnless(len(brains) == 1, '%s is already booked. Brains Count : %s ' % (bookable_object.title_or_id(), len(brains)))

    def testGetXthDayOfMonth(self):
        """
        """
        self.loginAsPortalOwner()
        self.createEmptyBookingCenter(self.member_folder)
        self.createEmptyBookableObject(self.booking_center, wf_action='publish')
        self.createEmptyBooking(self.bookable_object)
        title = 'A dummy title'
        description = 'A dummy description'
        name = 'dummy name'
        phone = '0666996699'
        mail = 'dummy@dummy.com'
        start_date = DateTime('2005/08/29 09:00:00 GMT+2')
        end_date = DateTime('2005/09/01 18:00:00 GMT+2')
        final_date = DateTime('2005/10/29 09:00:00 GMT+2')
        periodicity_variable = 2
        result = self.booking.getXthDayOfMonth(start_date, end_date, final_date, periodicity_variable)
        last_start_date = result[(-1)][0]
        self.failUnless(last_start_date <= final_date, '%s must be <= to %s' % (last_start_date, final_date))
        expected_result = [
         (
          DateTime('2005/09/12 09:00:00 GMT+2'), DateTime('2005/09/15 18:00:00 GMT+2')), (DateTime('2005/10/10 09:00:00 GMT+2'), DateTime('2005/10/13 18:00:00 GMT+2'))]
        self.assertEquals(result, expected_result)
        start_date = DateTime('2005/08/29 09:00:00 GMT+2')
        end_date = DateTime('2005/09/01 18:00:00 GMT+2')
        final_date = DateTime('2006/10/29 09:00:00 GMT+2')
        periodicity_variable = 5
        result = self.booking.getXthDayOfMonth(start_date, end_date, final_date, periodicity_variable)
        last_start_date = result[(-1)][0]
        self.failUnless(last_start_date <= final_date, '%s must be <= to %s' % (last_start_date, final_date))
        expected_result = [
         (
          DateTime('2005/10/31 09:00:00 GMT+1'), DateTime('2005/11/03 18:00:00 GMT+1')), (DateTime('2006/01/30 09:00:00 GMT+1'), DateTime('2006/02/02 18:00:00 GMT+1')), (DateTime('2006/05/29 09:00:00 GMT+2'), DateTime('2006/06/01 18:00:00 GMT+2')), (DateTime('2006/07/31 09:00:00 GMT+2'), DateTime('2006/08/03 18:00:00 GMT+2'))]
        self.assertEquals(result, expected_result)
        start_date = DateTime('2005/08/29 09:00:00 GMT+2')
        end_date = DateTime('2005/09/01 18:00:00 GMT+2')
        final_date = DateTime('2006/10/29 09:00:00 GMT+2')
        periodicity_variable = 0
        result = self.booking.getXthDayOfMonth(start_date, end_date, final_date, periodicity_variable)
        expected_result = []
        self.assertEqual(result, expected_result)

    def testCreatePeriodicBookingsType1(self):
        """
        """
        self.loginAsPortalOwner()
        self.createEmptyBookingCenter(self.member_folder)
        self.createEmptyBookableObject(self.booking_center, wf_action='publish')
        self.createEmptyBooking(self.bookable_object)
        title = 'A dummy title'
        description = 'A dummy description'
        name = 'dummy name'
        phone = '0666996699'
        mail = 'dummy@dummy.com'
        startDate = DateTime('2005/08/29 09:00')
        endDate = DateTime('2005/08/29 10:00')
        end_periodicity = DateTime('2005/08/29 09:00')
        self.booking.edit(title=title, description=description, fullName=name, phone=phone, mail=mail, startDate=startDate, endDate=endDate)
        self.failUnless(not self.booking.isPeriodicBooking())
        periodicity_end_date = DateTime('2004/08/29 09:00')
        infos = self.booking.getPeriodicityInfos(periodicity_type=1, periodicity_end_date=periodicity_end_date)
        result = self.booking.createPeriodicBookings(periodicity_type=1, periodicity_end_date=periodicity_end_date)
        self.assertEquals(1, len(self.bookable_object.objectIds()))
        self.assertEquals(1, len(self.booking.getAllPeriodicBookingBrains()))
        self.failUnless(not self.booking.isPeriodicBooking())
        periodicity_end_date = DateTime('2005/09/29 09:00')
        infos = self.booking.getPeriodicityInfos(periodicity_type=1, periodicity_end_date=periodicity_end_date)
        result = self.booking.createPeriodicBookings(periodicity_type=1, periodicity_end_date=periodicity_end_date)
        self.assertEquals(5, len(self.bookable_object.objectIds()))
        self.assertEquals(5, len(self.booking.getAllPeriodicBookingBrains()))
        self.failUnless(self.booking.isPeriodicBooking())
        self.logout()

    def testCreatePeriodicBookingsType2(self):
        """
        """
        self.loginAsPortalOwner()
        self.createEmptyBookingCenter(self.member_folder)
        self.createEmptyBookableObject(self.booking_center, wf_action='publish')
        self.createEmptyBooking(self.bookable_object)
        title = 'A dummy title'
        description = 'A dummy description'
        name = 'dummy name'
        phone = '0666996699'
        mail = 'dummy@dummy.com'
        startDate = DateTime('2005/08/29 09:00')
        endDate = DateTime('2005/08/29 10:00')
        self.booking.edit(title=title, description=description, fullName=name, phone=phone, mail=mail, startDate=startDate, endDate=endDate)
        self.failUnless(not self.booking.isPeriodicBooking())
        periodicity_end_date = DateTime('2005/10/29 09:00')
        infos = self.booking.getPeriodicityInfos(periodicity_type=2, periodicity_end_date=periodicity_end_date, week_interval=2)
        result = self.booking.createPeriodicBookings(periodicity_type=2, periodicity_end_date=periodicity_end_date, week_interval=2)
        self.assertEquals(5, len(self.bookable_object.objectIds()))
        self.assertEquals(5, len(self.booking.getAllPeriodicBookingBrains()))
        self.failUnless(self.booking.isPeriodicBooking())
        self.logout()

    def testCreatePeriodicBookingsType3(self):
        """
        """
        self.loginAsPortalOwner()
        self.createEmptyBookingCenter(self.member_folder)
        self.createEmptyBookableObject(self.booking_center, wf_action='publish')
        self.createEmptyBooking(self.bookable_object)
        title = 'A dummy title'
        description = 'A dummy description'
        name = 'dummy name'
        phone = '0666996699'
        mail = 'dummy@dummy.com'
        startDate = DateTime('2005/08/12 09:00')
        endDate = DateTime('2005/08/13 10:00')
        self.booking.edit(title=title, description=description, fullName=name, phone=phone, mail=mail, startDate=startDate, endDate=endDate)
        self.failUnless(not self.booking.isPeriodicBooking())
        periodicity_end_date = DateTime('2005/12/29 09:00')
        infos = self.booking.getPeriodicityInfos(periodicity_type=3, periodicity_end_date=periodicity_end_date)
        self.booking.edit(startDate=startDate, endDate=endDate)
        result = self.booking.createPeriodicBookings(periodicity_type=3, periodicity_end_date=periodicity_end_date)
        self.assertEquals(5, len(self.bookable_object.objectIds()))
        self.assertEquals(5, len(self.booking.getAllPeriodicBookingBrains()))
        self.failUnless(self.booking.isPeriodicBooking())
        start_date = DateTime('2005/08/14 09:00')
        end_date = DateTime('2005/08/14 12:00')
        self.booking.edit(startDate=start_date, endDate=end_date)
        infos = self.booking.getPeriodicityInfos(periodicity_type=3, periodicity_end_date=periodicity_end_date)
        result = self.booking.createPeriodicBookings(periodicity_type=3, periodicity_end_date=periodicity_end_date)
        self.assertEquals(9, len(self.bookable_object.objectIds()))
        self.assertEquals(9, len(self.booking.getAllPeriodicBookingBrains()))
        self.failUnless(self.booking.isPeriodicBooking())
        self.logout()

    def testGetIntervalOfMinutesGroupKeys(self):
        """
        """
        interval = 30
        start_dt = DateTime(2005, 11, 15, 8, 0, 0)
        end_dt = DateTime(2005, 11, 15, 12, 0, 0)
        expected = [ (2005, 11, 15, x * interval) for x in range(16, 24) ]
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt, interval)
        self.assertEquals(result, expected)
        start_dt = DateTime(2005, 11, 15, 9, 15, 0)
        end_dt = DateTime(2005, 11, 15, 9, 25, 0)
        expected = [(2005, 11, 15, 540)]
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt, interval)
        self.assertEquals(result, expected)
        start_dt = DateTime(2005, 11, 15, 9, 0, 0)
        end_dt = DateTime(2005, 11, 15, 9, 30, 0)
        expected = [(2005, 11, 15, 540)]
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt, interval)
        self.assertEquals(result, expected)
        start_dt = DateTime(2005, 11, 15, 9, 0, 0)
        end_dt = DateTime(2005, 11, 15, 9, 35, 0)
        expected = [(2005, 11, 15, 540), (2005, 11, 15, 570)]
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt, interval)
        self.assertEquals(result, expected)
        start_dt = DateTime(2005, 11, 15, 8, 55, 0)
        end_dt = DateTime(2005, 11, 15, 9, 30, 0)
        expected = [(2005, 11, 15, 510), (2005, 11, 15, 540)]
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt, interval)
        self.assertEquals(result, expected)
        start_dt = DateTime(2005, 11, 15, 8, 30, 0)
        end_dt = DateTime(2005, 11, 15, 9, 30, 0)
        expected = [(2005, 11, 15, 510), (2005, 11, 15, 540)]
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt, interval)
        self.assertEquals(result, expected)
        interval = 60
        start_dt = DateTime(2005, 11, 14, 22, 0, 0)
        end_dt = DateTime(2005, 11, 15, 2, 0, 0)
        expected = [ (2005, 11, 14, x * interval) for x in range(22, 24) ]
        expected.extend([ (2005, 11, 15, x * interval) for x in range(0, 2) ])
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt, interval)
        self.assertEquals(result, expected)
        start_dt = DateTime(2005, 11, 14, 9, 15, 0)
        end_dt = DateTime(2005, 11, 14, 9, 45, 0)
        expected = [(2005, 11, 14, 540)]
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt, interval)
        self.assertEquals(result, expected)
        start_dt = DateTime(2005, 11, 14, 9, 0, 0)
        end_dt = DateTime(2005, 11, 14, 10, 0, 0)
        expected = [(2005, 11, 14, 540)]
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt, interval)
        self.assertEquals(result, expected)

    def testGetDayGroupKeys(self):
        """
        """
        start_dt = DateTime(2005, 11, 14, 9, 0, 0)
        end_dt = DateTime(2005, 11, 14, 10, 0, 0)
        expected = [(2005, 11, 14)]
        result = self.btool.getDayGroupKeys(start_dt, end_dt)
        self.assertEquals(result, expected)
        start_dt = DateTime(2005, 11, 14, 0, 0, 0)
        end_dt = DateTime(2005, 11, 15, 0, 0, 0)
        expected = [(2005, 11, 14)]
        result = self.btool.getDayGroupKeys(start_dt, end_dt)
        self.assertEquals(result, expected)
        start_dt = DateTime(2005, 11, 14, 23, 59, 59)
        end_dt = DateTime(2005, 11, 15, 0, 0, 30)
        expected = [(2005, 11, 14), (2005, 11, 15)]
        result = self.btool.getDayGroupKeys(start_dt, end_dt)
        self.assertEquals(result, expected)

    def testGetWeekGroupKeys(self):
        """
        """
        start_dt = DateTime(2005, 11, 8, 9, 0, 0)
        end_dt = DateTime(2005, 11, 9, 18, 0, 0)
        expected = [(2005, 45)]
        result = self.btool.getWeekGroupKeys(start_dt, end_dt)
        self.assertEquals(result, expected)
        start_dt = DateTime(2005, 11, 7, 0, 0, 0)
        end_dt = DateTime(2005, 11, 14, 0, 0, 0)
        expected = [(2005, 45)]
        result = self.btool.getWeekGroupKeys(start_dt, end_dt)
        self.assertEquals(result, expected)
        start_dt = DateTime(2005, 11, 13, 23, 59, 59)
        end_dt = DateTime(2005, 11, 14, 0, 0, 1)
        expected = [(2005, 45), (2005, 46)]
        result = self.btool.getWeekGroupKeys(start_dt, end_dt)
        self.assertEquals(result, expected)

    def testGetMonthGroupKeys(self):
        """
        """
        start_dt = DateTime(2005, 11, 7, 9, 0, 0)
        end_dt = DateTime(2005, 11, 9, 18, 0, 0)
        expected = [(2005, 11)]
        result = self.btool.getMonthGroupKeys(start_dt, end_dt)
        self.assertEquals(result, expected)
        start_dt = DateTime(2005, 11, 1, 0, 0, 0)
        end_dt = DateTime(2005, 12, 1, 0, 0, 0)
        expected = [(2005, 11)]
        result = self.btool.getMonthGroupKeys(start_dt, end_dt)
        self.assertEquals(result, expected)
        start_dt = DateTime(2005, 10, 31, 23, 59, 59)
        end_dt = DateTime(2005, 11, 1, 0, 0, 1)
        expected = [(2005, 10), (2005, 11)]
        result = self.btool.getMonthGroupKeys(start_dt, end_dt)
        self.assertEquals(result, expected)

    def testGetYearGroupKeys(self):
        """
        """
        start_dt = DateTime(2005, 11, 7, 9, 0, 0)
        end_dt = DateTime(2005, 11, 9, 18, 0, 0)
        expected = [2005]
        result = self.btool.getYearGroupKeys(start_dt, end_dt)
        self.assertEquals(result, expected)
        start_dt = DateTime(2005, 1, 1, 0, 0, 0)
        end_dt = DateTime(2006, 1, 1, 0, 0, 0)
        expected = [2005]
        result = self.btool.getYearGroupKeys(start_dt, end_dt)
        self.assertEquals(result, expected)
        start_dt = DateTime(2005, 12, 31, 23, 59, 59)
        end_dt = DateTime(2006, 1, 1, 0, 0, 1)
        expected = [2005, 2006]
        result = self.btool.getYearGroupKeys(start_dt, end_dt)
        self.assertEquals(result, expected)

    def testGetBookingBrains(self):
        """
        """
        self.loginAsPortalOwner()
        self.createEmptyBookingCenter(self.member_folder)
        self.createEmptyBookableObject(self.booking_center, wf_action='publish')
        self.createEmptyBooking(self.bookable_object)
        start_date = DateTime(2005, 11, 15, 9, 0, 0)
        end_date = DateTime(2005, 11, 15, 9, 30, 0)
        self.booking.edit(startDate=start_date, endDate=end_date)
        brains = self.booking_center.getBookingBrains(start_date, end_date)
        self.assertEquals(len(brains), 1)
        start_date = DateTime(2005, 11, 15, 9, 5, 0)
        end_date = DateTime(2005, 11, 15, 9, 25, 0)
        brains = self.booking_center.getBookingBrains(start_date, end_date)
        self.assertEquals(len(brains), 1)
        start_date = DateTime(2005, 11, 15, 8, 55, 0)
        end_date = DateTime(2005, 11, 15, 9, 25, 0)
        brains = self.booking_center.getBookingBrains(start_date, end_date)
        self.assertEquals(len(brains), 1)
        start_date = DateTime(2005, 11, 15, 9, 5, 0)
        end_date = DateTime(2005, 11, 15, 9, 35, 0)
        brains = self.booking_center.getBookingBrains(start_date, end_date)
        self.assertEquals(len(brains), 1)
        start_date = DateTime(2005, 11, 15, 8, 55, 0)
        end_date = DateTime(2005, 11, 15, 9, 35, 0)
        brains = self.booking_center.getBookingBrains(start_date, end_date)
        self.assertEquals(len(brains), 1)
        start_date = DateTime(2005, 11, 15, 8, 30, 0)
        end_date = DateTime(2005, 11, 15, 9, 0, 0)
        brains = self.booking_center.getBookingBrains(start_date, end_date)
        self.assertEquals(len(brains), 0)
        start_date = DateTime(2005, 11, 15, 9, 30, 0)
        end_date = DateTime(2005, 11, 15, 10, 0, 0)
        brains = self.booking_center.getBookingBrains(start_date, end_date)
        self.assertEquals(len(brains), 0)


tests.append(TestPloneBooking)
if __name__ == '__main__':
    framework()
else:
    import unittest

    def test_suite():
        suite = unittest.TestSuite()
        for test in tests:
            suite.addTest(unittest.makeSuite(test))

        return suite