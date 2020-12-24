# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/x509.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 7826 bytes
"""
web2ldap plugin classes for
GSER-based LDAP syntaxes defined in
http://tools.ietf.org/html/rfc4523

At this time this is mainly a stub module.
Currently untested!
"""
import ldap0.dn, asn1crypto.pem, asn1crypto.x509, asn1crypto.crl
from web2ldap.app.schema.syntaxes import ASN1Object, Binary, GSER, syntax_registry

def x509name2ldapdn(x509name, subschema=None):
    dn_list = []
    for rdn in reversed(x509name.chosen):
        rdn_list = []
        for ava in rdn:
            type_oid = ava['type'].dotted
            type_name = type_oid
            if subschema is not None:
                try:
                    at_obj = subschema.get_obj((ldap0.schema.models.AttributeType),
                      type_oid,
                      raise_keyerror=True)
                except (KeyError, IndexError):
                    pass
                else:
                    type_name = at_obj.names[0]
            rdn_list.append((
             type_name,
             ava['value'].native))
        else:
            dn_list.append(rdn_list)

    else:
        return str(ldap0.dn.DNObj(tuple(dn_list)))


class AttributeCertificate(Binary):
    oid = '1.3.6.1.4.1.4203.666.11.10.2.1'
    oid: str
    desc = 'X.509 Attribute Certificate'
    desc: str
    mimeType = 'application/pkix-attr-cert'
    fileExt = 'cer'


class Certificate(Binary):
    oid = '1.3.6.1.4.1.1466.115.121.1.8'
    oid: str
    desc = 'X.509 Certificate'
    desc: str
    mimeType = 'application/pkix-cert'
    fileExt = 'cer'
    cert_display_template = '\n    <dl>\n      <dt>Issuer:</dt>\n      <dd>{cert_issuer_dn}</dd>\n      <dt>Subject</dt>\n      <dd>{cert_subject_dn}</dd>\n      <dt>Serial No.</dt>\n      <dd>{cert_serial_number_dec} ({cert_serial_number_hex})</dd>\n      <dt>Validity period</dt>\n      <dd>from {cert_not_before} until {cert_not_after}</dd>\n    </dl>\n    '
    cert_extn_display_template = '\n    <dt>{ext_crit} {ext_name} {ext_id} </dt>\n    <dd>{extn_value}</dd>\n    '

    def sanitize(self, attrValue: bytes) -> bytes:
        if asn1crypto.pem.detect(attrValue):
            try:
                _, _, attrValue = asn1crypto.pem.unarmor(attrValue, multiple=False)
            except ValueError:
                pass

        return attrValue

    def _display_extensions(self, x509):
        html = [
         '<p>Extensions</p>']
        html.append('<dl>')
        for ext in x509['tbs_certificate']['extensions']:
            ext_oid = str(ext['extn_id'])
            html.append(self.cert_extn_display_template.format(ext_id=(self._app.form.utf2display(ext_oid)),
              ext_name=(asn1crypto.x509.ExtensionId._map.get(ext_oid, ext_oid)),
              ext_crit=({False:'', 
             True:'critical: '}[ext['critical'].native]),
              extn_value=(self._app.form.utf2display(str(ext['extn_value'].parsed)))))
        else:
            html.append('</dl>')
            return html

    def display(self, valueindex=0, commandbutton=False) -> str:
        html = ['%d bytes' % (len(self._av),)]
        try:
            x509 = asn1crypto.x509.Certificate.load(self._av)
        except ValueError:
            return ''.join(html)
        else:
            html.append(self.cert_display_template.format(cert_issuer_dn=(self._app.form.utf2display(x509name2ldapdn(x509.issuer, self._schema))),
              cert_subject_dn=(self._app.form.utf2display(x509name2ldapdn(x509.subject, self._schema))),
              cert_serial_number_dec=(str(x509.serial_number)),
              cert_serial_number_hex=(hex(x509.serial_number)),
              cert_not_before=(x509['tbs_certificate']['validity']['not_before'].native),
              cert_not_after=(x509['tbs_certificate']['validity']['not_after'].native)))
            return ''.join(html)


class CACertificate(Certificate):
    oid = 'CACertificate-oid'
    oid: str
    desc = 'X.509 CA Certificate'
    desc: str
    mimeType = 'application/x-x509-ca-cert'

    def getMimeType(self):
        return self.mimeType


class CertificateList(Binary):
    oid = '1.3.6.1.4.1.1466.115.121.1.9'
    oid: str
    desc = 'Certificate Revocation List'
    desc: str
    mimeType = 'application/pkix-crl'
    fileExt = 'crl'
    crl_display_template = '\n      <dl>\n        <dt>Issuer:</dt>\n        <dd>{crl_issuer_dn}</dd>\n        <dt>This update</dt>\n        <dd>{crl_this_update}</dd>\n        <dt>Next update</dt>\n        <dd>{crl_next_update}</dd>\n      </dl>\n      '

    def sanitize(self, attrValue: bytes) -> bytes:
        if asn1crypto.pem.detect(attrValue):
            try:
                _, _, attrValue = asn1crypto.pem.unarmor(attrValue, multiple=False)
            except ValueError:
                pass

        return attrValue

    def display(self, valueindex=0, commandbutton=False) -> str:
        try:
            x509 = asn1crypto.crl.CertificateList.load(self._av)
        except ValueError:
            crl_html = ''
        else:
            crl_html = self.crl_display_template.format(crl_issuer_dn=(self._app.form.utf2display(x509name2ldapdn(x509.issuer, self._schema))),
              crl_this_update=(x509['tbs_cert_list']['this_update'].native),
              crl_next_update=(x509['tbs_cert_list']['next_update'].native))
        return ''.join(('%d bytes' % (len(self._av),), crl_html))


class CertificatePair(ASN1Object):
    oid = '1.3.6.1.4.1.1466.115.121.1.10'
    oid: str
    desc = 'X.509 Certificate Pair'
    desc: str
    mimeType = 'application/pkix-cert'
    fileExt = 'cer'


class SupportedAlgorithm(ASN1Object):
    oid = '1.3.6.1.4.1.1466.115.121.1.49'
    oid: str
    desc = 'X.509 Supported Algorithm'
    desc: str


class X509CertificateExactAssertion(GSER):
    oid = '1.3.6.1.1.15.1'
    oid: str
    desc = 'X.509 Certificate Exact Assertion'
    desc: str


class X509CertificateAssertion(GSER):
    oid = '1.3.6.1.1.15.2'
    oid: str
    desc = 'X.509 Certificate Assertion'
    desc: str


class X509CertificatePairExactAssertion(GSER):
    oid = '1.3.6.1.1.15.3'
    oid: str
    desc = 'X.509 Certificate Pair Exact Assertion'
    desc: str


class X509CertificatePairAssertion(GSER):
    oid = '1.3.6.1.1.15.4'
    oid: str
    desc = 'X.509 Certificate Pair Assertion'
    desc: str


class X509CertificateListExactAssertion(GSER):
    oid = '1.3.6.1.1.15.5'
    oid: str
    desc = 'X.509 Certificate List Exact Assertion'
    desc: str


class X509CertificateListAssertion(GSER):
    oid = '1.3.6.1.1.15.6'
    oid: str
    desc = 'X.509 Certificate List Assertion'
    desc: str


class X509AlgorithmIdentifier(GSER):
    oid = '1.3.6.1.1.15.7'
    oid: str
    desc = 'X.509 Algorithm Identifier'
    desc: str


syntax_registry.reg_at(Certificate.oid, [
 '2.5.4.36',
 'userCertificate', 'userCertificate;binary'])
syntax_registry.reg_at(CACertificate.oid, [
 '2.5.4.37',
 'cACertificate', 'cACertificate;binary'])
syntax_registry.reg_at(CertificateList.oid, [
 '2.5.4.38',
 '2.5.4.39',
 '2.5.4.53',
 'authorityRevocationList', 'authorityRevocationList;binary',
 'certificateRevocationList', 'certificateRevocationList;binary',
 'deltaRevocationList', 'deltaRevocationList;binary'])
syntax_registry.reg_syntaxes(__name__)