# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/groupware/teamobject.py
# Compiled at: 2012-10-12 07:02:39
import io
from datetime import datetime
from coils.core import *
from coils.net import DAVObject

class TeamObject(DAVObject):

    def get_property_webdav_principal_url(self):
        return ('<href>/dav/Teams/{0}.vcf</href>').format(self.entity.object_id)

    def get_property_webdav_owner(self):
        return ('<href>{0}</href>').format(self.get_appropriate_href('/dav/Contacts/10000.vcf'))

    def get_property_webdav_group(self):
        return

    def get_property_webdav_group_member_set(self):
        members = []
        for member in self.entity.members:
            href = self.get_appropriate_href(('/dav/Contacts/{0}.vcf').format(member.child_id))
            members.append(('<href>{0}</href>').format(href))

        return ('').join(members)

    def get_representation(self):
        if self._representation is None:
            self._representation = self.context.run_command('object::get-as-ics', object=self.entity)
        return self._representation