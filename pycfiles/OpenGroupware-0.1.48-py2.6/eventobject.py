# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/groupware/eventobject.py
# Compiled at: 2012-10-12 07:02:39
from xml.sax.saxutils import escape
from coils.core import *
from coils.net import DAVObject

class EventObject(DAVObject):

    def __init__(self, parent, name, **params):
        DAVObject.__init__(self, parent, name, **params)
        if self.entity is None:
            raise CoilsException()
        elif isinstance(self.entity, Appointment):
            if self.entity.caldav_uid is None:
                self.location = ('/dav/Calendar/{0}.ics').format(self.entity.object_id)
            else:
                self.location = ('/dav/Calendar/{0}').format(self.entity.caldav_uid)
        elif isinstance(self.entity, Process):
            self.location = None
        return

    def get_property_webdav_displayname(self):
        if isinstance(self.entity, Appointment):
            if self.entity.title is None:
                return ('Appointment Id#{0}').format(self.entity.object_id)
            else:
                return escape(self.entity.title)
        else:
            if self.entity.route is not None:
                return escape(self.entity.route.name)
            else:
                return 'Unknwon'
        return

    def get_property_webdav_owner(self):
        return ('<D:href>{0}</D:href>').format(self.get_appropriate_href(('/dav/Contacts/{0}.vcf').format(self.entity.owner_id)))

    def get_property_webdav_group(self):
        return

    def get_property_caldav_calendar_data(self):
        return escape(self.get_representation())

    def get_representation(self):
        if self._representation is None:
            self._representation = self.context.run_command('object::get-as-ics', object=self.entity)
        if self.context.user_agent_description['webdav']['escapeGETs']:
            return escape(self._representation)
        else:
            return self._representation
            return