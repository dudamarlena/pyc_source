# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/groupware/noteobject.py
# Compiled at: 2012-10-12 07:02:39
import os
from xml.sax.saxutils import escape
from coils.core import BLOBManager
from coils.net import DAVObject
from groupwareobject import GroupwareObject

class NoteObject(DAVObject, GroupwareObject):

    def __init__(self, parent, name, **params):
        DAVObject.__init__(self, parent, name, **params)

    def get_property_webdav_getcontenttype(self):
        if self.context.user_agent_description['webdav']['supportsMEMOs']:
            return 'calendar/ics'
        else:
            return 'text/plain'

    def get_property_caldav_calendar_data(self):
        return escape(self.get_representation())

    def get_property_webdav_getcontentlength(self):
        dentry = self.dir_entry
        if dentry:
            if self.context.user_agent_description['webdav']['supportsMEMOs'] and dentry.ics_size:
                return dentry.ics_size
            if dentry.file_size:
                return dentry.file_size
        if self.context.user_agent_description['webdav']['supportsMEMOs']:
            payload = self.get_representation()
            if payload:
                return unicode(len(payload))
        elif self.entity:
            handle = self.context.run_command('note::get-handle', id=self.entity.object_id)
            handle.seek(0, os.SEEK_END)
            size = handle.tell()
            BLOBManager.Close(handle)
            return size
        return '0'

    def get_property_webdav_owner(self):
        return ('<D:href>{0}</D:href>').format(self.get_appropriate_href(('/dav/Contacts/{0}.vcf').format(self.entity.owner_id)))

    def do_GET(self):
        if self.context.user_agent_description['webdav']['supportsMEMOs']:
            DAVObject.do_GET(self)
        else:
            handle = self.context.run_command('note::get-handle', id=self.entity.object_id)
            self.request.stream_response(200, stream=handle, mimetype=self.entity.get_mimetype(), headers={'etag': self.get_property_webdav_getetag()})