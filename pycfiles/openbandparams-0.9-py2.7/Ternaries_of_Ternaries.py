# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/openbandparams/examples/Ternaries_of_Ternaries.py
# Compiled at: 2015-04-09 02:47:55
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from openbandparams import *
AlInAs_InP = AlInAs(a=InP.a())
GaInAs_InP = GaInAs(a=InP.a())
AlGaInAs_InP = IIIVZincBlendeTernary(name='AlGaInAs/InP', elements=('Al', 'Ga', 'InAs'), binaries=(
 AlInAs_InP, GaInAs_InP), parameters=[])
instance1 = AlGaInAs_InP(Al=0.5)
print instance1.latex()
print 'instance1.Eg =', instance1.Eg()
GaInAs_InP.set_parameter(ValueParameter('Eg_Gamma', 1.0, 'eV'))
print 'instance1.Eg =', instance1.Eg()
instance1.set_parameter(ValueParameter('Eg_Gamma_bowing', 1.0, 'eV'))
print 'instance1.Eg =', instance1.Eg()
instance2 = AlGaInAs_InP(Al=0.5)
print 'instance2.Eg =', instance2.Eg()
instance1_copy = instance1(Al=0.5)
print 'instance1_copy.Eg =', instance1_copy.Eg()
instance1.set_parameter(ValueParameter('Eg_Gamma_bowing', 2.0, 'eV'))
print 'instance1.Eg =', instance1.Eg()
print 'instance1_copy.Eg =', instance1_copy.Eg()
AlGaInAs_InP.set_parameter(ValueParameter('Eg_Gamma_bowing', 3.0, 'eV'))
print 'instance1.Eg =', instance1.Eg()
print 'instance2.Eg =', instance2.Eg()
instance3 = AlGaInAs_InP(Al=0.5)
print 'instance3.Eg =', instance3.Eg()
instance4 = AlGaInAs_InP(Al=0.5)
print 'instance4.Eg =', instance4.Eg()