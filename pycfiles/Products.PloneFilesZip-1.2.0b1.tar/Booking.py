# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\PloneBooking\content\Booking.py
# Compiled at: 2008-11-19 15:29:16
__doc__ = '\n    PloneBooking: Booking Content\n'
__version__ = '$Revision: 1.13 $'
__author__ = ''
__docformat__ = 'restructuredtext'
from zope.interface import implements
from types import DictionaryType
from Products.ATContentTypes.content.folder import ATFolder
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from DateTime import DateTime
from Globals import InitializeClass
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.interfaces import IBaseContent
try:
    from Products.LinguaPlone.public import *
except ImportError:
    from Products.Archetypes.public import *

from Products.generator import i18n
from Products.PloneBooking.config import PROJECTNAME, I18N_DOMAIN
from Products.PloneBooking.content.schemata import BookingSchema
from Products.PloneBooking.interfaces import IBooking

class Booking(BaseContent):
    """
      Booking says which bookable object is booked ...
    """
    __module__ = __name__
    implements(IBooking)
    _at_rename_after_creation = True
    schema = BookingSchema
    security = ClassSecurityInfo()
    security.declareProtected('View', 'findXthDayOfMonth')

    def findXthDayOfMonth(self, date, day_name, pos):
        """
        Return: date of the Xth day (day_name) of given date month.
        date: DateTime
        day_name: string
        pos: int
        return: DateTime (%y/%m/%d)
        """
        month_number = date.month()
        ref_date = DateTime('%s/%s/01' % (date.year(), date.month()))
        while pos >= 0:
            if ref_date.Day() == day_name:
                pos = pos - 1
            if ref_date.month() != month_number:
                return 0
            if ref_date.Day() == day_name and pos == 0:
                return ref_date
            ref_date = ref_date + 1

        return 0

    security.declareProtected('View', 'getXthDayOfMonth')

    def getXthDayOfMonth(self, start_date, end_date, final_date, periodicity_variable):
        """
        return all dates corresponding to the x day of month, between "date" and "end_date"
        For example all the "third tuesday of month" between "date" and "end_date"
        """
        btool = getToolByName(self, 'portal_booking')
        ref_day_name = start_date.Day()
        ref_date = self.getNewDate(start_date)
        end_hour = end_date.TimeMinutes()
        start_hour = start_date.TimeMinutes()
        diff = DateTime(end_date.Date()) - DateTime(start_date.Date())
        result = []
        while ref_date <= final_date:
            result_date = self.findXthDayOfMonth(ref_date, ref_day_name, periodicity_variable)
            if result_date:
                new_start_date = DateTime('%s %s' % (result_date, start_hour))
                new_end_date = DateTime('%s %s' % (result_date + diff, end_hour))
                if new_start_date <= final_date:
                    result.append((new_start_date, new_end_date))
                ref_date = self.getNewDate(new_start_date)
            else:
                ref_date = self.getNewDate(ref_date)

        return result

    security.declarePrivate('getNewDate')

    def getNewDate(self, mydate):
        """
        Return a a new date, the first day of next month
        """
        month_number = mydate.month()
        year = mydate.year()
        hour = mydate.TimeMinutes()
        if month_number == 12:
            new_date = DateTime('%s/%s/%s %s' % (year + 1, '01', '01', hour))
        else:
            new_date = DateTime('%s/%s/%s %s' % (year, month_number + 1, '01', hour))
        return new_date

    security.declareProtected(permissions.ModifyPortalContent, 'getPeriodicityInfos')

    def getPeriodicityInfos(self, periodicity_type, periodicity_end_date, **kwargs):
        """
        Returns a list of tuple (start_ts, end_ts, already_booked)

        @param periodicity_type: type of periodicity
        @param periodicity_end_date: end date (DateTime of periodicity end)
        @param kwargs: It depends on the periodicity type
        """
        btool = getToolByName(self, 'portal_booking')
        start_dt = self.start()
        end_dt = self.end()
        start_ts = btool.zdt2ts(start_dt)
        end_ts = btool.zdt2ts(end_dt)
        booked_object_uid = self.getBookedObjectUID()
        booking_brains = self.getBookingBrains(start_date=start_dt, end_date=periodicity_end_date, getBookedObjectUID=booked_object_uid, review_state=('pending',
                                                                                                                                                       'booked'))
        booking_infos_ts = [ (btool.zdt2ts(DateTime(x.start)), btool.zdt2ts(DateTime(x.end))) for x in booking_brains ]
        periodicity_end_ts = btool.zdt2ts(periodicity_end_date)
        periodicity_infos_ts = []
        infos = []
        if periodicity_end_date <= end_dt:
            return ()
        if periodicity_type in (1, 2):
            step = 7
            if periodicity_type == 2:
                step = 7 * kwargs.get('week_interval', 1)
            ref_start = DateTime(start_dt) + step
            ref_end = DateTime(end_dt) + step
            while ref_start <= periodicity_end_date:
                periodicity_infos_ts.append((btool.zdt2ts(ref_start), btool.zdt2ts(ref_end)))
                ref_start += step
                ref_end += step

        if periodicity_type == 3:
            week_day_number_of_month = btool.weekDayNumberOfMonth(start_dt)
            result = self.getXthDayOfMonth(start_dt, end_dt, periodicity_end_date, week_day_number_of_month)
            periodicity_infos_ts = [ (btool.zdt2ts(x), btool.zdt2ts(y)) for (x, y) in result ]
        for (pstart_ts, pend_ts) in periodicity_infos_ts:
            b_booked = False
            for (bstart_ts, bend_ts) in booking_infos_ts:
                if bstart_ts >= pstart_ts and bstart_ts < pend_ts or bend_ts > pstart_ts and bend_ts <= pend_ts:
                    b_booked = True
                    break

            infos.append((pstart_ts, pend_ts, b_booked))

        return infos

    security.declareProtected(permissions.ModifyPortalContent, 'createOnePeriodicityBooking')

    def createOnePeriodicityBooking(self, start_ts, end_ts):
        """
            Create an object for periodicity
            Parameters:
                start_ts -> timestamp
                end_ts -> timestamp
            Return:
                OK if done
                NOK if already booked
        """
        btool = getToolByName(self, 'portal_booking')
        booked_obj = self.getBookedObject()
        booked_object_uid = self.getBookedObjectUID()
        start_date = btool.ts2zdt(start_ts)
        end_date = btool.ts2zdt(end_ts)
        booking_brains = self.getBookingBrains(start_date=start_date, end_date=end_date, getBookedObjectUID=booked_object_uid, review_state=('pending',
                                                                                                                                             'booked'))
        if booking_brains:
            return 'NOK'
        obj_id = self.generateUniqueId('Booking')
        booked_obj.invokeFactory('Booking', obj_id)
        obj = getattr(self, obj_id)
        args = {'startDate': start_date, 'endDate': end_date, 'title': self.Title(), 'description': self.Description(), 'fullName': self.getFullName(), 'phone': self.getPhone(), 'email': self.getEmail(), 'periodicityUID': self.getPeriodicityUID()}
        obj.edit(**args)
        return 'OK'

    security.declareProtected(permissions.ModifyPortalContent, 'createPeriodicBookings')

    def createPeriodicBookings(self, periodicity_type, periodicity_end_date, **kwargs):
        """
        create one object for each item return by getPeriodicityInfos method
        date already booked will be ignored
        """
        request = self.REQUEST
        response = request.RESPONSE
        btool = getToolByName(self, 'portal_booking')
        booked_obj = self.getBookedObject()
        infos = self.getPeriodicityInfos(periodicity_type, periodicity_end_date, **kwargs)
        ptool = getToolByName(self, 'portal_properties')
        charset = ptool.site_properties.default_charset
        response.setHeader('Content-type', 'text/html; charset=%s' % charset)
        if not infos:
            msg_id = 'message_no_booking_created'
            msg_default = 'No booking created.'
            msg = i18n.translate(I18N_DOMAIN, msg_id, context=self, default=msg_default)
            return msg
        created = 0
        already_booked = 0
        title = self.Title()
        description = self.Description()
        fullname = self.getFullName()
        phone = self.getPhone()
        email = self.getEmail()
        periodicity_uid = self.getPeriodicityUID()
        for (pstart_ts, pend_ts, b_booked) in infos:
            if b_booked:
                already_booked += 1
                continue
            obj_id = self.generateUniqueId('Booking')
            booked_obj.invokeFactory('Booking', obj_id)
            obj = getattr(self, obj_id)
            args = {'startDate': btool.ts2zdt(pstart_ts), 'endDate': btool.ts2zdt(pend_ts), 'title': title, 'description': description, 'fullName': fullname, 'phone': phone, 'email': email, 'periodicityUID': periodicity_uid}
            obj.edit(**args)
            created += 1

        mapping = {}
        mapping['created'] = str(created)
        mapping['already_booked'] = str(already_booked)
        msg_id = 'message_create_periodic_bookings'
        msg_default = '${created} items created, ${already_booked} already booked'
        msg = i18n.translate(I18N_DOMAIN, msg_id, mapping=mapping, context=self, default=msg_default)
        return msg

    security.declareProtected('View', 'getAllPeriodicBookingBrains')

    def getAllPeriodicBookingBrains(self, **kwargs):
        """
        get all bookings with parent_uid == parent.UID()
        """
        ctool = getToolByName(self, 'portal_catalog')
        query_args = {}
        query_args['portal_type'] = 'Booking'
        query_args['getPeriodicityUID'] = self.getPeriodicityUID()
        if kwargs:
            query_args.update(kwargs)
        return ctool.searchResults(**query_args)

    security.declareProtected('View', 'isPeriodicBooking')

    def isPeriodicBooking(self):
        """
        Return True if self was created with periodicity --> len(all_periodic_bookings) > 1
        """
        all_periodic_bookings = self.getAllPeriodicBookingBrains()
        if all_periodic_bookings and len(all_periodic_bookings) > 1:
            return True
        return False

    security.declarePrivate('getDefaultPeriodicityUID')

    def getDefaultPeriodicityUID(self):
        """
        Default value for parent_uid field
        Return self uid
        """
        return self.UID()

    security.declarePrivate('View', 'getDefaultStartDate')

    def getDefaultStartDate(self):
        """
        Default value for startDate field
        """
        ts_start = self.REQUEST.form.get('startDate', None)
        date_value = None
        if ts_start is not None:
            try:
                date_value = DateTime(float(ts_start))
            except ValueError:
                date_value = DateTime(ts_start)

        else:
            date_value = DateTime()
        minutes = date_value.minute()
        minutes = int(minutes / 5) * 5
        date_string = date_value.strftime('%Y/%m/%d %H')
        date_string += ':%s' % minutes
        return DateTime(date_string)

    security.declarePrivate('View', 'getDefaultEndDate')

    def getDefaultEndDate(self):
        """
        Default value for endDate field
        """
        ts_end = self.REQUEST.form.get('endDate', None)
        date_value = None
        if ts_end is not None:
            try:
                date_value = DateTime(float(ts_end))
            except ValueError:
                date_value = DateTime(ts_end)

        else:
            date_value = DateTime()
        minutes = date_value.minute()
        minutes = int(minutes / 5) * 5
        date_string = date_value.strftime('%Y/%m/%d %H')
        date_string += ':%s' % minutes
        return DateTime(date_string)

    security.declarePrivate('View', 'getDefaultEmail')

    def getDefaultEmail(self):
        """
        Default value for email field
        get email from authenticated member properties
        """
        mtool = getToolByName(self, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        email = ''
        if member is not None:
            email = member.getProperty('email', '')
        return email

    security.declarePrivate('View', 'getDefaultFullname')

    def getDefaultFullname(self):
        """
        Default value for fullname field
        get fullname from authenticated member properties
        """
        mtool = getToolByName(self, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        fullname = ''
        if member is not None:
            fullname = member.getProperty('fullname', '')
        return fullname

    security.declarePrivate('View', 'getDefaultPhone')

    def getDefaultPhone(self):
        """
        Default value for phone field
        get phone from authenticated member properties
        """
        mtool = getToolByName(self, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        phone = ''
        if member is not None:
            phone = member.getProperty('phone', '')
        return phone

    security.declareProtected('View', 'getBookedObject')

    def getBookedObject(self):
        """
        Returns booked object
        """
        return self.getBookableObject()

    security.declareProtected('View', 'hasBookedObject')

    def hasBookedObject(self, start_date, end_date):
        """
        Parameters
            start_date -> Date of booking's start (what is wished)
            end_date -> Date of booking's end (what is wished)

        Return true there are booked object during the given period.
        """
        booked_start_date = self.getStartDate()
        booked_end_date = self.getEndDate()
        if booked_start_date >= start_date and booked_start_date <= end_date:
            return True
        if booked_end_date >= start_date and booked_end_date <= end_date:
            return True
        if start_date <= booked_start_date and end_date >= booked_end_date:
            return True
        return False

    security.declarePublic('publishAutomatically')

    def publishAutomatically(self):
        """Return the option auto book"""
        review_mode = self.getBookingReviewMode()
        if review_mode == 'default':
            bcenter = self.getBookingCenter()
            review_mode = bcenter.getBookingReviewMode()
        if review_mode == 'publish':
            return True
        return False

    security.declareProtected(permissions.ModifyPortalContent, 'canWrite')

    def canWrite(self, field):
        """Check if you can write this field"""
        permission = getattr(field, 'write_restricted_permission', None)
        if permission is not None:
            if not self.publishAutomatically():
                wtool = getToolByName(self, 'portal_workflow')
                mtool = getToolByName(self, 'portal_membership')
                review_state = wtool.getInfoFor(self, 'review_state')
                if review_state == 'booked':
                    return mtool.checkPermission(permission, self)
        return True

    security.declareProtected(permissions.View, 'widget')

    def widget(self, field_name, mode='view', field=None, **kwargs):
        """Returns the rendered widget
        """
        if mode == 'edit':
            if field is None:
                field = self.Schema()[field_name]
            if not self.canWrite(field):
                macro_path = 'plonebooking_macros'
                template = self.restrictedTraverse(path=macro_path)
                return template.macros['read_only_field']
        return BaseContent.widget(self, field_name, mode, field, **kwargs)

    security.declareProtected('View', 'getStartDate')

    def getStartDate(self):
        """Alias of start method"""
        return self.start()

    security.declareProtected(permissions.ModifyPortalContent, 'setStartDate')

    def setStartDate(self, value, **kwargs):
        """Mutator for start field"""
        field = self.getField('startDate')
        if not self.canWrite(field):
            return
        field.set(self, value, **kwargs)

    security.declareProtected('View', 'getEndDate')

    def getEndDate(self):
        """Alias of end method"""
        return self.end()

    security.declareProtected(permissions.ModifyPortalContent, 'setEndDate')

    def setEndDate(self, value, **kwargs):
        """Mutator for end field"""
        field = self.getField('endDate')
        if not self.canWrite(field):
            return
        field.set(self, value, **kwargs)

    security.declarePrivate('setDefaults')

    def setDefaults(self):
        """Set field values to the default values
        """
        BaseContent.setDefaults(self)
        default_method = getattr(self, 'booking_defaults', self.restrictedTraverse('@@defaultFieldValues', None))
        if default_method is not None:
            kwargs = default_method()
            if type(kwargs) is DictionaryType:
                self.edit(**kwargs)
        return

    security.declareProtected('View', 'post_validate')

    def post_validate(self, REQUEST, errors):
        """Validate booked objects"""
        request = self.REQUEST
        response = request.RESPONSE
        ptool = getToolByName(self, 'portal_properties')
        charset = ptool.site_properties.default_charset
        start_date = DateTime(REQUEST.get('startDate'))
        end_date = DateTime(REQUEST.get('endDate'))
        booked_object_uid = self.getBookedObjectUID()
        booking_brains = self.getBookingBrains(start_date=start_date, end_date=end_date, getBookedObjectUID=booked_object_uid, review_state=('pending',
                                                                                                                                             'booked'))
        obj_path = ('/').join(self.getPhysicalPath())
        if end_date <= start_date:
            response.setHeader('Content-type', 'text/html; charset=%s' % charset)
            msg_id = 'message_end_date_before_start'
            msg_default = 'End date has to be strictly after start date.'
            msg = i18n.translate(I18N_DOMAIN, msg_id, context=self, default=msg_default)
            errors['endDate'] = msg
        if booking_brains:
            if len(booking_brains) == 1:
                brain_path = booking_brains[0].getPath()
                if obj_path == brain_path:
                    return
            response.setHeader('Content-type', 'text/html; charset=%s' % charset)
            msg_id = 'message_date_already_booked'
            msg_default = 'An object is already booked at this date.'
            msg = i18n.translate(I18N_DOMAIN, msg_id, context=self, default=msg_default)
            errors['startDate'] = msg
            errors['endDate'] = msg

    security.declareProtected('View', 'getNonEmptyTitle')

    def getNonEmptyTitle(self, **kwargs):
        """
        Returns original title of booking if exists otherwise returns a defautl title.
        """
        value = self.getField('title').get(self, **kwargs)
        if not value:
            btool = getToolByName(self, 'portal_booking')
            return btool.getBookingDefaultTitle()
        return value

    def _testBookingPeriod(self, start_ts, end_ts):
        booked_object_uid = self.getBookedObjectUID()
        booking_brains = self.getBookingBrains(start_date=start_ts, end_date=end_ts, getBookedObjectUID=booked_object_uid, review_state=('pending',
                                                                                                                                         'booked'))
        for booking in [ brain.getObject() for brain in booking_brains ]:
            if booking != self:
                return False

        return True

    security.declareProtected(permissions.ModifyPortalContent, 'testBookingPeriod')

    def testBookingPeriod(self, REQUEST):
        """
            Test if there are no bookings on the new period defined on
            this booking
        """
        request = self.REQUEST
        response = request.RESPONSE
        errorMessages = ''
        kwargs = request.form
        ptool = getToolByName(self, 'portal_properties')
        charset = ptool.site_properties.default_charset
        response.setHeader('Content-type', 'text/html; charset=%s' % charset)
        if kwargs.has_key('start_ts') and kwargs.has_key('end_ts'):
            start_ts = kwargs.pop('start_ts')
            end_ts = kwargs.pop('end_ts')
            if not self._testBookingPeriod(start_ts, end_ts):
                msg_id = 'message_date_already_booked'
                msg_default = 'An object is already booked at this date.'
                msg = i18n.translate(I18N_DOMAIN, msg_id, context=self, default=msg_default)
                errorMessages += '\n' + msg
        if errorMessages:
            btool = getToolByName(self, 'portal_booking')
            return '%s:%s%s' % (btool.zdt2ts(self.getStartDate()), btool.zdt2ts(self.getEndDate()), errorMessages)
        return True

    security.declareProtected(permissions.ModifyPortalContent, 'updateBooking')

    def updateBooking(self, REQUEST):
        """
            Allow to modify dates with ajax requests
        """
        request = self.REQUEST
        response = request.RESPONSE
        errorMessages = ''
        kwargs = request.form
        ptool = getToolByName(self, 'portal_properties')
        charset = ptool.site_properties.default_charset
        response.setHeader('Content-type', 'text/html; charset=%s' % charset)
        if kwargs.has_key('start_ts') and kwargs.has_key('end_ts'):
            start_ts = kwargs.pop('start_ts')
            end_ts = kwargs.pop('end_ts')
            if not self._testBookingPeriod(start_ts, end_ts):
                msg_id = 'message_date_already_booked'
                msg_default = 'An object is already booked at this date.'
                msg = i18n.translate(I18N_DOMAIN, msg_id, context=self, default=msg_default)
                errorMessages += '\n' + msg
            kwargs['startDate'] = DateTime(int(start_ts))
            kwargs['endDate'] = DateTime(int(end_ts))
        fieldsToValidate = ['fullName', 'phone', 'email']
        for fieldName in fieldsToValidate:
            if kwargs.has_key(fieldName):
                field = self.getField(fieldName)
                result = field.validate(kwargs[fieldName], self, errors={})
                if result:
                    errorMessages += '\n' + result

        if errorMessages:
            btool = getToolByName(self, 'portal_booking')
            return '%s:%s%s' % (btool.zdt2ts(self.getStartDate()), btool.zdt2ts(self.getEndDate()), errorMessages)
        else:
            ftool = getToolByName(self, 'portal_factory')
            try:
                new_context = ftool.doCreate(self, self.getId())
            except AttributeError:
                new_context = self

            start_date = kwargs.pop('startDate', None)
            if start_date is not None:
                new_context.setStartDate(start_date)
            end_date = kwargs.pop('endDate', None)
            if end_date is not None:
                new_context.setEndDate(end_date)
            new_context.processForm(values=kwargs)
            return True
        return

    security.declareProtected(permissions.ModifyPortalContent, 'updateStatus')

    def updateStatus(self, REQUEST):
        """
            Allow to book and delete from ajax requests
        """
        action = str(self.REQUEST.form.get('workflow_action'))
        if action == 'book' or action == 'cancel':
            wf_tool = getToolByName(self, 'portal_workflow')
            wf_tool.doActionFor(self, action)
        return True


registerType(Booking, PROJECTNAME)