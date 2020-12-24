# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/openbandparams/examples/GaPSb_on_InP.py
# Compiled at: 2015-04-09 02:47:55
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from openbandparams import *
print 'Lattice matching GaPSb to InP (at the growth temperature of 470 C):'
Tg = 743.15
print '>>> a_InP = InP.a(T=Tg)\n',
a_InP = InP.a(T=Tg)
print '>>> GaPSb_on_InP = GaPSb(a=a_InP, T=Tg)\n',
GaPSb_on_InP = GaInAs(a=a_InP, T=Tg)
print '>>> InP.a(T=Tg)\n', InP.a(T=Tg)
print '>>> GaPSb_on_InP.a()\n', GaPSb_on_InP.a(T=Tg)
print '>>> GaPSb_on_InP.element_fraction("Ga")\n',
print GaPSb_on_InP.element_fraction('Ga')
print '\nGet the properties at 70 C:'
T = 343.15
kT = 0.0258 / 300 * T
print 'Eg_Gamma', GaPSb_on_InP.Eg_Gamma(T=T)
print 'Eg_X', GaPSb_on_InP.Eg_X(T=T)
print 'Eg_L', GaPSb_on_InP.Eg_L(T=T)
xg = GaPSb_on_InP.Eg_X(T=T) - GaPSb_on_InP.Eg_Gamma(T=T)
print 'Eg_X - Eg_Gamma', xg
print '(Eg_X - Eg_Gamma)/kT', xg / kT
lg = GaPSb_on_InP.Eg_L(T=T) - GaPSb_on_InP.Eg_Gamma(T=T)
print 'Eg_L - Eg_Gamma', lg
print '(Eg_L - Eg_Gamma)/kT', lg / kT
meff_e_Gamma = GaPSb_on_InP.meff_e_Gamma(T=T)
print 'meff_e_Gamma', meff_e_Gamma
meff_e_L_long = GaPSb_on_InP.meff_e_L_long(T=T)
print 'meff_e_L_long', meff_e_L_long
meff_e_L_trans = GaPSb_on_InP.meff_e_L_trans(T=T)
print 'meff_e_L_trans', meff_e_L_trans
meff_e_L_DOS = GaPSb_on_InP.meff_e_L_long(T=T) ** (1.0 / 3) * GaPSb_on_InP.meff_e_L_trans(T=T) ** (2.0 / 3)
print 'meff_e_L_DOS', meff_e_L_DOS
DOS_ratio = meff_e_L_DOS ** (3.0 / 2) / meff_e_Gamma ** (3.0 / 2)
print 'meff_DOS_ratio', DOS_ratio