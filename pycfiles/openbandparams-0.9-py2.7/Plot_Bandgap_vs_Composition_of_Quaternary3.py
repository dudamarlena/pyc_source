# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/openbandparams/examples/Plot_Bandgap_vs_Composition_of_Quaternary3.py
# Compiled at: 2015-06-18 10:36:06
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from openbandparams import *
import matplotlib.pyplot as plt, numpy
alloy = GaInPAs
T = 300
N = 100
xs = numpy.linspace(0, 1, N)
ys = numpy.linspace(0, 1, N)
X, Y = numpy.meshgrid(xs, ys)
Z = numpy.empty(shape=(N, N), dtype=numpy.double)
for i in xrange(N):
    for j in xrange(N):
        Z[(i, j)] = alloy(x=X[(i, j)], y=Y[(i, j)]).Eg(T=T)

fig = plt.figure()
CS = plt.contour(1 - X, 1 - Y, Z, 10, colors='k')
plt.clabel(CS, inline=True, fontsize=10)
plt.title('$%s$ (T = %.0f K)' % (alloy.latex(), T))
plt.xlabel('%s fraction' % alloy.elements[1])
plt.ylabel('%s fraction' % alloy.elements[3])
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
        plt.savefig(output_filename)
    else:
        plt.show()