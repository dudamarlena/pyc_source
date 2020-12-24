# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/openbandparams/examples/Plot_Conduction_Band_Offset_vs_Lattice_Constant.py
# Compiled at: 2015-04-09 02:47:55
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from openbandparams import *
import matplotlib.pyplot as plt, numpy
T = 300
T_lattice = 300
fig = plt.figure()
ax = fig.add_subplot(111)
plt.xlabel('Lattice Parameter at %g K ($\\AA$)' % T_lattice)
plt.ylabel('Conduction Band Offsets at %g K (eV)' % T)
red = '#FE0303'
green = '#04A004'
blue = '#0404FF'
red_green = '#8D8D04'
red_blue = '#8D048D'
green_blue = '#04AEAE'
phosphide_binaries = [
 AlP, GaP, InP]
arsenide_binaries = [AlAs, GaAs, InAs]
antimonide_binaries = [AlSb, GaSb, InSb]
phosphide_ternaries = [
 AlGaP, AlInP, GaInP]
arsenide_ternaries = [AlGaAs, AlInAs, GaInAs]
antimonide_ternaries = [AlGaSb, AlInSb, GaInSb]
phosphide_arsenide_ternaries = [AlPAs, GaPAs, InPAs]
phosphide_antimonide_ternaries = [AlPSb, GaPSb, InPSb]
arsenide_antimonide_ternaries = [AlAsSb, GaAsSb, InAsSb]
fractions = numpy.linspace(0, 1, 1000)
for ternaries, color in [(phosphide_ternaries, red),
 (
  arsenide_ternaries, green),
 (
  antimonide_ternaries, blue),
 (
  phosphide_arsenide_ternaries, red_green),
 (
  phosphide_antimonide_ternaries, red_blue),
 (
  arsenide_antimonide_ternaries, green_blue)]:
    for ternary in ternaries:
        ax.plot([ ternary(x=f).a(T=T_lattice) for f in fractions ], [ ternary(x=f).VBO(T=T) + ternary(x=f).Eg(T=T) for f in fractions
                                                                    ], color=color, linewidth=1.2)

x = []
y = []
label = []
for binaries, color in [(phosphide_binaries, red),
 (
  arsenide_binaries, green),
 (
  antimonide_binaries, blue)]:
    ax.plot([ b.a(T=T_lattice) for b in binaries ], [ b.VBO(T=T) + b.Eg(T=T) for b in binaries ], color=color, linestyle=' ', marker='o', markersize=4, markeredgecolor=color)
    x.extend([ b.a(T=T_lattice) for b in binaries ])
    y.extend([ b.VBO(T=T) + b.Eg(T=T) for b in binaries ])
    label.extend([ b.name for b in binaries ])

for x, y, label in zip(x, y, label):
    ax.annotate(label, xy=(x, y), xytext=(-5, 5), ha='right', va='bottom', bbox=dict(linewidth=0, fc='white', alpha=0.9), textcoords='offset points')

xmin, xmax = plt.xlim()
plt.xlim(xmin - 0.05, xmax)
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
        plt.savefig(output_filename)
    else:
        plt.show()