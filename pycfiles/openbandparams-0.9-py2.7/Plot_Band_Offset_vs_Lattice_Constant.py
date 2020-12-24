# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/openbandparams/examples/Plot_Band_Offset_vs_Lattice_Constant.py
# Compiled at: 2014-12-20 03:47:21
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from openbandparams import *
import matplotlib.pyplot as plt, numpy
T = 300
fig = plt.figure()
ax = fig.add_subplot(111)
plt.xlabel('Lattice Parameter at %g K ($\\AA$)' % T)
plt.ylabel('Band Offset at %g K (eV)' % T)
x = []
y = []
label = []
for b in [AlP, GaP, InP,
 AlAs, GaAs, InAs,
 AlSb, GaSb, InSb]:
    x.append(b.a(T=T))
    y.append(b.Eg(T=T) + b.VBO(T=T))
    label.append(b.name)

ax.plot(x, y, 'b.')
for x, y, label in zip(x, y, label):
    ax.annotate(label, xy=(x, y), xytext=(-5, 5), ha='right', va='bottom', bbox=dict(linewidth=0, fc='white', alpha=0.9), textcoords='offset points')

indices = numpy.arange(100)
fractions = numpy.linspace(0, 1, 100)
x = numpy.empty(100, dtype=numpy.float)
y = numpy.empty(100, dtype=numpy.float)
for tern in [AlGaP, AlInP, GaInP,
 AlGaAs, AlInAs, GaInAs,
 AlGaSb, AlInSb, GaInSb,
 AlPAs, GaPAs, InPAs,
 AlPSb, GaPSb, InPSb,
 AlAsSb, GaAsSb, InAsSb]:
    for i, f in zip(indices, fractions):
        instance = tern(x=f)
        x[i] = instance.a(T=T)
        y[i] = instance.Eg(T=T) + instance.VBO(T=T)

    ax.plot(x, y, 'b-')

x = []
y = []
label = []
for b in [AlP, GaP, InP,
 AlAs, GaAs, InAs,
 AlSb, GaSb, InSb]:
    x.append(b.a(T=T))
    y.append(b.VBO(T=T))
    label.append(b.name)

ax.plot(x, y, 'r.')
for x, y, label in zip(x, y, label):
    ax.annotate(label, xy=(x, y), xytext=(-5, 5), ha='right', va='bottom', bbox=dict(linewidth=0, fc='white', alpha=0.9), textcoords='offset points')

indices = numpy.arange(100)
fractions = numpy.linspace(0, 1, 100)
x = numpy.empty(100, dtype=numpy.float)
y = numpy.empty(100, dtype=numpy.float)
for tern in [AlGaP, AlInP, GaInP,
 AlGaAs, AlInAs, GaInAs,
 AlGaSb, AlInSb, GaInSb,
 AlPAs, GaPAs, InPAs,
 AlPSb, GaPSb, InPSb,
 AlAsSb, GaAsSb, InAsSb]:
    for i, f in zip(indices, fractions):
        instance = tern(x=f)
        x[i] = instance.a(T=T)
        y[i] = instance.VBO(T=T)

    ax.plot(x, y, 'r-')

xmin, xmax = plt.xlim()
plt.xlim(xmin - 0.05, xmax)
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
        plt.savefig(output_filename)
    else:
        plt.show()