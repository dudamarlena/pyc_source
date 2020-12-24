# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/apple.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 2022 bytes
"""
web2ldap plugin classes for attributes defined in apple.schema
"""
import web2ldap.app.searchform
from web2ldap.app.schema.syntaxes import XmlValue, UUID, DynamicValueSelectList, syntax_registry
syntax_registry.reg_at(UUID.oid, [
 '1.3.6.1.4.1.63.1000.1.1.1.1.20'])

class UUIDReference(DynamicValueSelectList, UUID):
    oid = 'UUIDReference-oid'
    oid: str
    ldap_url = 'ldap:///_?apple-generateduid,entryDN?sub?(apple-generateduid=*)'

    def display(self, valueindex=0, commandbutton=False) -> str:
        value_disp = self._app.form.utf2display(self.av_u)
        return ' '.join((
         value_disp,
         self._app.anchor('searchform',
           '&raquo;', (
          (
           'dn', self._dn),
          ('searchform_mode', 'adv'),
          ('search_attr', 'apple-generateduid'),
          (
           'search_option', web2ldap.app.searchform.SEARCH_OPT_IS_EQUAL),
          (
           'search_string', value_disp)),
           title='Search entry by UUID')))

    def formField(self) -> str:
        return DynamicValueSelectList.formField(self)


syntax_registry.reg_at(UUIDReference.oid, [
 '1.3.6.1.4.1.63.1000.1.1.1.14.7',
 '1.3.6.1.4.1.63.1000.1.1.1.14.10'])
syntax_registry.reg_at(XmlValue.oid, [
 '1.3.6.1.4.1.63.1000.1.1.1.19.6',
 '1.3.6.1.4.1.63.1000.1.1.1.17.1',
 '1.3.6.1.4.1.63.1000.1.1.1.14.8',
 '1.3.6.1.4.1.63.1000.1.1.1.1.9',
 '1.3.6.1.4.1.63.1000.1.1.1.1.10',
 '1.3.6.1.4.1.63.1000.1.1.1.1.16',
 '1.3.6.1.4.1.63.1000.1.1.1.1.13'])
syntax_registry.reg_syntaxes(__name__)