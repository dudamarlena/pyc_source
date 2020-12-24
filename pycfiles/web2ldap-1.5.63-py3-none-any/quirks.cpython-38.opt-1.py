# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/quirks.py
# Compiled at: 2019-11-25 07:11:40
# Size of source mod 2**32: 8118 bytes
"""
Special syntax and attribute type registrations for enforcing
standard-compliant behaviour even if current subschema of
a server is erroneous or could not be retrieved.
"""
import ldap0.ldapurl, web2ldap.app.searchform
from web2ldap.app.schema.syntaxes import syntax_registry, Audio, AuthzDN, Binary, Boolean, CountryString, DirectoryString, DistinguishedName, DomainComponent, JPEGImage, LDAPUrl, OctetString, OID, PhotoG3Fax, PostalAddress, RFC822Address, Uri, UTCTime
syntax_registry.reg_at(OID.oid, [
 '1.2.826.0.1050.11.0', 'ogSupportedProfile',
 '1.3.6.1.4.1.1466.101.120.13', 'supportedControl',
 '1.3.6.1.4.1.1466.101.120.7', 'supportedExtension',
 '1.3.6.1.4.1.4203.1.3.5', 'supportedFeatures',
 'supportedCapabilities'])
syntax_registry.reg_at(RFC822Address.oid, [
 '0.9.2342.19200300.100.1.3',
 '2.16.840.1.113730.3.1.13',
 '2.16.840.1.113730.3.1.17',
 '2.16.840.1.113730.3.1.30',
 '1.3.6.1.4.1.42.2.27.2.1.15',
 '2.16.840.1.113730.3.1.47',
 '1.2.840.113549.1.9.1'])
syntax_registry.reg_at(JPEGImage.oid, [
 '0.9.2342.19200300.100.1.60'])
syntax_registry.reg_at(Audio.oid, [
 '0.9.2342.19200300.100.1.55'])
syntax_registry.reg_at(PhotoG3Fax.oid, [
 '0.9.2342.19200300.100.1.7'])
syntax_registry.reg_at(Uri.oid, [
 '1.3.6.1.4.1.250.1.57'])
syntax_registry.reg_at(Boolean.oid, [
 '2.5.18.9'])
syntax_registry.reg_at(PostalAddress.oid, [
 '2.5.4.16',
 '2.5.4.26',
 '0.9.2342.19200300.100.1.39'])
syntax_registry.reg_at(LDAPUrl.oid, [
 '2.16.840.1.113730.3.1.34'])
syntax_registry.reg_at(UTCTime.oid, [
 '2.5.18.1',
 '2.5.18.2',
 'createtimestamp-oid',
 'modifytimestamp-oid'])
syntax_registry.reg_at(CountryString.oid, [
 'c',
 'countryName',
 '2.5.4.6'])
syntax_registry.reg_at(Binary.oid, [
 '2.16.840.1.113730.3.1.216',
 '2.16.840.1.113730.3.140'])
syntax_registry.reg_at(AuthzDN.oid, [
 '2.5.18.3',
 '2.5.18.4'])
syntax_registry.reg_at(DomainComponent.oid, [
 '0.9.2342.19200300.100.1.25',
 'dc',
 'domainComponent'])

class UserPassword(OctetString, DirectoryString):
    oid = 'UserPassword-oid'
    oid: str

    def display(self, valueindex=0, commandbutton=False) -> str:
        try:
            result = DirectoryString.display(self, valueindex, commandbutton)
        except UnicodeDecodeError:
            result = OctetString.display(self, valueindex, commandbutton)
        else:
            return result


syntax_registry.reg_at(UserPassword.oid, [
 '2.5.4.35'])

class NamingContexts(DistinguishedName):
    oid = 'NamingContexts-oid'
    oid: str
    desc = 'Naming contexts in rootDSE'
    desc: str
    ldap_url = 'ldap:///cn=cn=config?olcSuffix?one?(objectClass=olcDatabaseConfig)'

    def _config_link(self):
        config_context = None
        config_scope_str = None
        config_filter = None
        try:
            config_context = self._app.ls.uc_decode(self._app.ls.rootDSE['configContext'][0])[0]
        except KeyError:
            try:
                _ = self._app.ls.rootDSE['ds-private-naming-contexts']
            except KeyError:
                pass
            else:
                config_context = 'cn=Backends,cn=config'
                config_filter = '(&(objectClass=ds-cfg-backend)(ds-cfg-base-dn=%s))' % self.av_u
                config_scope_str = web2ldap.app.searchform.SEARCH_SCOPE_STR_ONELEVEL
        else:
            config_filter = '(&(objectClass=olcDatabaseConfig)(olcSuffix=%s))' % self.av_u
            config_scope_str = web2ldap.app.searchform.SEARCH_SCOPE_STR_ONELEVEL
        if config_context:
            if config_scope_str:
                if config_filter:
                    return self._app.anchor('search',
                      'Config', (
                     (
                      'dn', config_context),
                     (
                      'scope', config_scope_str),
                     (
                      'filterstr', config_filter)),
                      title=('Search for configuration entry below %s' % config_context))

    def _monitor_link(self):
        monitor_context = None
        monitor_scope_str = None
        monitor_filter = None
        try:
            _ = self._app.ls.rootDSE['monitorContext']
        except KeyError:
            try:
                _ = self._app.ls.rootDSE['ds-private-naming-contexts']
            except KeyError:
                pass
            else:
                monitor_context = 'cn=monitor'
                monitor_filter = '(&(objectClass=ds-backend-monitor-entry)(ds-backend-base-dn=%s))' % self.av_u
                monitor_scope_str = web2ldap.app.searchform.SEARCH_SCOPE_STR_ONELEVEL
        else:
            monitor_context = 'cn=Databases,cn=Monitor'
            monitor_filter = '(&(objectClass=monitoredObject)(namingContexts=%s))' % self.av_u
            monitor_scope_str = web2ldap.app.searchform.SEARCH_SCOPE_STR_ONELEVEL
        if monitor_context:
            if monitor_scope_str:
                if monitor_filter:
                    return self._app.anchor('search',
                      'Monitor', (
                     (
                      'dn', monitor_context),
                     (
                      'scope', monitor_scope_str),
                     (
                      'filterstr', monitor_filter)),
                      title=('Search for monitoring entry below %s' % monitor_context))

    def _additional_links(self):
        r = DistinguishedName._additional_links(self)
        r.append(self._app.anchor('search', 'Down', (
         (
          'dn', self.av_u),
         (
          'scope', web2ldap.app.searchform.SEARCH_SCOPE_STR_ONELEVEL),
         ('filterstr', '(objectClass=*)'))))
        r.append(self._app.anchor('dit', 'Tree', (
         (
          'dn', self.av_u),)))
        config_link = self._config_link()
        if config_link:
            r.append(config_link)
        monitor_link = self._monitor_link()
        if monitor_link:
            r.append(monitor_link)
        return r


syntax_registry.reg_at(NamingContexts.oid, [
 'namingContexts',
 '1.3.6.1.4.1.1466.101.120.5'])

class AltServer(LDAPUrl):
    oid = 'AltServer-oid'
    oid: str
    desc = 'LDAP URIs of alternative server(s)'
    desc: str

    def _command_ldap_url(self, ldap_url):
        ldap_url_obj = ldap0.ldapurl.LDAPUrl(ldapUrl=ldap_url)
        ldap_url_obj.who = self._app.ls.who
        ldap_url_obj.scope = ldap0.ldapurl.LDAP_SCOPE_BASE
        ldap_url_obj.cred = None
        return ldap_url_obj


syntax_registry.reg_at(AltServer.oid, [
 'altServer',
 '1.3.6.1.4.1.1466.101.120.6'])
syntax_registry.reg_syntaxes(__name__)