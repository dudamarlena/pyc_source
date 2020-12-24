# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/groupware/contactobject.py
# Compiled at: 2012-10-12 07:02:39
from coils.net import DAVObject
from groupwareobject import GroupwareObject

class ContactObject(DAVObject, GroupwareObject):

    def __init__(self, parent, name, **params):
        DAVObject.__init__(self, parent, name, **params)

    def get_property_webdav_principal_url(self):
        return ('<D:href>{0}</D:href>').format(self.get_appropriate_href(('/dav/Contacts/{0}.vcf').format(self.entity.object_id)))

    def get_property_webdav_owner(self):
        return ('<D:href>{0}</D:href>').format(self.get_appropriate_href(('/dav/Contacts/{0}.vcf').format(self.entity.owner_id)))

    def get_property_webdav_group(self):
        return

    def get_property_webdav_group_membership(self):
        if self.entity.is_account:
            teams = self.context.run_command('team::get', member_id=self.entity.object_id)
            groups = []
            for team in teams:
                url = self.get_appropriate_href(('/dav/Teams/{0}.vcf').format(self.team.object_id))
                groups.append(('<D:href>{0}</D:href>').format(url))

            return ('').join(groups)
        else:
            return
            return

    def get_property_coils_first_name(self):
        return self.entity.first_name

    def get_property_coils_last_name(self):
        return self.entity.last_name

    def get_property_coils_file_as(self):
        return self.entity.file_as

    def get_property_coils_is_account(self):
        if self.entity.is_account:
            return 'true'
        return 'false'

    def get_property_coils_gender(self):
        if self.entity.gender is None:
            return 'unknown'
        else:
            return self.entity.gender.lower()

    def get_representation(self):
        if self._representation is None:
            self._representation = self.context.run_command('object::get-as-ics', object=self.entity)
        return self._representation