# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/openbandparams/examples/Binaries.py
# Compiled at: 2015-04-09 02:47:55
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from openbandparams import *
print 'GaAs bandgap (at T = 300 K): ', GaAs.Eg(), 'eV'
print ''
print 'GaAs bandgap (at T = 300 K):  %.3f eV' % GaAs.Eg()
print 'GaAs Gamma-valley gap (at T = 300 K):  %.3f eV' % GaAs.Eg_Gamma()
print 'GaAs X-valley gap (at T = 300 K):  %.3f eV' % GaAs.Eg_X()
print 'GaAs bandgap (at T = 0 K):  %.3f eV' % GaAs.Eg(T=0)
print 'InAs bandgap (at T = 300 K):  %.3f eV' % InAs.Eg()
print ''
print 'GaAs electron effective mass in the Gamma-valley:  %.3f m0' % GaAs.meff_e_Gamma()
print ''
print 'GaAs electron effective mass in the X-valley in the longitudinal direction:  %.3f m0' % GaAs.meff_e_X_long()
print 'GaAs electron effective mass in the X-valley in the transverse direction:  %.3f m0' % GaAs.meff_e_X_trans()
print 'GaAs electron density-of-states effective mass in the X-valley:  %.3f m0' % GaAs.meff_e_X_DOS()
print ''
print 'GaAs electron effective mass in the L-valley in the longitudinal direction:  %.3f m0' % GaAs.meff_e_L_long()
print 'GaAs electron effective mass in the L-valley in the transverse direction:  %.3f m0' % GaAs.meff_e_L_trans()
print 'GaAs electron density-of-states effective mass in the L-valley:  %.3f m0' % GaAs.meff_e_L_DOS()
print ''
print 'GaAs heavy-hole effective mass in the [100] direction:  %.3f m0' % GaAs.meff_hh_100()
print 'GaAs heavy-hole effective mass in the [110] direction:  %.3f m0' % GaAs.meff_hh_110()
print 'GaAs heavy-hole effective mass in the [111] direction:  %.3f m0' % GaAs.meff_hh_111()
print ''
print 'GaAs light-hole effective mass in the [100] direction:  %.3f m0' % GaAs.meff_lh_100()
print 'GaAs light-hole effective mass in the [110] direction:  %.3f m0' % GaAs.meff_lh_110()
print 'GaAs light-hole effective mass in the [111] direction:  %.3f m0' % GaAs.meff_lh_111()
print ''
print 'GaAs split-off band effective mass:  %.3f m0' % GaAs.meff_SO()
print ''
import string
print ' Material | Lattice Param. [Ang] | Bandgap [eV]'
print '------------------------------------------------'
for mat in iii_v_zinc_blende_binaries:
    print string.rjust(str(mat), 7),
    try:
        a = mat.a()
    except:
        a = mat.a_300K()

    print '  | ', string.rjust('%.3f' % a, 12), '    ',
    print '  |    %.3f' % mat.Eg()