# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/obpds/examples/degenerate_pn_diode.py
# Compiled at: 2015-11-15 13:26:57
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from obpds import *
p = Layer(1 * um, InAs, 1000000000000000.0 / cm3)
n = Layer(1 * um, InAs, -2e+18 / cm3)
d = TwoTerminalDevice(layers=[p, n])
import matplotlib.pyplot as plt
_, ax1 = plt.subplots()
ax1.set_ymargin(0.05)
ax1.set_ylabel('Energy (eV)')
ax1.set_xlabel('Depth (nm)')
solution = d.get_equilibrium(approx='boltzmann')
x = solution.x * 10000000.0
ax1.plot(x, solution.Ev, 'r:')
ax1.plot(x, solution.Ec, 'b:', lw=2, label='Parabolic Boltzmann')
solution = d.get_equilibrium(approx='parabolic')
x = solution.x * 10000000.0
ax1.plot(x, solution.Ev, 'r--')
ax1.plot(x, solution.Ec, 'b--', lw=2, label='Parabolic')
solution = d.get_equilibrium(approx='kane')
x = solution.x * 10000000.0
ax1.plot(x, solution.Ev, 'r-')
ax1.plot(x, solution.Ec, 'b-', label='Non-parabolic Kane')
ax1.plot(x, solution.Ef, 'k--')
ax1.legend(loc='best')
plt.show()