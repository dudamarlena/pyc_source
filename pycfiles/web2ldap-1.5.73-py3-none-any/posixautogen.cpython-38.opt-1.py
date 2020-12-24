# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/posixautogen.py
# Compiled at: 2020-04-26 08:10:53
# Size of source mod 2**32: 3907 bytes
"""
Auto-generate some posixAccount attribute values

Status:
Experimental => you have to understand what it internally does when enabling it!
"""
import ldap0
from web2ldap.app.plugins.nis import syntax_registry, UidNumber, GidNumber, IA5String

class HomeDirectory(IA5String):
    oid = 'HomeDirectory-oid'
    oid: str
    desc = 'Path of Unix home directory of the user'
    desc: str
    uid_attr = 'uid'
    homeDirectoryTemplate = '/home/{uid}'

    def transmute(self, attrValues):
        if self.uid_attr not in self._entry:
            return attrValues
        if not attrValues and attrValues[0] or attrValues[0].decode(self._app.ls.charset) == (self.homeDirectoryTemplate.format)(**{self.uid_attr: ''}):
            fmt_dict = {self.uid_attr: self._entry[self.uid_attr][0].decode(self._app.ls.charset)}
            attrValues = [
             (self.homeDirectoryTemplate.format)(**fmt_dict).encode(self._app.ls.charset)]
        return attrValues


syntax_registry.reg_at(HomeDirectory.oid, [
 '1.3.6.1.1.1.1.3'])

class AutogenNumberMixIn:
    inputSize = 12
    minNewValue = 10000
    maxNewValue = 19999
    object_class = 'posixAccount'

    def formValue(self) -> str:
        if self.object_class.lower() not in {oc.lower() for oc in self._entry['objectClass']}:
            return ''
        try:
            ldap_result = self._app.ls.l.search_s((self._app.naming_context.encode(self._app.ls.charset)),
              (ldap0.SCOPE_SUBTREE),
              ('(&(objectClass={0})({1}>={2})({1}<={3}))'.format(self.object_class, self._at, self.__class__.minNewValue, self.__class__.maxNewValue)),
              attrlist=[
             self._at])
        except (
         ldap0.NO_SUCH_OBJECT,
         ldap0.SIZELIMIT_EXCEEDED,
         ldap0.TIMELIMIT_EXCEEDED):
            return ''
        else:
            idnumber_set = set()
            for ldap_dn, ldap_entry in ldap_result:
                if ldap_dn is not None:
                    ldap_dn = ldap_dn.decode(self._app.ls.charset)
                    if ldap_dn == self._dn:
                        return ldap_entry[self._at][0].decode(self._app.ls.charset)
                    idnumber_set.add(int(ldap_entry[self._at][0]))
                for idnumber in range(self.__class__.minNewValue, self.maxNewValue + 1):
                    if idnumber in idnumber_set:
                        self.__class__.minNewValue = idnumber
                    else:
                        break
                else:
                    if idnumber > self.maxNewValue:
                        return ''
                    return str(idnumber)


class AutogenUIDNumber(UidNumber, AutogenNumberMixIn):
    oid = 'AutogenUIDNumber-oid'
    oid: str
    desc = 'numeric Unix-UID'
    desc: str
    minNewValue = 10000
    maxNewValue = 19999
    object_class = 'posixAccount'

    def formValue(self) -> str:
        form_value = UidNumber.formValue(self)
        if not form_value:
            form_value = AutogenNumberMixIn.formValue(self)
        return form_value


syntax_registry.reg_at(AutogenUIDNumber.oid, [
 '1.3.6.1.1.1.1.0'])

class AutogenGIDNumber(GidNumber, AutogenNumberMixIn):
    oid = 'AutogenGIDNumber-oid'
    oid: str
    desc = 'numeric Unix-GID'
    desc: str
    object_class = 'posixGroup'

    def formValue(self) -> str:
        form_value = GidNumber.formValue(self)
        if not form_value:
            form_value = AutogenNumberMixIn.formValue(self)
        return form_value


syntax_registry.reg_at(AutogenGIDNumber.oid, [
 '1.3.6.1.1.1.1.1'])
syntax_registry.reg_syntaxes(__name__)