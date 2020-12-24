# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\protocol\persistentSearch.py
# Compiled at: 2020-02-23 02:04:04
"""
"""
from pyasn1.type.namedtype import NamedTypes, NamedType, OptionalNamedType
from pyasn1.type.namedval import NamedValues
from pyasn1.type.univ import Sequence, Integer, Boolean, Enumerated
from .rfc4511 import LDAPDN
from .controls import build_control

class PersistentSearchControl(Sequence):
    componentType = NamedTypes(NamedType('changeTypes', Integer()), NamedType('changesOnly', Boolean()), NamedType('returnECs', Boolean()))


class ChangeType(Enumerated):
    namedValues = NamedValues(('add', 1), ('delete', 2), ('modify', 4), ('modDN', 8))


class EntryChangeNotificationControl(Sequence):
    componentType = NamedTypes(NamedType('changeType', ChangeType()), OptionalNamedType('previousDN', LDAPDN()), OptionalNamedType('changeNumber', Integer()))


def persistent_search_control(change_types, changes_only=True, return_ecs=True, criticality=False):
    control_value = PersistentSearchControl()
    control_value.setComponentByName('changeTypes', Integer(change_types))
    control_value.setComponentByName('changesOnly', Boolean(changes_only))
    control_value.setComponentByName('returnECs', Boolean(return_ecs))
    return build_control('2.16.840.1.113730.3.4.3', criticality, control_value)