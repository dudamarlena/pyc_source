# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/openbandparams/examples/Plot_Band_Offset_vs_Composition_of_Ternary.py
# Compiled at: 2015-07-09 16:40:15
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from openbandparams import *
import matplotlib.pyplot as plt, numpy
alloy = AlGaAs
T = 300
fig = plt.figure()
ax = fig.add_subplot(111)
plt.title('%s (T = %g K)' % (alloy.name, T))
plt.xlabel('%s fraction' % alloy.elements[1])
plt.ylabel('Band Offset at %g K (eV)' % T)
x = [
 0, 1]
y = []
label = []
for b in alloy.binaries:
    y.append(b.Eg(T=T) + b.VBO(T=T))
    label.append(b.name)

ax.plot(x, y, 'b.')
for x, y, label in zip(x, y, label):
    ax.annotate(label, xy=(x, y), xytext=(-5, 5), ha='right', va='bottom', bbox=dict(linewidth=0, fc='white', alpha=0.9), textcoords='offset points')

indices = numpy.arange(100)
fractions = numpy.linspace(0, 1, 100)
x = numpy.empty(100, dtype=numpy.float)
y = numpy.empty(100, dtype=numpy.float)
for tern in [alloy]:
    for i, f in zip(indices, fractions):
        instance = tern(x=f)
        x[i] = 1 - f
        y[i] = instance.Eg(T=T) + instance.VBO(T=T)

    ax.plot(x, y, 'b-')

x = [
 0, 1]
y = []
label = []
for b in alloy.binaries:
    y.append(b.VBO(T=T))
    label.append(b.name)

ax.plot(x, y, 'r.')
for x, y, label in zip(x, y, label):
    ax.annotate(label, xy=(x, y), xytext=(-5, 5), ha='right', va='bottom', bbox=dict(linewidth=0, fc='white', alpha=0.9), textcoords='offset points')

indices = numpy.arange(100)
fractions = numpy.linspace(0, 1, 100)
x = numpy.empty(100, dtype=numpy.float)
y = numpy.empty(100, dtype=numpy.float)
for tern in [alloy]:
    for i, f in zip(indices, fractions):
        instance = tern(x=f)
        x[i] = 1 - f
        y[i] = instance.VBO(T=T)

    ax.plot(x, y, 'r-')

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
        plt.savefig(output_filename)
    else:
        plt.show()