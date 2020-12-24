# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\PloneBooking\browser\export.py
# Compiled at: 2008-11-19 15:28:58
__doc__ = '\n'
import csv, cStringIO
from zope.component import getUtility
from zope.interface import implements
from DateTime import DateTime
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.PloneBooking.interfaces import IBookingExporter
from Products.PloneBooking import PloneBookingFactory as _
from zope.i18n.interfaces import ITranslationDomain, INegotiator

class BookingExporter:
    """
        Basic implementation of a Booking exporter.
        You can orverride this implementation by using some
        ZCML in an overrides.zcml
    """
    __module__ = __name__
    implements(IBookingExporter)

    def getFields(self):
        """
            Return the labels of all the fields for this export
        """
        return [
         _('label_booking_user_full_name', 'Full Name'), _('label_booking_user_phone', 'Phone'), _('label_booking_user_email', 'Email'), _('label_booking_start_date', 'Booking start date'), _('label_booking_end_date', 'Booking end date')]

    def getValues(self, brains):
        """
            Return a list of values associated with this brain.
        """
        results = []
        for brain in brains:
            booking = brain.getObject()
            results.append((booking.getFullName(), booking.getPhone(), booking.getEmail(), booking.getStartDate(), booking.getEndDate()))

        return results

    def getPortalType(self):
        """
            Return the portal to use for the request
        """
        return 'Booking'

    def getEncoding(self):
        """
            Get the encoding that will be used for the CSV export
        """
        return 'utf-8'


class Export(BrowserView):
    """
        Export the bookables of a selected ressource (ressource type given
        in the context)
    """
    __module__ = __name__

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.exporter = getUtility(IBookingExporter)
        self.catalog = getToolByName(self.context, 'portal_catalog')
        if request.form.get('export_type') == 'csv':
            self.__call__ = self.exportToCsv
        elif request.form.get('export_type') == 'html':
            self.values = self.getValues()
            if len(self.values) < 1:
                self.context.plone_utils.addPortalMessage(_('info_no_results', 'There is no booking matching your criteria.'), 'info')
        else:
            self.values = None
        return

    def getBrains(self):
        """
            Get the brains associated with the export request
        """
        query = {'portal_type': self.exporter.getPortalType(), 'path': ('/').join(self.context.getPhysicalPath()), 'start': {'query': self.start, 'range': 'min'}, 'end': {'query': self.end, 'range': 'max'}}
        brains = self.catalog(**query)
        return brains

    def getFields(self):
        """
            Return translated fields in a list of unicode
        """
        fields = getUtility(IBookingExporter).getFields()
        return [ self.context.translate(field, domain=field.domain) for field in fields ]

    def getValues(self):
        try:
            self.start = DateTime(int(self.context.request.form['ts_start']))
            self.end = DateTime(int(self.context.request.form['ts_end']))
        except KeyError:
            self.context.request.response.redirect(self.context.absolute_url() + '/export_form')

        if self.start + 6000 < self.end:
            self.context.plone_utils.addPortalMessage(_('error_range_too_large', 'Please enter a range that fits into 2 monthes.'), 'error')
            self.context.request.response.redirect(self.context.absolute_url() + '/export_form')
        return self.exporter.getValues(self.getBrains())

    def getEncoding(self):
        """
            Return the encoding of the CSV file
        """
        return getUtility(IBookingExporter).getEncoding()

    def exportToCsv(self):
        """
            Called only when the user select "CSV" export type
        """
        fields = self.getFields()
        values = self.getValues()
        stream = cStringIO.StringIO()
        writer = csv.writer(stream)
        encoding = self.getEncoding()
        writer.writerow([ field.encode(encoding) for field in fields ])
        writer.writerows(values)
        result = stream.getvalue()
        stream.close()
        response = self.context.request.response
        response.setHeader('Content-Type', 'text/csv')
        response.setHeader('Content-Encoding', encoding)
        response.setHeader('Content-Disposition', 'attachment; filename=booking-%s-%s-%s.csv' % (self.context.getId(), self.start.strftime('%Y%m%d'), self.end.strftime('%Y%m%d')))
        return result

    def exportToHtml(self):
        """
            Called by the page template, return a list of list containing all the
            fields to display
        """
        return self.values