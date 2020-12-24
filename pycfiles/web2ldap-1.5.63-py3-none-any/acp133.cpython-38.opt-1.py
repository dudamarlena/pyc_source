# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/acp133.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 4858 bytes
"""
web2ldap plugin classes for ACP-133
(see draft-dally-acp133-and-ldap)

Currently untested!
"""
from web2ldap.app.schema.syntaxes import SelectList, DynamicDNSelectList, syntax_registry

class AddressListDN(DynamicDNSelectList):
    oid = 'AddressListDN-oid'
    oid: str
    desc = 'DN which points to address list entry '
    desc: str
    ldap_url = 'ldap:///_?cn?sub?(objectClass=addressList)'


syntax_registry.reg_at(AddressListDN.oid, [
 '2.16.840.1.101.2.2.1.61',
 '2.6.5.2.14'])

class LMF(SelectList):
    oid = 'LMF-oid'
    oid: str
    desc = 'Language and Media Format (see section 3.59 of draft-dally-acp133-and-ldap-01)'
    desc: str
    attr_value_dict = {'T':'tape',  'A':'ASCII', 
     'C':'card'}


syntax_registry.reg_at(LMF.oid, [
 '2.16.840.1.101.2.2.1.62'])

class TRC(SelectList):
    oid = 'TRC-oid'
    oid: str
    desc = 'Transmission Release Code (see section 3.126 of draft-dally-acp133-and-ldap-01)'
    desc: str
    attr_value_dict = {'A':'Australia',  'B':'British Commonwealth less Canada, Australia, and New Zealand', 
     'C':'Canada', 
     'U':'US', 
     'X':'Belgium, Denmark, France, Germany, Greece, Italy, Netherlands, Norway, Portugal, Turkey, NATO', 
     'Z':'New Zealand'}


syntax_registry.reg_at(TRC.oid, [
 '2.16.840.1.101.2.2.1.97'])

class ACPLegacyFormat(SelectList):
    oid = '2.16.840.1.101.2.2.2.17'
    oid: str
    desc = 'aCPLegacyFormat syntax (see section 6.1 of draft-dally-acp133-and-ldap-01)'
    desc: str
    attr_value_dict = {'0':'JANAP128',  '1':'ACP126', 
     '2':'DOI103', 
     '3':'DOI103Special', 
     '4':'ACP127', 
     '5':'ACP127Converted', 
     '6':'Reserved1', 
     '7':'ACP127State', 
     '8':'ACP127Modified', 
     '9':'SOCOMMSpecial', 
     '10':'SOCOMMNarrative', 
     '11':'Reserved2', 
     '12':'SOCOMMNarrativeSpecial', 
     '13':'SOCOMMData', 
     '14':'SOCOMMInternal', 
     '15':'SOCOMMExternal', 
     '32':'32 (national or bilateral use)', 
     '33':'33 (national or bilateral use)', 
     '34':'34 (national or bilateral use)', 
     '35':'35 (national or bilateral use)', 
     '36':'36 (national or bilateral use)', 
     '37':'37 (national or bilateral use)', 
     '38':'38 (national or bilateral use)', 
     '39':'39 (national or bilateral use)', 
     '40':'40 (national or bilateral use)', 
     '41':'41 (national or bilateral use)', 
     '42':'42 (national or bilateral use)', 
     '43':'43 (national or bilateral use)', 
     '44':'44 (national or bilateral use)', 
     '45':'45 (national or bilateral use)', 
     '46':'46 (national or bilateral use)', 
     '47':'47 (national or bilateral use)', 
     '48':'48 (national or bilateral use)'}


class ACPPreferredDelivery(SelectList):
    oid = '2.16.840.1.101.2.2.2.6'
    oid: str
    desc = 'aCPPreferredDelivery syntax (see section 6.2 of draft-dally-acp133-and-ldap-01)'
    desc: str
    attr_value_dict = {'0':'SMTP',  '1':'ACP 127', 
     '2':'MHS'}


class AddressListType(SelectList):
    oid = '2.16.840.1.101.2.2.2.8'
    oid: str
    desc = 'addressListType syntax (see section 6.6 of draft-dally-acp133-and-ldap-01)'
    desc: str
    attr_value_dict = {'0':'AIG',  '1':'TYPE', 
     '2':'CAD', 
     '3':'TASKFORCE'}


class Classification(SelectList):
    oid = '2.16.840.1.101.2.2.2.4'
    oid: str
    desc = 'Classification syntax (see section 6.8 of draft-dally-acp133-and-ldap-01)'
    desc: str
    attr_value_dict = {'0':'unmarked',  '1':'unclassified', 
     '2':'restricted', 
     '3':'confidential', 
     '4':'secret', 
     '5':'top secret'}


class Community(SelectList):
    oid = '2.16.840.1.101.2.2.2.5'
    oid: str
    desc = 'Community syntax (see section 6.9 of draft-dally-acp133-and-ldap-01)'
    desc: str
    attr_value_dict = {'0':'GENSER',  '1':'SI', 
     '2':'both'}


syntax_registry.reg_syntaxes(__name__)