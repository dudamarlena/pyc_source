# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/nis.py
# Compiled at: 2020-04-26 05:21:36
# Size of source mod 2**32: 6586 bytes
"""
web2ldap plugin classes for schema elements defined in RFC2307
"""
import re, web2ldap.app.searchform
from web2ldap.app.schema.syntaxes import DaysSinceEpoch, DNSDomain, DynamicValueSelectList, IA5String, Integer, IPHostAddress, IPServicePortNumber, MacAddress, SelectList, syntax_registry

class RFC2307BootParameter(IA5String):
    oid = '1.3.6.1.1.1.0.1'
    oid: str
    desc = 'RFC2307 Boot Parameter'
    desc: str
    reObj = None


class GidNumber(DynamicValueSelectList, Integer):
    oid = 'GidNumber-oid'
    oid: str
    desc = 'RFC2307: An integer uniquely identifying a group in an administrative domain'
    desc: str
    minValue = 0
    maxValue = 4294967295
    ldap_url = 'ldap:///_?gidNumber,cn?sub?(objectClass=posixGroup)'

    def _validate(self, attrValue: bytes) -> bool:
        return Integer._validate(self, attrValue)

    def display(self, valueindex=0, commandbutton=False) -> str:
        ocs = self._entry.object_class_oid_set()
        if 'posixAccount' in ocs or 'shadowAccount' in ocs:
            return DynamicValueSelectList.display(self, valueindex, commandbutton)
        else:
            res = [
             Integer.display(self, valueindex, commandbutton=False)]
            if not commandbutton:
                return res[0]
                if 'posixGroup' in ocs:
                    title = 'Search primary group members'
                    searchform_params = [
                     (
                      'dn', self._dn),
                     ('searchform_mode', 'adv'),
                     ('search_attr', 'objectClass'),
                     (
                      'search_option', web2ldap.app.searchform.SEARCH_OPT_IS_EQUAL),
                     ('search_string', 'posixAccount'),
                     ('search_attr', 'gidNumber'),
                     (
                      'search_option', web2ldap.app.searchform.SEARCH_OPT_IS_EQUAL),
                     (
                      'search_string', self.av_u)]
            else:
                title = None
            searchform_params = None
        if title:
            if searchform_params:
                res.append(self._app.anchor('searchform',
                  '&raquo;', searchform_params,
                  title=title))
        return ' '.join(res)

    def formField(self) -> str:
        ocs = self._entry.object_class_oid_set()
        if 'posixAccount' in ocs or 'shadowAccount' in ocs:
            return DynamicValueSelectList.formField(self)
        return Integer.formField(self)


syntax_registry.reg_at(GidNumber.oid, [
 '1.3.6.1.1.1.1.1'])

class MemberUID(IA5String, DynamicValueSelectList):
    oid = 'MemberUID-oid'
    oid: str
    desc = 'RFC2307 numerical UID of group member(s)'
    desc: str
    ldap_url = None

    def __init__(self, app, dn: str, schema, attrType: str, attrValue: bytes, entry=None):
        IA5String.__init__(self, app, dn, schema, attrType, attrValue, entry)
        if self.ldap_url:
            DynamicValueSelectList.__init__(self, app, dn, schema, attrType, attrValue, entry)

    def _validate(self, attrValue: bytes) -> bool:
        if self.ldap_url:
            return DynamicValueSelectList._validate(self, attrValue)
        return IA5String._validate(self, attrValue)

    def formField(self) -> str:
        if self.ldap_url:
            return DynamicValueSelectList.formField(self)
        return IA5String.formField(self)

    def display(self, valueindex=0, commandbutton=False) -> str:
        res = [
         IA5String.display(self, valueindex, commandbutton=False)]
        if commandbutton:
            res.append(self._app.anchor('searchform',
              '&raquo;', [
             (
              'dn', self._dn),
             (
              'filterstr',
              '(&(objectClass=posixAccount)(uid=%s))' % self._app.form.utf2display(self.av_u)),
             ('searchform_mode', 'exp')],
              title='Search for user entry'))
        return ' '.join(res)


syntax_registry.reg_at(MemberUID.oid, [
 '1.3.6.1.1.1.1.12'])

class RFC2307NISNetgroupTriple(IA5String):
    oid = '1.3.6.1.1.1.0.0'
    oid: str
    desc = 'RFC2307 NIS Netgroup Triple'
    desc: str
    reObj = re.compile('^\\([a-z0-9.-]*,[a-z0-9.-]*,[a-z0-9.-]*\\)$')


class UidNumber(Integer):
    oid = 'UidNumber-oid'
    oid: str
    desc = 'Numerical user ID for Posix systems'
    desc: str
    minValue = 0
    maxValue = 4294967295


syntax_registry.reg_at(UidNumber.oid, [
 '1.3.6.1.1.1.1.0'])

class Shell(SelectList):
    oid = 'Shell-oid'
    oid: str
    desc = 'Shell for user of Posix systems'
    desc: str
    attr_value_dict = {'/bin/sh':'Standard shell /bin/sh',  '/bin/bash':'Bourne-Again SHell /bin/bash', 
     '/bin/csh':'/bin/csh', 
     '/bin/tcsh':'/bin/tcsh', 
     '/bin/ksh':'Korn shell /bin/ksh', 
     '/bin/passwd':'Password change /bin/passwd', 
     '/bin/true':'/bin/true', 
     '/bin/false':'/bin/false', 
     '/bin/zsh':'Zsh /bin/zsh', 
     '/usr/bin/bash':'Bourne-Again SHell /usr/bin/bash', 
     '/usr/bin/csh':'/usr/bin/csh', 
     '/usr/bin/tcsh':'/usr/bin/csh', 
     '/usr/bin/ksh':'Korn shell /usr/bin/ksh', 
     '/usr/bin/zsh':'Zsh /usr/bin/zsh', 
     '/usr/sbin/nologin':'Login denied /usr/sbin/nologin'}


syntax_registry.reg_at(Shell.oid, [
 '1.3.6.1.1.1.1.4'])

class IpServiceProtocol(SelectList):
    oid = 'IpServiceProtocol-oid'
    oid: str
    desc = 'RFC 2307: IP service protocol'
    desc: str
    attr_value_dict = {'tcp':'tcp', 
     'udp':'udp'}


syntax_registry.reg_at(IpServiceProtocol.oid, [
 '1.3.6.1.1.1.1.16'])
syntax_registry.reg_at(IPHostAddress.oid, [
 '1.3.6.1.1.1.1.19',
 '1.3.6.1.1.1.1.20'])
syntax_registry.reg_at(DNSDomain.oid, [
 '1.3.6.1.1.1.1.30'])
syntax_registry.reg_at(DaysSinceEpoch.oid, [
 '1.3.6.1.1.1.1.10',
 '1.3.6.1.1.1.1.5'])
syntax_registry.reg_at(IPServicePortNumber.oid, [
 '1.3.6.1.1.1.1.15'])
syntax_registry.reg_at(MacAddress.oid, [
 '1.3.6.1.1.1.1.22'])
syntax_registry.reg_syntaxes(__name__)