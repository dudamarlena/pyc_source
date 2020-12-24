# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\protocol\controls.py
# Compiled at: 2020-02-23 02:04:03
"""
"""
from .rfc4511 import Control, Criticality, LDAPOID
from ..utils.asn1 import encode

def build_control(oid, criticality, value, encode_control_value=True):
    control = Control()
    control.setComponentByName('controlType', LDAPOID(oid))
    control.setComponentByName('criticality', Criticality(criticality))
    if value is not None:
        if encode_control_value:
            control.setComponentByName('controlValue', encode(value))
        else:
            control.setComponentByName('controlValue', value)
    return control