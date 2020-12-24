# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/openbandparams/examples/advanced/GaInAsSb_on_GaSb/Plot_Strained_Bandgap_vs_Lattice_Constant_of_Quaternary3.py
# Compiled at: 2015-04-09 02:47:55
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
from openbandparams import *
import matplotlib.pyplot as plt, numpy
quaternary = GaInAsSb
T = 300
fig = plt.figure()
ax = fig.add_subplot(111)
plt.title('$%s/GaSb$ from 0 to 3%% strain' % quaternary.latex())
plt.xlabel('Unstrained Lattice Parameter at %g K ($\\AA$)' % T)
plt.ylabel('Strained Bandgap at %g K (eV)' % T)
xs = []
ys = []
labels = []
for b in [GaSb, InAs, InSb]:
    xs.append(b.a(T=T))
    ys.append(b.Eg_Gamma(T=T))
    labels.append(b.name)

ax.plot(xs, ys, 'k.')
for x, y, label in zip(xs, ys, labels):
    ax.annotate(label, xy=(x, y), xytext=(-5, 5), ha='right', va='bottom', bbox=dict(linewidth=0, fc='white', alpha=0.9), textcoords='offset points')

indices = numpy.arange(100)
fractions = numpy.linspace(0, 1, 100)
x = numpy.empty(100, dtype=numpy.float)
Eg_hh = numpy.empty(100, dtype=numpy.float)
Eg_lh = numpy.empty(100, dtype=numpy.float)
first = True
for xfrac in numpy.linspace(0, 1, 10):
    for i, yfrac in zip(indices, fractions):
        instance = quaternary(x=xfrac, y=yfrac)
        x[i] = instance.a(T=T)
        strained = instance.strained_001(GaSb)
        strain = strained.strain_out_of_plane(T=T)
        if not 0.0 <= strain <= 0.03:
            Eg_hh[i] = numpy.nan
            Eg_lh[i] = numpy.nan
        else:
            Eg_hh[i] = strained.Eg_hh(T=T)
            Eg_lh[i] = strained.Eg_lh(T=T)

    if first:
        ax.plot(x, Eg_hh, 'b-', label='Eg_hh')
        first = False
    else:
        ax.plot(x, Eg_hh, 'b-')

for yfrac in numpy.linspace(0, 1, 10):
    for i, xfrac in zip(indices, fractions):
        instance = quaternary(x=xfrac, y=yfrac)
        x[i] = instance.a(T=T)
        strained = instance.strained_001(GaSb)
        strain = strained.strain_out_of_plane(T=T)
        if not 0.0 <= strain <= 0.03:
            Eg_hh[i] = numpy.nan
            Eg_lh[i] = numpy.nan
        else:
            Eg_hh[i] = strained.Eg_hh(T=T)
            Eg_lh[i] = strained.Eg_lh(T=T)

    ax.plot(x, Eg_hh, 'b--')

plt.xlim(6, 6.5)
plt.ylim(0, 0.8)
plt.legend(loc='best')
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
        plt.savefig(output_filename)
    else:
        plt.show()