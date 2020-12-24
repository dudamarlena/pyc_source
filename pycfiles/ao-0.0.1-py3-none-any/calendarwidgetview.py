# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/anz/dashboard/browser/calendarwidgetview.py
# Compiled at: 2010-09-26 21:53:54
from math import ceil, floor
import time, cjson
from DateTime import DateTime
from Products.Five import BrowserView
from zope.interface import implements
from zope.component import getUtility
from Acquisition import aq_parent, aq_inner, aq_base
from zope.i18n import translate
from Products.PythonScripts.standard import url_quote_plus
from Products.CMFCore.utils import getToolByName
from plone.memoize.interfaces import ICacheChooser
from anz.dashboard.interfaces import ICalendarWidgetView
from anz.dashboard import MSG_FACTORY as _

class CalendarWidgetView(BrowserView):
    """ Calendar widget functions interface. """
    __module__ = __name__
    implements(ICalendarWidgetView)

    def getReviewStateString(self, retJson=True):
        """ Return event review state query string.
        
        @retJson
        format return value to json format or not( default True )
        
        @return a dict contains review state string:
        {
            success: True,
            msg: 'Get review state string success.',
            stateStr: '...'
        }
        
        """
        ret = {}
        ctool = getToolByName(self.context, 'portal_calendar')
        states = ctool.getCalendarStates()
        ret['success'] = True
        ret['msg'] = _('Get review state string success.')
        ret['stateStr'] = ('').join(map(lambda x: 'review_state=%s&amp;' % url_quote_plus(x), states))
        return retJson and cjson.encode(ret) or ret

    def events(self, start, end, cachetime=300, retJson=True):
        """ Return events involved in specific date range( [start,end) ).
        
        involved means event's time range overlapped with specific date range,
        greater and equal the start date and less then the end date.
        
        @param start
        start date of the time range( DateTime object or its string format )
        
        @param end
        end date of the time range( DateTime object or its string format )
        
        @retJson
        format return value to json format or not( default True )
        
        @return status of create process
        json data:
        {
            success: True,
            msg: 'Get events success.',
            events: {
                '20100201': [{
                    'title': 'event title',
                    'desc': 'event desc',
                    'start': 'start date',
                    'end': 'end date',
                    'url': 'event url',
                    'location': 'event location'
                },...],
                '20100202': [...],
                ...
                '20100207': [...]
            }
        }
        
        """
        request = self.request
        ret = {}
        try:
            if not isinstance(start, DateTime):
                start = DateTime(start)
            if not isinstance(end, DateTime):
                end = DateTime(end)
            start = self._getBeginAndEndTimes(start)[0]
            end = self._getBeginAndEndTimes(end)[1]
            days = int(ceil(end - start))
            events = {}
            for n in range(days):
                dt = start + n
                events[dt.strftime('%Y%m%d')] = []

            ctool = getToolByName(self.context, 'portal_calendar')
            catalog = getToolByName(self.context, 'portal_catalog')
            query = {'portal_type': ctool.getCalendarTypes(), 'review_state': ctool.getCalendarStates(), 'start': {'query': end, 'range': 'max'}, 'end': {'query': start, 'range': 'min'}, 'sort_on': 'start'}
            results = catalog.searchResults(query)
            for r in results:
                s = r.start
                e = r.end
                info = {'title': unicode(r.Title), 'desc': unicode(r.Description), 'start': r.start.strftime('%Y/%m/%d %H:%M:%S'), 'end': r.end.strftime('%Y/%m/%d %H:%M:%S'), 'url': r.getURL(), 'location': unicode(r.location)}
                if int(ceil(e - s)) > 1:
                    if s < start:
                        crossStart = 0
                    else:
                        crossStart = int(floor(s - start))
                    if e > end:
                        crossEnd = int(ceil(end - start))
                    else:
                        crossEnd = int(ceil(e - start))
                    for n in range(crossStart, crossEnd):
                        dt = start + n
                        events[dt.strftime('%Y%m%d')].append(info)

                else:
                    events[s.strftime('%Y%m%d')].append(info)

            ret['success'] = True
            ret['msg'] = translate(_('Get events success.'), context=request)
            ret['events'] = events
        except Exception, e:
            ret['success'] = False
            ret['msg'] = str(e)

        return retJson and cjson.encode(ret) or ret

    def _getBeginAndEndTimes(self, dt):
        year = dt.year()
        month = dt.month()
        day = dt.day()
        begin = DateTime('%d/%02d/%02d 00:00:00' % (year, month, day))
        end = DateTime('%d/%02d/%02d 23:59:59' % (year, month, day))
        return (
         begin, end)