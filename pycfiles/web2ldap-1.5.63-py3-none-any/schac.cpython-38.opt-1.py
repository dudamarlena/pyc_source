# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/schac.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 2603 bytes
"""
web2ldap plugin classes for attributes defined in SCHAC

See https://www.terena.org/activities/tf-emc2/schac.html
"""
import re, datetime
from web2ldap.app.schema.syntaxes import DateOfBirth, DirectoryString, IA5String, NumericString, CountryString, DNSDomain, syntax_registry
from web2ldap.app.plugins.msperson import Gender
syntax_registry.reg_at(CountryString.oid, [
 '1.3.6.1.4.1.25178.1.2.5',
 '1.3.6.1.4.1.25178.1.2.11'])
syntax_registry.reg_at(DNSDomain.oid, [
 '1.3.6.1.4.1.25178.1.2.9'])

class SchacMotherTongue(IA5String):
    oid = 'SchacMotherTongue-oid'
    oid: str
    desc = 'Language tag of the language a person learns first (see RFC 3066).'
    desc: str
    reObj = re.compile('^[a-zA-Z]{2,8}(-[a-zA-Z0-9]{2,8})*$')


syntax_registry.reg_at(SchacMotherTongue.oid, [
 '1.3.6.1.4.1.25178.1.2.1'])
syntax_registry.reg_at(Gender.oid, [
 '1.3.6.1.4.1.25178.1.2.2'])

class SchacDateOfBirth(DateOfBirth):
    oid = 'SchacDateOfBirth-oid'
    oid: str
    desc = 'Date of birth: syntax YYYYMMDD'
    desc: str
    storageFormat = '%Y%m%d'


syntax_registry.reg_at(SchacDateOfBirth.oid, [
 '1.3.6.1.4.1.25178.1.2.3'])

class SchacYearOfBirth(NumericString):
    oid = 'SchacYearOfBirth-oid'
    oid: str
    desc = 'Year of birth: syntax YYYY'
    desc: str
    maxLen = 4
    maxLen: str
    input_pattern = '^[0-9]{4}$'
    input_pattern: str
    reObj = re.compile(input_pattern)

    def _validate(self, attrValue: bytes) -> bool:
        try:
            birth_year = int(attrValue)
        except ValueError:
            return False
        else:
            return birth_year <= datetime.date.today().year


syntax_registry.reg_at(SchacYearOfBirth.oid, [
 '1.3.6.1.4.1.25178.1.0.2.3'])

class SchacUrn(DirectoryString):
    oid = 'SchacUrn-oid'
    oid: str
    desc = 'Generic URN for SCHAC'
    desc: str
    input_pattern = '^urn:mace:terena.org:schac:.+$'
    input_pattern: str
    reObj = re.compile(input_pattern)


syntax_registry.reg_at(SchacUrn.oid, [
 '1.3.6.1.4.1.25178.1.2.10',
 '1.3.6.1.4.1.25178.1.2.13',
 '1.3.6.1.4.1.25178.1.2.14',
 '1.3.6.1.4.1.25178.1.2.15',
 '1.3.6.1.4.1.25178.1.2.19'])
syntax_registry.reg_syntaxes(__name__)