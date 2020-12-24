# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/opends.py
# Compiled at: 2019-12-02 12:59:46
# Size of source mod 2**32: 19228 bytes
"""
web2ldap plugin classes for OpenDS and OpenDJ
"""
import re, ldap0
from ldap0.dn import DNObj
from web2ldap.app.schema.syntaxes import BindDN, DirectoryString, DynamicDNSelectList, MultilineText, OctetString, SelectList, syntax_registry
from web2ldap.app.plugins.x509 import Certificate
from web2ldap.app.plugins.groups import MemberOf
from web2ldap.app.plugins.quirks import NamingContexts
from web2ldap.app.schema import no_humanreadable_attr
syntax_registry.reg_at(MemberOf.oid, [
 '1.3.6.1.4.1.42.2.27.9.1.792'])

class OpenDSCfgPasswordPolicy(DynamicDNSelectList):
    oid = 'OpenDSCfgPasswordPolicy-oid'
    oid: str
    desc = 'DN of the ds-cfg-password-policy entry'
    desc: str
    ldap_url = 'ldap:///cn=Password Policies,cn=config?cn?one?(objectClass=ds-cfg-password-policy)'


syntax_registry.reg_at(OpenDSCfgPasswordPolicy.oid, [
 '1.3.6.1.4.1.26027.1.1.161',
 '1.3.6.1.4.1.26027.1.1.244'])

class OpenDSCfgPasswordStorageScheme(DynamicDNSelectList):
    oid = 'OpenDSCfgPasswordStorageScheme-oid'
    oid: str
    desc = 'DN of the ds-cfg-password-storage-scheme entry'
    desc: str
    ldap_url = 'ldap:///cn=Password Storage Schemes,cn=config?cn?one?(objectClass=ds-cfg-password-storage-scheme)'


syntax_registry.reg_at(OpenDSCfgPasswordStorageScheme.oid, [
 '1.3.6.1.4.1.26027.1.1.137'])

class OpenDSCfgPasswordGenerator(DynamicDNSelectList):
    oid = 'OpenDSCfgPasswordGenerator-oid'
    oid: str
    desc = 'DN of the ds-cfg-password-generator entry'
    desc: str
    ldap_url = 'ldap:///cn=Password Generators,cn=config?cn?one?(objectClass=ds-cfg-password-generator)'


syntax_registry.reg_at(OpenDSCfgPasswordGenerator.oid, [
 '1.3.6.1.4.1.26027.1.1.153'])

class OpenDSCfgIdentityMapper(DynamicDNSelectList):
    oid = 'OpenDSCfgIdentityMapper-oid'
    oid: str
    desc = 'DN of the ds-cfg-identity-mapper entry'
    desc: str
    ldap_url = 'ldap:///cn=Identity Mappers,cn=config?cn?one?(objectClass=ds-cfg-identity-mapper)'


syntax_registry.reg_at(OpenDSCfgIdentityMapper.oid, [
 '1.3.6.1.4.1.26027.1.1.113',
 '1.3.6.1.4.1.26027.1.1.114'])

class OpenDSCfgCertificateMapper(DynamicDNSelectList):
    oid = 'OpenDSCfgCertificateMapper-oid'
    oid: str
    desc = 'DN of the ds-cfg-certificate-mapper entry'
    desc: str
    ldap_url = 'ldap:///cn=Certificate Mappers,cn=config?cn?one?(objectClass=ds-cfg-certificate-mapper)'


syntax_registry.reg_at(OpenDSCfgCertificateMapper.oid, [
 '1.3.6.1.4.1.26027.1.1.262'])

class OpenDSCfgKeyManagerProvider(DynamicDNSelectList):
    oid = 'OpenDSCfgKeyManagerProvider-oid'
    oid: str
    desc = 'DN of the ds-cfg-key-manager-provider entry'
    desc: str
    ldap_url = 'ldap:///cn=Key Manager Providers,cn=config?cn?one?(objectClass=ds-cfg-key-manager-provider)'


syntax_registry.reg_at(OpenDSCfgKeyManagerProvider.oid, [
 '1.3.6.1.4.1.26027.1.1.263'])

class OpenDSCfgTrustManagerProvider(DynamicDNSelectList):
    oid = 'OpenDSCfgTrustManagerProvider-oid'
    oid: str
    desc = 'DN of the ds-cfg-trust-manager-provider entry'
    desc: str
    ldap_url = 'ldap:///cn=Trust Manager Providers,cn=config?cn?one?(objectClass=ds-cfg-trust-manager-provider)'


syntax_registry.reg_at(OpenDSCfgTrustManagerProvider.oid, [
 '1.3.6.1.4.1.26027.1.1.264'])

class OpenDSCfgSSLClientAuthPolicy(SelectList):
    oid = 'OpenDSCfgSSLClientAuthPolicy-oid'
    oid: str
    desc = 'Specifies the policy regarding client SSL certificates'
    desc: str
    attr_value_dict = {'disabled':'Client certificate is not requested',  'optional':'Client certificate is requested but not required', 
     'required':'Client certificate is required'}


syntax_registry.reg_at(OpenDSCfgSSLClientAuthPolicy.oid, [
 '1.3.6.1.4.1.26027.1.1.90'])

class OpenDSCfgSNMPSecurityLevel(SelectList):
    oid = 'OpenDSCfgSNMPSecurityLevel-oid'
    oid: str
    desc = 'Specifies the policy regarding client SSL certificates'
    desc: str
    attr_value_dict = {'authnopriv':'Authentication activated with no privacy.',  'authpriv':'Authentication with privacy activated.', 
     'noauthnopriv':'No security mechanisms activated.'}


syntax_registry.reg_at(OpenDSCfgSNMPSecurityLevel.oid, [
 '1.3.6.1.4.1.26027.1.1.452'])

class OpenDSCfgInvalidSchemaBehaviour(SelectList):
    oid = 'OpenDSCfgInvalidSchemaBehaviour-oid'
    oid: str
    desc = 'Specifies how OpenDS behaves in case of schema errors'
    desc: str
    attr_value_dict = {'reject':'reject',  'default':'default', 
     'accept':'accept', 
     'warn':'warn'}


syntax_registry.reg_at(OpenDSCfgInvalidSchemaBehaviour.oid, [
 '1.3.6.1.4.1.26027.1.1.31',
 '1.3.6.1.4.1.26027.1.1.88'])

class OpenDSCfgEtimeResolution(SelectList):
    oid = 'OpenDSCfgEtimeResolution-oid'
    oid: str
    desc = 'Specifies the resolution to use for operation elapsed processing time (etime) measurements.'
    desc: str
    attr_value_dict = {'milliseconds':'milliseconds',  'nanoseconds':'nanoseconds'}


syntax_registry.reg_at(OpenDSCfgEtimeResolution.oid, [
 '1.3.6.1.4.1.26027.1.1.442'])

class OpenDSCfgWritabilityMode(SelectList):
    oid = 'OpenDSCfgWritabilityMode-oid'
    oid: str
    desc = 'Specifies the kinds of write operations the Directory Server can process.'
    desc: str
    attr_value_dict = {'disabled':'all write operations are rejected',  'enabled':'all write operations are processed', 
     'internal-only':'write operations requested as internal/sync operations are processed'}


syntax_registry.reg_at(OpenDSCfgWritabilityMode.oid, [
 '1.3.6.1.4.1.26027.1.1.123'])

class OpenDSCfgCertificateValidationPolicy(SelectList):
    oid = 'OpenDSCfgCertificateValidationPolicy-oid'
    oid: str
    desc = 'Specifies the way client certs are checked in user entry.'
    desc: str
    attr_value_dict = {'always':"Always require matching peer certificate in user's entry",  'ifpresent':"Require one matching certificate if attribute exists in user's entry", 
     'never':"Peer certificate is not checked in user's entry at all"}


syntax_registry.reg_at(OpenDSCfgCertificateValidationPolicy.oid, [
 '1.3.6.1.4.1.26027.1.1.16'])

class OpenDSCfgAccountStatusNotificationType(SelectList):
    oid = 'OpenDSCfgAccountStatusNotificationType-oid'
    oid: str
    desc = 'Specifies when the generate a notification about account status'
    desc: str
    attr_value_dict = {'account-disabled':'User account has been disabled by an administrator',  'account-enabled':'User account has been enabled by an administrator', 
     'account-expired':'User authentication has failed because the account has expired', 
     'account-idle-locked':'User account has been locked because it was idle for too long', 
     'account-permanently-locked':'User account has been permanently locked after too many failed attempts', 
     'account-reset-locked':'User account has been locked, because the password had been reset by an administrator but not changed by the User within the required interval', 
     'account-temporarily-locked':'User account has been temporarily locked after too many failed attempts', 
     'account-unlocked':'User account has been unlocked by an administrator', 
     'password-changed':'User changes his/her own password', 
     'password-expired':'User authentication has failed because the password has expired', 
     'password-expiring':"Password expiration warning is encountered for user's password for the first time.", 
     'password-reset':"User's password was reset by an administrator."}


syntax_registry.reg_at(OpenDSCfgAccountStatusNotificationType.oid, [
 '1.3.6.1.4.1.26027.1.1.238'])

class OpenDSCfgSslProtocol(SelectList):
    oid = 'OpenDSCfgSslProtocol-oid'
    oid: str
    desc = 'Specifies the SSL/TLS protocols supported.'
    desc: str
    attr_value_dict = {'SSL':'any version of SSL',  'SSLv2':'SSL version 2 or higher', 
     'SSLv3':'SSL version 3', 
     'TLS':'any version of TLS', 
     'TLSv1':'TLS version 1.0 (RFC 2246)', 
     'TLSv1.1':'TLS version 1.1 (RFC 4346)'}


syntax_registry.reg_at(OpenDSCfgSslProtocol.oid, [
 '1.3.6.1.4.1.26027.1.1.391'])

class OpenDSCfgSslCipherSuite(SelectList):
    oid = 'OpenDSCfgSslCipherSuite-oid'
    oid: str
    desc = 'Specifies the used cipher suites.'
    desc: str
    attr_value_dict = {'SSL_DHE_DSS_EXPORT1024_WITH_DES_CBC_SHA':'SSL_DHE_DSS_EXPORT1024_WITH_DES_CBC_SHA',  'SSL_DHE_DSS_EXPORT1024_WITH_RC4_56_SHA':'SSL_DHE_DSS_EXPORT1024_WITH_RC4_56_SHA', 
     'SSL_DHE_DSS_EXPORT_WITH_DES40_CBC_SHA':'SSL_DHE_DSS_EXPORT_WITH_DES40_CBC_SHA', 
     'SSL_DHE_DSS_WITH_3DES_EDE_CBC_SHA':'SSL_DHE_DSS_WITH_3DES_EDE_CBC_SHA', 
     'SSL_DHE_DSS_WITH_DES_CBC_SHA':'SSL_DHE_DSS_WITH_DES_CBC_SHA', 
     'SSL_DHE_DSS_WITH_RC4_128_SHA':'SSL_DHE_DSS_WITH_RC4_128_SHA', 
     'SSL_DHE_RSA_EXPORT_WITH_DES40_CBC_SHA':'SSL_DHE_RSA_EXPORT_WITH_DES40_CBC_SHA', 
     'SSL_DHE_RSA_WITH_3DES_EDE_CBC_SHA':'SSL_DHE_RSA_WITH_3DES_EDE_CBC_SHA', 
     'SSL_DHE_RSA_WITH_DES_CBC_SHA':'SSL_DHE_RSA_WITH_DES_CBC_SHA', 
     'SSL_DH_DSS_EXPORT_WITH_DES40_CBC_SHA':'SSL_DH_DSS_EXPORT_WITH_DES40_CBC_SHA', 
     'SSL_DH_DSS_WITH_3DES_EDE_CBC_SHA':'SSL_DH_DSS_WITH_3DES_EDE_CBC_SHA', 
     'SSL_DH_DSS_WITH_DES_CBC_SHA':'SSL_DH_DSS_WITH_DES_CBC_SHA', 
     'SSL_DH_RSA_EXPORT_WITH_DES40_CBC_SHA':'SSL_DH_RSA_EXPORT_WITH_DES40_CBC_SHA', 
     'SSL_DH_RSA_WITH_3DES_EDE_CBC_SHA':'SSL_DH_RSA_WITH_3DES_EDE_CBC_SHA', 
     'SSL_DH_RSA_WITH_DES_CBC_SHA':'SSL_DH_RSA_WITH_DES_CBC_SHA', 
     'SSL_DH_anon_EXPORT_WITH_DES40_CBC_SHA':'SSL_DH_anon_EXPORT_WITH_DES40_CBC_SHA', 
     'SSL_DH_anon_EXPORT_WITH_RC4_40_MD5':'SSL_DH_anon_EXPORT_WITH_RC4_40_MD5', 
     'SSL_DH_anon_WITH_3DES_EDE_CBC_SHA':'SSL_DH_anon_WITH_3DES_EDE_CBC_SHA', 
     'SSL_DH_anon_WITH_DES_CBC_SHA':'SSL_DH_anon_WITH_DES_CBC_SHA', 
     'SSL_DH_anon_WITH_RC4_128_MD5':'SSL_DH_anon_WITH_RC4_128_MD5', 
     'SSL_FORTEZZA_DMS_WITH_FORTEZZA_CBC_SHA':'SSL_FORTEZZA_DMS_WITH_FORTEZZA_CBC_SHA', 
     'SSL_FORTEZZA_DMS_WITH_NULL_SHA':'SSL_FORTEZZA_DMS_WITH_NULL_SHA', 
     'SSL_RSA_EXPORT1024_WITH_DES_CBC_SHA':'SSL_RSA_EXPORT1024_WITH_DES_CBC_SHA', 
     'SSL_RSA_EXPORT1024_WITH_RC4_56_SHA':'SSL_RSA_EXPORT1024_WITH_RC4_56_SHA', 
     'SSL_RSA_EXPORT_WITH_DES40_CBC_SHA':'SSL_RSA_EXPORT_WITH_DES40_CBC_SHA', 
     'SSL_RSA_EXPORT_WITH_RC2_CBC_40_MD5':'SSL_RSA_EXPORT_WITH_RC2_CBC_40_MD5', 
     'SSL_RSA_EXPORT_WITH_RC4_40_MD5':'SSL_RSA_EXPORT_WITH_RC4_40_MD5', 
     'SSL_RSA_FIPS_WITH_3DES_EDE_CBC_SHA':'SSL_RSA_FIPS_WITH_3DES_EDE_CBC_SHA', 
     'SSL_RSA_FIPS_WITH_DES_CBC_SHA':'SSL_RSA_FIPS_WITH_DES_CBC_SHA', 
     'SSL_RSA_WITH_3DES_EDE_CBC_SHA':'SSL_RSA_WITH_3DES_EDE_CBC_SHA', 
     'SSL_RSA_WITH_DES_CBC_SHA':'SSL_RSA_WITH_DES_CBC_SHA', 
     'SSL_RSA_WITH_IDEA_CBC_SHA':'SSL_RSA_WITH_IDEA_CBC_SHA', 
     'SSL_RSA_WITH_NULL_MD5':'SSL_RSA_WITH_NULL_MD5', 
     'SSL_RSA_WITH_NULL_SHA':'SSL_RSA_WITH_NULL_SHA', 
     'SSL_RSA_WITH_RC4_128_MD5':'SSL_RSA_WITH_RC4_128_MD5', 
     'SSL_RSA_WITH_RC4_128_SHA':'SSL_RSA_WITH_RC4_128_SHA', 
     'TLS_DHE_DSS_WITH_AES_128_CBC_SHA':'TLS_DHE_DSS_WITH_AES_128_CBC_SHA', 
     'TLS_DHE_DSS_WITH_AES_256_CBC_SHA':'TLS_DHE_DSS_WITH_AES_256_CBC_SHA', 
     'TLS_DHE_RSA_WITH_AES_128_CBC_SHA':'TLS_DHE_RSA_WITH_AES_128_CBC_SHA', 
     'TLS_DHE_RSA_WITH_AES_256_CBC_SHA':'TLS_DHE_RSA_WITH_AES_256_CBC_SHA', 
     'TLS_DH_anon_WITH_AES_128_CBC_SHA':'TLS_DH_anon_WITH_AES_128_CBC_SHA', 
     'TLS_DH_anon_WITH_AES_256_CBC_SHA':'TLS_DH_anon_WITH_AES_256_CBC_SHA', 
     'TLS_KRB5_EXPORT_WITH_DES_CBC_40_MD5':'TLS_KRB5_EXPORT_WITH_DES_CBC_40_MD5', 
     'TLS_KRB5_EXPORT_WITH_DES_CBC_40_SHA':'TLS_KRB5_EXPORT_WITH_DES_CBC_40_SHA', 
     'TLS_KRB5_EXPORT_WITH_RC2_CBC_40_MD5':'TLS_KRB5_EXPORT_WITH_RC2_CBC_40_MD5', 
     'TLS_KRB5_EXPORT_WITH_RC2_CBC_40_SHA':'TLS_KRB5_EXPORT_WITH_RC2_CBC_40_SHA', 
     'TLS_KRB5_EXPORT_WITH_RC4_40_MD5':'TLS_KRB5_EXPORT_WITH_RC4_40_MD5', 
     'TLS_KRB5_EXPORT_WITH_RC4_40_SHA':'TLS_KRB5_EXPORT_WITH_RC4_40_SHA', 
     'TLS_KRB5_WITH_3DES_EDE_CBC_MD5':'TLS_KRB5_WITH_3DES_EDE_CBC_MD5', 
     'TLS_KRB5_WITH_3DES_EDE_CBC_SHA':'TLS_KRB5_WITH_3DES_EDE_CBC_SHA', 
     'TLS_KRB5_WITH_DES_CBC_MD5':'TLS_KRB5_WITH_DES_CBC_MD5', 
     'TLS_KRB5_WITH_DES_CBC_SHA':'TLS_KRB5_WITH_DES_CBC_SHA', 
     'TLS_KRB5_WITH_IDEA_CBC_MD5':'TLS_KRB5_WITH_IDEA_CBC_MD5', 
     'TLS_KRB5_WITH_IDEA_CBC_SHA':'TLS_KRB5_WITH_IDEA_CBC_SHA', 
     'TLS_KRB5_WITH_RC4_128_MD5':'TLS_KRB5_WITH_RC4_128_MD5', 
     'TLS_KRB5_WITH_RC4_128_SHA':'TLS_KRB5_WITH_RC4_128_SHA', 
     'TLS_RSA_WITH_AES_128_CBC_SHA':'TLS_RSA_WITH_AES_128_CBC_SHA', 
     'TLS_RSA_WITH_AES_256_CBC_SHA':'TLS_RSA_WITH_AES_256_CBC_SHA'}


syntax_registry.reg_at(OpenDSCfgSslCipherSuite.oid, [
 '1.3.6.1.4.1.26027.1.1.392'])

class OpenDSCfgPrivilege(SelectList):
    oid = 'OpenDSCfgPrivilege-oid'
    oid: str
    desc = 'Specifies the name of a privilege that should not be evaluated by the server.'
    desc: str
    attr_value_dict = {'backend-backup':'Request backup tasks',  'backend-restore':'Request restore tasks', 
     'bypass-acl':'Bypass access control checks', 
     'bypass-lockdown':'Bypass server lockdown mode', 
     'cancel-request':'Cancel operations of other client connections', 
     'config-read':'Read server configuration', 
     'config-write':'Update the server configuration', 
     'data-sync':'Participate in data synchronization', 
     'disconnect-client':'Terminate other client connections', 
     'jmx-notify':'Subscribe to receive JMX notifications', 
     'jmx-read':'Perform JMX read operations', 
     'jmx-write':'Perform JMX write operations', 
     'ldif-export':'Request LDIF export tasks', 
     'ldif-import':'Request LDIF import tasks', 
     'modify-acl':"Modify the server's access control configuration", 
     'password-reset':'Reset user passwords', 
     'privilege-change':'Make changes to specific root privileges and user privileges', 
     'proxied-auth':'Use proxied authorization control or SASL authz ID', 
     'server-lockdown':'Lockdown a server', 
     'server-restart':'Request server to perform an in-core restart', 
     'server-shutdown':'Request server shut down', 
     'subentry-write':'Perform write ops on LDAP subentries', 
     'unindexed-search':'Request unindexed searches', 
     'update-schema':'Change server schema', 
     'changelog-read':'Read change log backend', 
     'monitor-read':'Read monitoring backend'}


syntax_registry.reg_at(OpenDSCfgPrivilege.oid, [
 '1.3.6.1.4.1.26027.1.1.261',
 '1.3.6.1.4.1.26027.1.1.387',
 '1.3.6.1.4.1.26027.1.1.260'])

class OpenDSCfgTimeInterval(DirectoryString):
    oid = 'OpenDSCfgTimeInterval-oid'
    oid: str
    desc = 'A time interval consisting of integer value and time unit'
    desc: str
    reObj = re.compile('^[0-9]+ (seconds|minutes|hours|days)$')


syntax_registry.reg_at(OpenDSCfgTimeInterval.oid, [
 '1.3.6.1.4.1.26027.1.1.142',
 '1.3.6.1.4.1.26027.1.1.145',
 '1.3.6.1.4.1.26027.1.1.147',
 '1.3.6.1.4.1.26027.1.1.148',
 '1.3.6.1.4.1.26027.1.1.149',
 '1.3.6.1.4.1.26027.1.1.150',
 '1.3.6.1.4.1.26027.1.1.152',
 '1.3.6.1.4.1.26027.1.1.375',
 '1.3.6.1.4.1.26027.1.1.115'])

class OpenDSSyncHist(OctetString, DirectoryString):
    oid = 'OpenDSSyncHist-oid'
    oid: str
    desc = 'List of modifications'
    desc: str

    def display(self, valueindex=0, commandbutton=False) -> str:
        try:
            mod_attr_type, mod_number, mod_type, mod_value = self._av.split(':', 3)
        except ValueError:
            return OctetString.display(self, valueindex, commandbutton)
        else:
            first_str = self._app.form.utf2display(':'.join((mod_attr_type, mod_number, mod_type)).decode(self._app.ls.charset))
            if no_humanreadable_attr(self._schema, mod_attr_type):
                mod_value_html = mod_value.hex().upper()
            else:
                mod_value_html = self._app.form.utf2display(mod_value.decode(self._app.ls.charset))
            return ':<br>'.join((first_str, mod_value_html))


syntax_registry.reg_at(OpenDSSyncHist.oid, [
 '1.3.6.1.4.1.26027.1.1.119'])

class OpenDSdsCfgAlternatebindDn(BindDN):
    oid = 'OpenDSdsCfgAlternatebindDn-oid'
    oid: str
    desc = 'OpenDS/OpenDJ alternative bind DN'
    desc: str

    def formValue(self) -> str:
        if not self._av:
            return ''
        try:
            dn_obj = DNObj(self.av_u)
        except ldap0.DECODING_ERROR:
            return BindDN.formValue(self)
        else:
            new_rdn = DNObj(tuple([(
             rdn_attr,
             rdn_value[0] or self._entry.get(rdn_attr, [''])[0]) for rdn_attr, rdn_value in dn_obj.rdn_attrs().items()]))
            return str(new_rdn + dn_obj.parent())


syntax_registry.reg_at(OpenDSdsCfgAlternatebindDn.oid, [
 '1.3.6.1.4.1.26027.1.1.13'])

class ChangeLogChanges(MultilineText):
    oid = 'ChangeLogChanges-oid'
    oid: str
    desc = 'a set of changes to apply to an entry'
    desc: str
    lineSep = b'\n'
    cols = 77


syntax_registry.reg_at(ChangeLogChanges.oid, [
 '2.16.840.1.113730.3.1.8'])
syntax_registry.reg_at(Certificate.oid, [
 '1.3.6.1.4.1.26027.1.1.408'])
syntax_registry.reg_at(NamingContexts.oid, [
 '1.3.6.1.4.1.26027.1.1.246',
 '1.3.6.1.4.1.26027.1.1.8'])
syntax_registry.reg_syntaxes(__name__)