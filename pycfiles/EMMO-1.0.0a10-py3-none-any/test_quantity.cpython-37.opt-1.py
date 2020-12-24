# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /emmo/tests/test_quantity.py
# Compiled at: 2020-04-10 18:20:30
# Size of source mod 2**32: 691 bytes
import os, sys
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import World
import owlready2
from emmo.quantity import isquantity, get_units, Quantity, physics_dimension_of_quantity, physics_dimension_of_unit
world = World()
emmo = world.get_ontology()
emmo.load()
o = emmo
w = o.world
assert not isquantity(emmo.Item)
assert isquantity(emmo.Length)
print(get_units(emmo.Length))