# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/freeradius.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 593 bytes
"""
web2ldap plugin classes for FreeRADIUS/LDAP schema
"""
from web2ldap.app.schema.syntaxes import DynamicDNSelectList, syntax_registry

class RadiusProfileDN(DynamicDNSelectList):
    oid = 'RadiusProfileDN-oid'
    oid: str
    desc = 'DN of a radius profile entry with real data'
    desc: str
    ldap_url = 'ldap:///_??sub?(&(objectClass=radiusprofile)(!(radiusProfileDn=*)))'


syntax_registry.reg_at(RadiusProfileDN.oid, [
 '1.3.6.1.4.1.3317.4.3.1.49'])
syntax_registry.reg_syntaxes(__name__)