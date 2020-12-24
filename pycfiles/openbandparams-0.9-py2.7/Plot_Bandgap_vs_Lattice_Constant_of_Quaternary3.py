# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/openbandparams/examples/Plot_Bandgap_vs_Lattice_Constant_of_Quaternary3.py
# Compiled at: 2015-08-15 20:40:28
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from openbandparams import *
import matplotlib.pyplot as plt, numpy
quaternary = GaInPAs
T = 300
fig = plt.figure()
ax = fig.add_subplot(111)
plt.xlabel('Lattice Parameter at %g K ($\\AA$)' % T)
plt.ylabel('Bandgap at %g K (eV)' % T)
xs = []
y_Gamma = []
y_X = []
y_L = []
labels = []
for b in quaternary.binaries:
    xs.append(b.a(T=T))
    y_Gamma.append(b.Eg_Gamma(T=T))
    y_X.append(b.Eg_X(T=T))
    y_L.append(b.Eg_L(T=T))
    labels.append(b.name)

ax.plot(xs, y_Gamma, 'r.')
ax.plot(xs, y_X, 'b.')
ax.plot(xs, y_L, 'g.')
for x, y, label in zip(xs, y_Gamma, labels):
    ax.annotate(label, xy=(x, y), xytext=(-5, 5), ha='right', va='bottom', bbox=dict(linewidth=0, fc='white', alpha=0.9), textcoords='offset points')

for x, y, label in zip(xs, y_X, labels):
    ax.annotate(label, xy=(x, y), xytext=(-5, 5), ha='right', va='bottom', bbox=dict(linewidth=0, fc='white', alpha=0.9), textcoords='offset points')

for x, y, label in zip(xs, y_L, labels):
    ax.annotate(label, xy=(x, y), xytext=(-5, 5), ha='right', va='bottom', bbox=dict(linewidth=0, fc='white', alpha=0.9), textcoords='offset points')

indices = numpy.arange(100)
fractions = numpy.linspace(0, 1, 100)
x = numpy.empty(100, dtype=numpy.float)
y_Gamma = numpy.empty(100, dtype=numpy.float)
y_X = numpy.empty(100, dtype=numpy.float)
y_L = numpy.empty(100, dtype=numpy.float)
first = True
for xfrac in numpy.linspace(0, 1, 10):
    for i, yfrac in zip(indices, fractions):
        instance = quaternary(x=xfrac, y=yfrac)
        x[i] = instance.a(T=T)
        y_Gamma[i] = instance.Eg_Gamma(T=T)
        y_X[i] = instance.Eg_X(T=T)
        y_L[i] = instance.Eg_L(T=T)

    if first:
        ax.plot(x, y_Gamma, 'r-', label='$\\Gamma$')
        ax.plot(x, y_X, 'b-', label='$X$')
        ax.plot(x, y_L, 'g-', label='$L$')
        first = False
    else:
        ax.plot(x, y_Gamma, 'r-')
        ax.plot(x, y_X, 'b-')
        ax.plot(x, y_L, 'g-')

for yfrac in numpy.linspace(0, 1, 10):
    for i, xfrac in zip(indices, fractions):
        instance = quaternary(x=xfrac, y=yfrac)
        x[i] = instance.a(T=T)
        y_Gamma[i] = instance.Eg_Gamma(T=T)
        y_X[i] = instance.Eg_X(T=T)
        y_L[i] = instance.Eg_L(T=T)

    ax.plot(x, y_Gamma, 'r--')
    ax.plot(x, y_X, 'b--')
    ax.plot(x, y_L, 'g--')

xmin, xmax = plt.xlim()
plt.xlim(xmin - 0.05, xmax)
plt.legend(loc='best')
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
        plt.savefig(output_filename)
    else:
        plt.show()