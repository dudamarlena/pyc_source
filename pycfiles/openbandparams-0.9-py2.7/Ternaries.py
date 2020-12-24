# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/openbandparams/examples/Ternaries.py
# Compiled at: 2015-04-09 02:47:55
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from openbandparams import *
print 'All three of these are identical:'
print '>>> AlGaAs(x=0.3).Eg()\n', AlGaAs(x=0.3).Eg()
print '>>> AlGaAs(Al=0.3).Eg()\n', AlGaAs(Al=0.3).Eg()
print '>>> AlGaAs(Ga=0.7).Eg()\n', AlGaAs(Ga=0.7).Eg()
print ''
print 'These two are identical:'
print '>>> AlGaAs(x=0.3).Eg_Gamma()\n', AlGaAs(x=0.3).Eg_Gamma()
print ''
print 'Alternate forms:'
print '>>> AlGaAs(x=0.3).Eg()\n', AlGaAs(x=0.3).Eg()
print '>>> AlGaAs(x=0.3).Eg(T=300)\n', AlGaAs(x=0.3).Eg(T=300)
print ''
print 'This is the preferred usage (more efficient),if you want multiple parameters from one alloy composition:'
print '>>> myAlGaAs = AlGaAs(x=0.3)\n',
myAlGaAs = AlGaAs(x=0.3)
print '>>> myAlGaAs.Eg()\n', myAlGaAs.Eg()
print '>>> myAlGaAs.Eg(T=300)\n', myAlGaAs.Eg(T=300)
print ''
print 'Lattice matching to a substrate (at the growth temperature):'
print '>>> a_InP = InP.a(T=800)\n',
a_InP = InP.a(T=800)
print '>>> GaInAs_on_InP = GaInAs(a=a_InP, T=800)\n',
GaInAs_on_InP = GaInAs(a=a_InP, T=800)
print '>>> InP.a(T=800)\n', InP.a(T=800)
print '>>> GaInAs_on_InP.a()\n', GaInAs_on_InP.a(T=800)
print '>>> GaInAs_on_InP.element_fraction("Ga")\n',
print GaInAs_on_InP.element_fraction('Ga')
print '>>> GaInAs_on_InP.Eg()\n', GaInAs_on_InP.Eg()
print ''
print 'Other examples:'
print '>>> AlGaAs.meff_hh_100(Al=0.3)\n', AlGaAs(Al=0.3).meff_hh_100()
print '>>> AlGaAs.meff_hh_110(Al=0.3)\n', AlGaAs(Al=0.3).meff_hh_110()
print '>>> AlGaAs.meff_hh_111(Al=0.3)\n', AlGaAs(Al=0.3).meff_hh_111()
print '>>> AlGaAs.meff_lh_100(Al=0.3)\n', AlGaAs(Al=0.3).meff_lh_100()
print '>>> AlGaAs.meff_lh_110(Al=0.3)\n', AlGaAs(Al=0.3).meff_lh_110()
print '>>> AlGaAs.meff_lh_111(Al=0.3)\n', AlGaAs(Al=0.3).meff_lh_111()
print ''