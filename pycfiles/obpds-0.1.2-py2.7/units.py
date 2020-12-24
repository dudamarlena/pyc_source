# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/obpds/units.py
# Compiled at: 2015-04-01 14:26:54
from pint import UnitRegistry
units = UnitRegistry()
m = units.m
cm = units.cm
cm3 = units.cm ** 3
um = units.um
nm = units.nm

def to_units(v, u):
    if not isinstance(v, units.Quantity):
        raise TypeError(('Missing units: {}').format(v))
    return v.to(u).magnitude