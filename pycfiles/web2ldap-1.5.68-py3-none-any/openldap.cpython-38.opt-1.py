# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/openldap.py
# Compiled at: 2020-02-15 12:48:20
# Size of source mod 2**32: 16987 bytes
"""
web2ldap plugin classes for OpenLDAP
"""
import re, binascii
import pyasn1.codec.ber as ber_decoder
import ldap0.ldapurl, ldap0.controls, ldap0.openldap
from ldap0.controls import KNOWN_RESPONSE_CONTROLS
import web2ldapcnf, web2ldap.app.gui
from web2ldap.app.schema.syntaxes import AuthzDN, BindDN, DirectoryString, DistinguishedName, DynamicDNSelectList, IA5String, Integer, LDAPUrl, LDAPv3ResultCode, MultilineText, NotBefore, OctetString, SelectList, Uri, UUID, syntax_registry
from web2ldap.ldaputil.oidreg import OID_REG
from web2ldap.app.plugins.quirks import NamingContexts

class CSNSid(IA5String):
    oid = '1.3.6.1.4.1.4203.666.11.2.4'
    oid: str
    desc = 'change sequence number SID (CSN SID)'
    desc: str
    minLen = 3
    minLen: int
    maxLen = 3
    maxLen: int
    reObj = re.compile('^[a-fA-F0-9]{3}$')


class CSN(IA5String):
    oid = '1.3.6.1.4.1.4203.666.11.2.1'
    oid: str
    desc = 'change sequence number (CSN)'
    desc: str
    minLen = 40
    minLen: int
    maxLen = 40
    maxLen: int
    reObj = re.compile('^[0-9]{14}\\.[0-9]{6}Z#[a-fA-F0-9]{6}#[a-fA-F0-9]{3}#[a-fA-F0-9]{6}$')


syntax_registry.reg_at(CSN.oid, [
 '1.3.6.1.4.1.4203.666.1.25',
 '1.3.6.1.4.1.4203.666.1.7',
 '1.3.6.1.4.1.4203.666.1.13',
 'contextCSN', 'entryCSN', 'namingCSN'])
syntax_registry.reg_at(NamingContexts.oid, [
 '1.3.6.1.4.1.4203.1.12.2.3.2.0.10'])

class OlcDbIndex(DirectoryString):
    oid = 'OlcDbIndex-oid'
    oid: str
    desc = 'OpenLDAP indexing directive'
    desc: str
    reObj = re.compile('^[a-zA-Z]?[a-zA-Z0-9.,;-]* (pres|eq|sub)(,(pres|eq|sub))*$')


syntax_registry.reg_at(OlcDbIndex.oid, [
 '1.3.6.1.4.1.4203.1.12.2.3.2.0.2'])

class OlcSubordinate(SelectList):
    oid = 'OlcSubordinate-oid'
    oid: str
    desc = 'Indicates whether backend is subordinate'
    desc: str
    attr_value_dict = {'':'-/- (FALSE)',  'TRUE':'TRUE', 
     'advertise':'advertise'}


syntax_registry.reg_at(OlcSubordinate.oid, [
 '1.3.6.1.4.1.4203.1.12.2.3.2.0.15'])

class OlcRootDN(BindDN):
    oid = 'OlcRootDN-oid'
    oid: str
    desc = 'The rootdn in the database'
    desc: str
    default_rdn = 'cn=admin'

    def formValue(self) -> str:
        form_value = BindDN.formValue(self)
        try:
            olc_suffix = self._entry['olcSuffix'][0].decode()
        except KeyError:
            pass
        else:
            if not (form_value and form_value.endswith(olc_suffix)):
                try:
                    form_value = ','.join((self.default_rdn, olc_suffix))
                except KeyError:
                    pass
                else:
                    return form_value


syntax_registry.reg_at(OlcRootDN.oid, [
 '1.3.6.1.4.1.4203.1.12.2.3.2.0.8'])

class OlcMultilineText(MultilineText):
    oid = 'OlcMultilineText-oid'
    oid: str
    desc = 'OpenLDAP multiline configuration strings'
    desc: str
    cols = 90
    minInputRows = 3

    def display(self, valueindex=0, commandbutton=False) -> str:
        return '<code>%s</code>' % MultilineText.display(self, valueindex, commandbutton)


syntax_registry.reg_at(OlcMultilineText.oid, [
 '1.3.6.1.4.1.4203.1.12.2.3.0.1',
 '1.3.6.1.4.1.4203.1.12.2.3.0.6',
 '1.3.6.1.4.1.4203.1.12.2.3.0.8'])

class OlcSyncRepl(OlcMultilineText, LDAPUrl):
    oid = 'OlcSyncRepl-oid'
    oid: str
    desc = 'OpenLDAP syncrepl directive'
    desc: str
    minInputRows = 5

    def __init__(self, app, dn: str, schema, attrType: str, attrValue: bytes, entry=None):
        OlcMultilineText.__init__(self, app, dn, schema, attrType, attrValue, entry)

    def display(self, valueindex=0, commandbutton=False) -> str:
        return commandbutton and self._av or OlcMultilineText.display(self, valueindex, commandbutton)
        srd = ldap0.openldap.SyncReplDesc(self._av)
        return ' '.join((
         OlcMultilineText.display(self, valueindex, commandbutton),
         web2ldap.app.gui.ldap_url_anchor(self._app, srd.ldap_url())))


syntax_registry.reg_at(OlcSyncRepl.oid, [
 '1.3.6.1.4.1.4203.1.12.2.3.2.0.11'])

class OlmSeeAlso(DynamicDNSelectList):
    oid = 'OlmSeeAlso-oid'
    oid: str
    desc = 'DN of a overlase or database object in back-monitor'
    desc: str
    ldap_url = 'ldap:///_?monitoredInfo?sub?(&(objectClass=monitoredObject)(|(entryDN:dnOneLevelMatch:=cn=Databases,cn=Monitor)(entryDN:dnOneLevelMatch:=cn=Overlays,cn=Monitor)(entryDN:dnOneLevelMatch:=cn=Backends,cn=Monitor)))'


syntax_registry.reg_at((OlmSeeAlso.oid),
  [
 '2.5.4.34'],
  structural_oc_oids=[
 '1.3.6.1.4.1.4203.666.3.16.8'])

class OlcPPolicyDefault(DynamicDNSelectList, DistinguishedName):
    oid = 'OlcPPolicyDefault-oid'
    oid: str
    desc = 'DN of a pwdPolicy object for uncustomized objects'
    desc: str
    ldap_url = 'ldap:///_?cn?sub?(objectClass=pwdPolicy)'

    def __init__(self, app, dn: str, schema, attrType: str, attrValue: bytes, entry=None):
        DynamicDNSelectList.__init__(self, app, dn, schema, attrType, attrValue, entry)

    def _validate(self, attrValue: bytes) -> bool:
        return DynamicDNSelectList._validate(self, attrValue)


syntax_registry.reg_at(OlcPPolicyDefault.oid, [
 '1.3.6.1.4.1.4203.1.12.2.3.3.12.1'])

class OlcMemberOfDangling(SelectList):
    oid = 'OlcMemberOfDangling-oid'
    oid: str
    desc = 'Behavior in case of dangling references during modification'
    desc: str
    attr_value_dict = {'':'-/-',  'ignore':'ignore', 
     'drop':'drop', 
     'error':'error'}


syntax_registry.reg_at(OlcMemberOfDangling.oid, [
 '1.3.6.1.4.1.4203.1.12.2.3.3.18.1'])
syntax_registry.reg_at(NotBefore.oid, [
 '1.3.6.1.4.1.4203.666.11.5.1.2', 'reqStart',
 '1.3.6.1.4.1.4203.666.11.5.1.3', 'reqEnd'])

class AuditContext(NamingContexts):
    oid = 'AuditContext'
    oid: str
    desc = 'OpenLDAP DN pointing to audit naming context'
    desc: str

    def display(self, valueindex=0, commandbutton=False) -> str:
        r = [DistinguishedName.display(self, valueindex, commandbutton)]
        if commandbutton:
            r.extend([
             self._app.anchor('searchform',
               'Search', [
              (
               'dn', self.av_u),
              (
               'scope', str(ldap0.SCOPE_ONELEVEL))],
               title='Go to search form for audit log'),
             self._app.anchor('search',
               'List all', [
              (
               'dn', self.av_u),
              ('filterstr', '(objectClass=auditObject)'),
              (
               'scope', str(ldap0.SCOPE_ONELEVEL))],
               title='List audit log entries of all operations'),
             self._app.anchor('search',
               'List writes', [
              (
               'dn', self.av_u),
              ('filterstr', '(objectClass=auditWriteObject)'),
              (
               'scope', str(ldap0.SCOPE_ONELEVEL))],
               title='List audit log entries of all write operations')])
        return web2ldapcnf.command_link_separator.join(r)


syntax_registry.reg_at(AuditContext.oid, [
 '1.3.6.1.4.1.4203.666.11.5.1.30', 'auditContext',
 '1.3.6.1.4.1.4203.1.12.2.3.3.4.1'])

class ReqResult(LDAPv3ResultCode):
    oid = 'ReqResult-oid'
    oid: str


syntax_registry.reg_at(ReqResult.oid, [
 '1.3.6.1.4.1.4203.666.11.5.1.7', 'reqResult'])

class ReqMod(OctetString, DirectoryString):
    oid = 'ReqMod-oid'
    oid: str
    desc = 'List of modifications/old values'
    desc: str
    known_modtypes = {
     b'+', b'-', b'=', b'#', b''}

    def display(self, valueindex=0, commandbutton=False) -> str:
        if self._av == b':':
            return ':'
        try:
            mod_attr_type, mod_attr_rest = self._av.split(b':', 1)
            mod_type = mod_attr_rest[0:1].strip()
        except (ValueError, IndexError):
            return OctetString.display(self, valueindex, commandbutton)
        else:
            if mod_type not in self.known_modtypes:
                return OctetString.display(self, valueindex, commandbutton)
            elif len(mod_attr_rest) > 1:
                try:
                    mod_type, mod_attr_value = mod_attr_rest.split(b' ', 1)
                except ValueError:
                    return OctetString.display(self, valueindex, commandbutton)

            else:
                mod_attr_value = b''
            mod_attr_type_u = mod_attr_type.decode(self._app.ls.charset)
            mod_type_u = mod_type.decode(self._app.ls.charset)
            try:
                mod_attr_value.decode(self._app.ls.charset)
            except UnicodeDecodeError:
                return '%s:%s<br>\n<code>\n%s\n</code>\n' % (
                 self._app.form.utf2display(mod_attr_type_u),
                 self._app.form.utf2display(mod_type_u),
                 mod_attr_value.hex().upper())
            else:
                return DirectoryString.display(self, valueindex, commandbutton)
                raise ValueError


syntax_registry.reg_at(ReqMod.oid, [
 '1.3.6.1.4.1.4203.666.11.5.1.16', 'reqMod',
 '1.3.6.1.4.1.4203.666.11.5.1.17', 'reqOld'])

class ReqControls(IA5String):
    oid = '1.3.6.1.4.1.4203.666.11.5.3.1'
    oid: str
    desc = 'List of LDAPv3 extended controls sent along with a request'
    desc: str

    def display(self, valueindex=0, commandbutton=False) -> str:
        result_lines = [IA5String.display(self, valueindex, commandbutton)]
        _, rest = self.av_u.strip().split('}{', 1)
        if rest.endswith('}'):
            result_lines.append('Extracted:')
            ctrl_tokens = list(filter(None, [t.strip() for t in rest[:-1].split(' ')]))
            ctrl_type = ctrl_tokens[0]
            try:
                ctrl_name, _, _ = OID_REG[ctrl_type]
            except (KeyError, ValueError):
                try:
                    ctrl_name = KNOWN_RESPONSE_CONTROLS.get(ctrl_type).__class__.__name__
                except KeyError:
                    ctrl_name = None

            else:
                if ctrl_name:
                    result_lines.append(self._app.form.utf2display(ctrl_name))
                try:
                    ctrl_criticality = {'TRUE':True,  'FALSE':False}[ctrl_tokens[(ctrl_tokens.index('criticality') + 1)].upper()]
                except (KeyError, ValueError, IndexError):
                    ctrl_criticality = False
                else:
                    result_lines.append('criticality %s' % str(ctrl_criticality).upper())
            try:
                ctrl_value = binascii.unhexlify(ctrl_tokens[(ctrl_tokens.index('controlValue') + 1)].upper()[1:-1])
            except (KeyError, ValueError, IndexError):
                pass
            else:
                try:
                    decoded_control_value = ber_decoder.decode(ctrl_value)
                except Exception:
                    decoded_control_value = ctrl_value
                else:
                    result_lines.append('controlValue %s' % self._app.form.utf2display(repr(decoded_control_value)).replace('\n', '<br>'))
        return '<br>'.join(result_lines)


syntax_registry.reg_at(ReqControls.oid, [
 '1.3.6.1.4.1.4203.666.11.5.1.10', 'reqControls',
 '1.3.6.1.4.1.4203.666.11.5.1.11', 'reqRespControls'])

class ReqEntryUUID(UUID):
    oid = 'ReqEntryUUID-oid'
    oid: str

    def display(self, valueindex=0, commandbutton=False) -> str:
        display_value = UUID.display(self, valueindex, commandbutton)
        if not commandbutton:
            return display_value
        return web2ldapcnf.command_link_separator.join((
         display_value,
         self._app.anchor('search',
           'Search target', (
          (
           'dn', self._dn),
          (
           'filterstr',
           '(entryUUID=%s)' % self.av_u),
          (
           'search_root',
           str(self._app.ls.get_search_root(self._app.ls.uc_decode(self._entry['reqDN'][0])[0])))),
           title='Search entry by UUID')))


syntax_registry.reg_at(ReqEntryUUID.oid, [
 '1.3.6.1.4.1.4203.666.11.5.1.31', 'reqEntryUUID'])

class ReqSession(Integer):
    oid = 'ReqSession-oid'
    oid: str

    def display(self, valueindex=0, commandbutton=False) -> str:
        display_value = Integer.display(self, valueindex, commandbutton)
        if not commandbutton:
            return display_value
        return web2ldapcnf.command_link_separator.join((
         display_value,
         self._app.anchor('search',
           '&raquo;', (
          (
           'dn', self._dn),
          (
           'search_root', str(self._app.naming_context)),
          ('searchform_mode', 'adv'),
          ('search_attr', 'reqSession'),
          (
           'search_option', web2ldap.app.searchform.SEARCH_OPT_IS_EQUAL),
          (
           'search_string', self.av_u)),
           title='Search all audit entries with same session number')))


syntax_registry.reg_at(ReqSession.oid, [
 '1.3.6.1.4.1.4203.666.11.5.1.5', 'reqSession'])

class Authz(DirectoryString):
    oid = '1.3.6.1.4.1.4203.666.2.7'
    oid: str
    desc = 'OpenLDAP authz'
    desc: str


syntax_registry.reg_at(AuthzDN.oid, [
 'monitorConnectionAuthzDN',
 '1.3.6.1.4.1.4203.666.1.55.7',
 'reqAuthzID',
 '1.3.6.1.4.1.4203.666.11.5.1.6'])

class OpenLDAPACI(DirectoryString):
    oid = '1.3.6.1.4.1.4203.666.2.1'
    oid: str
    desc = 'OpenLDAP ACI'
    desc: str


class OpenLDAPSpecialBackendSuffix(NamingContexts):
    oid = 'OpenLDAPSpecialBackendSuffix-oid'
    oid: str
    desc = 'OpenLDAP special backend suffix'
    desc: str

    def _config_link(self):
        attr_type_u = self._at[:-7]
        try:
            config_context = self._app.ls.uc_decode(self._app.ls.rootDSE['configContext'][0])[0]
        except KeyError:
            return
        else:
            return self._app.anchor('search',
              'Config', (
             (
              'dn', config_context),
             (
              'scope', web2ldap.app.searchform.SEARCH_SCOPE_STR_ONELEVEL),
             (
              'filterstr',
              '(&(objectClass=olcDatabaseConfig)(olcDatabase=%s))' % attr_type_u)),
              title=('Search for configuration entry below %s' % config_context))


syntax_registry.reg_at(OpenLDAPSpecialBackendSuffix.oid, [
 'monitorContext', '1.3.6.1.4.1.4203.666.1.10',
 'configContext', '1.3.6.1.4.1.4203.1.12.2.1'])
syntax_registry.reg_at(Uri.oid, ['monitorConnectionListener'])
syntax_registry.reg_at(DistinguishedName.oid, [
 'entryDN',
 'reqDN'])
syntax_registry.reg_syntaxes(__name__)