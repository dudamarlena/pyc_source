# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/openbandparams/examples/advanced/GaInAsSb_on_GaSb/Plot_Strained_Band_Offset_vs_Composition_of_Quaternary3.py
# Compiled at: 2015-04-09 02:47:55
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
from openbandparams import *
import matplotlib.pyplot as plt, numpy
alloy = GaInAsSb
T = 300
N = 100
xs = numpy.linspace(0, 1, N)
ys = numpy.linspace(0, 1, N)
X, Y = numpy.meshgrid(xs, ys)
Z = numpy.empty(shape=(N, N), dtype=numpy.double)
W = numpy.empty(shape=(N, N), dtype=numpy.double)
for i in xrange(N):
    for j in xrange(N):
        strained = alloy(x=X[(i, j)], y=Y[(i, j)]).strained_001(GaSb)
        strain = strained.strain_out_of_plane(T=T)
        if not 0.0 <= strain <= 0.03:
            Z[(i, j)] = numpy.nan
            W[(i, j)] = numpy.nan
        else:
            Z[(i, j)] = strained.VBO_hh(T=T) - GaSb.VBO()
            W[(i, j)] = GaSb.CBO() - strained.CBO(T=T)

fig = plt.figure()
CS = plt.contour(1 - X, 1 - Y, Z, 14, colors='r')
plt.clabel(CS, inline=True, fontsize=10)
CS2 = plt.contour(1 - X, 1 - Y, W, 12, colors='b')
plt.clabel(CS2, inline=True, fontsize=10)
plt.title('$%s/GaSb$ from 0 to 3%% strain (T = %.0f K)' % (alloy.latex(), T))
plt.xlabel('%s fraction' % alloy.elements[1])
plt.ylabel('%s fraction' % alloy.elements[3])
plt.plot([numpy.nan], [numpy.nan], 'b-', label='Conduction Band Offset')
plt.plot([numpy.nan], [numpy.nan], 'r-', label='Valance Band Offset')
plt.legend(loc='lower left')
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
        plt.savefig(output_filename)
    else:
        plt.show()