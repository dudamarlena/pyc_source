# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/net/foundation/dateobject.py
# Compiled at: 2012-10-12 07:02:39
import datetime, vobject
from StringIO import StringIO
from time import strftime
from davobject import DAVObject
from bufferedwriter import BufferedWriter

class DateObject(DAVObject):

    def __init__(self, parent, name, **params):
        DAVObject.__init__(self, parent, name, **params)

    def get_property_getetag(self):
        return unicode(('{0}:{1}:{2}').format(self.prefix, self.entity.object_id, self.entity.version))

    def get_property_webdav_displayname(self):
        return self.display_name

    def get_property_webdav_getcontentlength(self):
        return unicode(len(self.get_representation()))

    def get_property_webdav_getcontenttype(self):
        return 'text/calendar'

    def get_property_webdav_getlastmodified(self):
        return self.most_recent_entry_datetime.strftime('%a, %d %b %Y %H:%M:%S GMT')

    def _load_contents(self):
        return True

    @property
    def date_value(self):
        if hasattr(self, 'date'):
            return self.date
        return datetime.date.today()

    @property
    def comment_value(self):
        if hasattr(self, 'comment'):
            return self.comment_value
        return ''

    def get_representation(self):
        if hasattr(self, 'representation'):
            return self.representation
        calendar = vobject.iCalendar()
        event = calendar.add('vevent')
        event.add('uid').value = ('{0}:{1}:{2}').format(self.prefix, self.entity.object_id)
        event.add('description').value = self.comment_value
        event.add('status').value = 'CONFIRMED'
        event.add('summary').value = self.title
        event.add('dtstamp').value = datetime.datetime.now()
        event.add('dtstart').value = self.date_value
        event.add('X-MICROSOFT-CDO-INSTTYPE').value = '0'
        event.add('x-coils-appointment-kind').value = 'static'
        event.add('x-coils-post-duration').value = '0'
        event.add('x-coils-prior-duration').value = '0'
        event.add('x-coils-conflict-disable').value = 'TRUE'
        event.add('class').value = 'PUBLIC'
        event.add('X-MICROSOFT-CDO-IMPORTANCE').value = '0'
        event.add('X-MICROSOFT-CDO-BUSYSTATUS').value = 'FREE'
        event.add('X-MICROSOFT-CDO-ALLDAYEVENT').value = 'TRUE'
        event.add('X-MICROSOFT-CDO-INTENDEDSTATUS').value = 'FREE'
        event.add('transp').value = 'TRANSPARENT'
        self.representation = calendar.serialize()
        return self.representation

    def do_GET(self):
        payload = self.get_representation()
        if payload is not None:
            self.request.simple_response(200, data=unicode(payload), mimetype=self.get_property_webdav_getcontenttype(), headers={'ETag': self.get_property_getetag()})
            return
        else:
            raise NoSuchPathException(('{0} not found').format(self.name))
            return