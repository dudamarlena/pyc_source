# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/groupware/taskobject.py
# Compiled at: 2012-10-12 07:02:39
from xml.sax.saxutils import escape
import io, time
from datetime import datetime
from coils.core import *
from coils.net import *
from coils.net import DAVObject

class TaskObject(DAVObject):

    def __init__(self, parent, name, **params):
        DAVObject.__init__(self, parent, name, **params)

    def get_representation(self):
        if self._representation is None:
            self._representation = self.context.run_command('object::get-as-ics', object=self.entity)
        return self._representation

    def get_property_webdav_owner(self):
        return ('<D:href>{0}</D:href>').format(self.get_appropriate_href(('/dav/Contacts/{0}.vcf').format(self.entity.owner_id)))

    def get_property_caldav_calendar_data(self):
        return escape(self.get_representation())

    def get_property_webdav_contenttype(self):
        return 'calendar/ics'

    def get_property_caldav_calendar_data(self):
        return escape(self.get_representation())