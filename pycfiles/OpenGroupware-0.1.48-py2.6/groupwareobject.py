# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/groupware/groupwareobject.py
# Compiled at: 2012-10-12 07:02:39
from StringIO import StringIO
from coils.net import DAVObject

class GroupwareObject(object):

    def _get_privileges(self):
        data = self._ctx.access_manager.filter_by_access('r', data)

    def get_property_webdav_current_user_privilege_set(self):
        rights = self.context.access_manager.access_rights(self.context, self.entity)
        result = StringIO()
        result.write('<D:privilege>')
        if 'r' in rights:
            result.write('<read/>')
        if 'w' in rights:
            result.write('<D:write-content/>')
        result.write('<D:read-current-user-privilege-set/>')
        result.write('</D:privilege>')
        result = result.getvalue()
        return result

    def get_property_webdav_current_user_principal(self):
        url = self.get_appropriate_href(('/dav/Contacts/{0}.vcf').format(self.context.account_id))
        return ('<D:href>{0}.vcf</D:href>').format(url)

    def get_property_coils_version(self):
        if self.entity.version is None:
            return '0'
        else:
            return unicode(self.entity.version)

    def get_property_coils_objectid(self):
        return unicode(self.entity.object_id)