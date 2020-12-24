# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/csci/countdown/browser/countdownview.py
# Compiled at: 2009-09-15 08:55:39
from zope.interface import implements, Interface
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from csci.countdown import countdownMessageFactory as _
import time, datetime

class IcountdownView(Interface):
    """
    countdown view interface
    """
    __module__ = __name__

    def test():
        """ test method"""
        pass


class countdownView(BrowserView):
    """
    countdown browser view
    """
    __module__ = __name__
    implements(IcountdownView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def calc_diff(self):
        target_date = datetime.datetime(*time.strptime(self.context.target, '%d/%m/%y %H:%M')[:5])
        target_date = target_date.timetuple()
        today = datetime.datetime.utcnow()
        today = today.timetuple()
        togo = time.mktime(target_date) - time.mktime(today)
        togo = datetime.timedelta(seconds=togo)
        returned_dates = {}
        returned_dates['target'] = self.context.target
        returned_dates['days'] = togo.days
        togo_list = str(togo).split(' ')
        togo_list = togo_list[2].split(':')
        returned_dates['hours'] = togo_list[0]
        returned_dates['mins'] = togo_list[1]
        returned_dates['secs'] = togo_list[2]
        self.context.returned_dates = returned_dates
        raw_text = str(self.context.abovecount)
        raw_text = raw_text.replace('$daystogo$', str(togo.days))
        returned_dates['text'] = raw_text
        return returned_dates