# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-fat/egg/sc/social/viewcounter/interfaces.py
# Compiled at: 2010-08-18 13:21:09
from zope import schema
from zope.interface import Interface
from sc.social.viewcounter import MessageFactory as _

class IPageView(Interface):
    """ A single page view -- when a user access one content in our site
    """
    __module__ = __name__
    object_uid = schema.ASCIILine(title=_('Object UID'), required=True)
    object_path = schema.ASCIILine(title=_('Object path'), required=True)
    object_type = schema.TextLine(title=_('Portal type'), required=True)
    access_datetime = schema.Datetime(title=_('Access date'), required=True, readonly=True)
    user_ip = schema.TextLine(title=_('User IP address'), required=True)
    username = schema.TextLine(title=_('Username'), required=True)


class IReports(Interface):
    """ Reports interface
    """
    __module__ = __name__

    def invalidateCache(self):
        pass

    def viewsLastHour(self):
        pass

    def viewsLastDay(self):
        pass

    def viewsLastWeek(self):
        pass

    def viewsLastMonth(self):
        pass

    def viewsLastYear(self):
        pass

    def viewsAllTime(self):
        pass