# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/openbandparams/examples/Plot_Bandgap_vs_Composition_of_Ternary.py
# Compiled at: 2015-07-09 16:42:41
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from openbandparams import *
import matplotlib.pyplot as plt, numpy
alloy = AlGaAs
xs = numpy.linspace(0, 1, 100)
T = 300
gamma = [ alloy(x=x).Eg_Gamma(T=T) for x in xs ]
X = [ alloy(x=x).Eg_X(T=T) for x in xs ]
L = [ alloy(x=x).Eg_L(T=T) for x in xs ]
fig = plt.figure()
ax = fig.add_subplot(111)
plt.title('%s (T = %.2g K)' % (alloy.name, T))
plt.xlabel('%s fraction' % alloy.elements[1])
plt.ylabel('Bandgap (eV)')
ax.plot(xs, gamma, 'r-', label='$\\Gamma$')
ax.plot(xs, X, 'g--', label='$X$')
ax.plot(xs, L, 'b:', label='$L$')
plt.legend(loc='best')
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
        plt.savefig(output_filename)
    else:
        plt.show()