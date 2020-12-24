# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joe/workspace/python/klient/src/django-caldav/django_caldav/utils.py
# Compiled at: 2014-08-22 06:39:00
from django.utils.encoding import smart_unicode
import lxml.builder as lb
from djangodav import utils
WebDAV_NS = utils.WEBDAV_NS
WebDAV_MAP = utils.WEBDAV_NSMAP
WebDAV = utils.D
CalDAV_NS = 'urn:ietf:params:xml:ns:caldav'
CalDAV_MAP = {'C': CalDAV_NS}
CalDAV = lb.ElementMaker(namespace=CalDAV_NS, nsmap=CalDAV_MAP)
CalendarServer_NS = 'http://calendarserver.org/ns/'
CalendarServer_MAP = {'CS': CalendarServer_NS}
CalendarServer = lb.ElementMaker(namespace=CalendarServer_NS, nsmap=CalendarServer_MAP)
url_join = utils.url_join

class iCalendar(object):

    @staticmethod
    def unicode(string_like):
        """
        Converts vStringLike iCalendar object  (f.e. vText) into unicode string
        """
        return ('{unicode}').format(unicode=smart_unicode(string_like))

    @staticmethod
    def datetime(datetime_like):
        """
        Converts vDatetimeLike iCalendar object (f.e. vDDDTypes) into timezone-aware datetime
        """
        return datetime_like.dt