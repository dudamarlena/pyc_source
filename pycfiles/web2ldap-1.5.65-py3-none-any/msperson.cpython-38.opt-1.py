# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/msperson.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 3040 bytes
"""
web2ldap plugin classes for attributes defined for msPerson
"""
import re, os.path, web2ldapcnf
from web2ldap.app.schema.syntaxes import DateOfBirth, DirectoryString, IA5String, PropertiesSelectList, syntax_registry
try:
    import vatnumber
except ImportError:
    vatnumber = None
else:

    class Gender(PropertiesSelectList):
        oid = 'Gender-oid'
        oid: str
        desc = 'Representation of human sex (see ISO 5218)'
        desc: str
        properties_pathname = os.path.join(web2ldapcnf.etc_dir, 'properties', 'attribute_select_gender.properties')


    syntax_registry.reg_at(Gender.oid, [
     '1.3.6.1.4.1.5427.1.389.4.7'])
    syntax_registry.reg_at(DateOfBirth.oid, [
     '1.3.6.1.4.1.5427.1.389.4.2'])

    class LabeledBICandIBAN(DirectoryString):
        __doc__ = '\n    More information:\n    https://de.wikipedia.org/wiki/International_Bank_Account_Number\n    http://www.pruefziffernberechnung.de/I/IBAN.shtml\n    '
        oid = 'LabeledBICandIBAN-oid'
        oid: str
        desc = 'International bank account number (IBAN) syntax (see ISO 13616:1997)'
        desc: str


    syntax_registry.reg_at(LabeledBICandIBAN.oid, [
     '1.3.6.1.4.1.5427.1.389.4.13'])

    class EuVATId(IA5String):
        __doc__ = '\n    More information:\n    http://www.bzst.de/DE/Steuern_International/USt_Identifikationsnummer/Merkblaetter/Aufbau_USt_IdNr.pdf\n    https://de.wikipedia.org/wiki/Umsatzsteuer-Identifikationsnummer\n    '
        oid = 'EuVATId-oid'
        oid: str
        desc = 'Value Added Tax Ident Number of organizations within European Union'
        desc: str
        reObj = re.compile('^((AT)?U[0-9]{8}|(BE)?[0-9]{10}|(BG)?[0-9]{9,10}|(CY)?[0-9]{8}L|(CZ)?[0-9]{8,10}|(DE)?[0-9]{9}|(DK)?[0-9]{8}|(EE)?[0-9]{9}|(EL|GR)?[0-9]{9}|(ES)?[0-9A-Z][0-9]{7}[0-9A-Z]|(FI)?[0-9]{8}|(FR)?[0-9A-Z]{2}[0-9]{9}|(GB)?([0-9]{9}([0-9]{3})?|[A-Z]{2}[0-9]{3})|(HU)?[0-9]{8}|(IE)?[0-9]S[0-9]{5}L|(IT)?[0-9]{11}|(LT)?([0-9]{9}|[0-9]{12})|(LU)?[0-9]{8}|(LV)?[0-9]{11}|(MT)?[0-9]{8}|(NL)?[0-9]{9}B[0-9]{2}|(PL)?[0-9]{10}|(PT)?[0-9]{9}|(RO)?[0-9]{2,10}|(SE)?[0-9]{12}|(SI)?[0-9]{8}|(SK)?[0-9]{10})$')

        def _validate(self, attrValue: bytes) -> bool:
            if vatnumber:
                return vatnumber.check_vat(attrValue)
            return IA5String._validate(self, attrValue)

        def sanitize(self, attrValue: bytes) -> bytes:
            return attrValue.upper().replace(b' ', b'')


    syntax_registry.reg_at(EuVATId.oid, [
     '1.3.6.1.4.1.5427.1.389.4.11'])
    syntax_registry.reg_syntaxes(__name__)