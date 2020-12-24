# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/monty-carlo/atomic/ex_atomic.py
# Compiled at: 2011-09-07 20:02:41
import atomic as a, numpy as num, logging
logging.basicConfig(level=logging.DEBUG)
Na = a.Atom(atomic_no=11)
Cl = a.Atom(atomic_no=17)
Na.size = 25
Cl.size = 40
Na2, Na3, Na4, Na5, Na6, Na7, Na8, Na9, Na10, Na11, Na12, Na13, Na14 = Na.copy(13)
Cl2, Cl3, Cl4, Cl5, Cl6, Cl7, Cl8, Cl9, Cl10, Cl11, Cl12, Cl13 = Cl.copy(12)
Na.position = num.array([0, 0, 0])
Cl.position = num.array([0.5, 1, 0])
Na2.position = num.array([0.5, 0.5, 0])
Cl2.position = num.array([0, 0.5, 0])
Na3.position = num.array([1, 1, 0])
Cl3.position = num.array([0.5, 0, 0])
Na4.position = num.array([1, 0, 0])
Cl4.position = num.array([1, 0.5, 0])
Na5.position = num.array([0, 1, 0])
Cl5.position = num.array([0, 0, 0.5])
Na6.position = num.array([0.5, 1, 0.5])
Cl6.position = num.array([0.5, 0.5, 0.5])
Na7.position = num.array([0, 0.5, 0.5])
Cl7.position = num.array([1, 1, 0.5])
Na8.position = num.array([0.5, 0, 0.5])
Cl8.position = num.array([1, 0, 0.5])
Na9.position = num.array([1, 0.5, 0.5])
Cl9.position = num.array([0, 1, 0.5])
Na10.position = num.array([0, 0, 1])
Cl10.position = num.array([0.5, 1, 1])
Na11.position = num.array([0.5, 0.5, 1])
Cl11.position = num.array([0, 0.5, 1])
Na12.position = num.array([1, 1, 1])
Cl12.position = num.array([0.5, 0, 1])
Na13.position = num.array([1, 0, 1])
Cl13.position = num.array([1, 0.5, 1])
Na14.position = num.array([0, 1, 0])
list_of_atoms = [
 Na, Na2, Na3, Na4, Na5, Na6, Na7, Na8, Na9, Na10, Na11, Na12, Na13, Na14,
 Cl2, Cl3, Cl4, Cl5, Cl6, Cl7, Cl8, Cl9, Cl10, Cl11, Cl12, Cl13]
unit_vec = (
 num.array([1, 0, 0]), num.array([0, 1, 0]), num.array([0, 0, 1]))
lat = a.Lattice(unit_vec, list_of_atoms, strech=3)
lat.show()