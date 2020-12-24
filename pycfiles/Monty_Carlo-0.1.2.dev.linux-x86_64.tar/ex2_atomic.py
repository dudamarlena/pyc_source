# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/monty-carlo/atomic/ex2_atomic.py
# Compiled at: 2011-09-07 20:02:41
import atomic as a, numpy as num, logging
logging.basicConfig(level=logging.DEBUG)
Na = a.Atom(atomic_no=11)
Cl = a.Atom(atomic_no=17)
Na.size = 25
Cl.size = 40
Na2, = Na.copy(1)
Cl2, = Cl.copy(1)
Na.position = num.array([0, 0])
Cl.position = num.array([0.5, 0])
Na2.position = num.array([0.5, 0.5])
Cl2.position = num.array([0, 0.5])
list_of_atoms = [
 Na, Na2, Cl, Cl2]
unit_vec = (
 num.array([1, 0]), num.array([0, 1]))
lat = a.Lattice(unit_vec, list_of_atoms, strech=3)
lat.show()