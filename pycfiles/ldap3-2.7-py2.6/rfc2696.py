# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\protocol\rfc2696.py
# Compiled at: 2020-02-23 02:01:40
"""
"""
from pyasn1.type.univ import OctetString, Integer, Sequence
from pyasn1.type.namedtype import NamedTypes, NamedType
from pyasn1.type.constraint import ValueRangeConstraint
from .controls import build_control
MAXINT = Integer(2147483647)
rangeInt0ToMaxConstraint = ValueRangeConstraint(0, MAXINT)

class Integer0ToMax(Integer):
    subtypeSpec = Integer.subtypeSpec + rangeInt0ToMaxConstraint


class Size(Integer0ToMax):
    pass


class Cookie(OctetString):
    pass


class RealSearchControlValue(Sequence):
    componentType = NamedTypes(NamedType('size', Size()), NamedType('cookie', Cookie()))


def paged_search_control(criticality=False, size=10, cookie=None):
    control_value = RealSearchControlValue()
    control_value.setComponentByName('size', Size(size))
    control_value.setComponentByName('cookie', Cookie(cookie if cookie else ''))
    return build_control('1.2.840.113556.1.4.319', criticality, control_value)