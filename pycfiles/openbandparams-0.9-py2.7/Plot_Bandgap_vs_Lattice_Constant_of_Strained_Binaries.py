# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/openbandparams/examples/Plot_Bandgap_vs_Lattice_Constant_of_Strained_Binaries.py
# Compiled at: 2015-04-09 02:47:55
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from openbandparams import *
import matplotlib.pyplot as plt, numpy
T = 300
fig = plt.figure()
ax = fig.add_subplot(111)
plt.xlabel('Substrate Lattice Parameter at %g K ($\\AA$)' % T)
plt.ylabel('Strained Bandgap at %g K (eV)' % T)
x = []
y = []
label = []
for b in [AlP, GaP, InP,
 AlAs, GaAs, InAs,
 AlSb, GaSb, InSb]:
    x.append(b.a(T=T))
    y.append(b.Eg(T=T))
    label.append(b.name)

ax.plot(x, y, 'k.')
for x, y, label in zip(x, y, label):
    ax.annotate(label, xy=(x, y), xytext=(5, 5), ha='left', va='bottom', bbox=dict(linewidth=0, fc='white', alpha=0.9), textcoords='offset points')

first = True
strains = numpy.linspace(-0.02, 0.02, 100)
for unstrained in [AlP, GaP, InP,
 AlAs, GaAs, InAs,
 AlSb, GaSb, InSb]:
    straineds = [ unstrained.strained_001(strain) for strain in strains ]
    substrate_a = [ strained.substrate_a() for strained in straineds ]
    Eg_hh = [ strained.Eg_hh() for strained in straineds ]
    Eg_lh = [ strained.Eg_lh() for strained in straineds ]
    if first:
        plt.plot(substrate_a, Eg_hh, 'r-', label='CB-HH gap')
        plt.plot(substrate_a, Eg_lh, 'g-', label='CB-LH gap')
        first = False
    else:
        plt.plot(substrate_a, Eg_hh, 'r-')
        plt.plot(substrate_a, Eg_lh, 'g-')

plt.legend(loc='best')
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
        plt.savefig(output_filename)
    else:
        plt.show()