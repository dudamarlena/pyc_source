# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/openbandparams/examples/Quaternaries.py
# Compiled at: 2015-04-09 02:47:55
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from openbandparams import *
print 'Type 1 Quaternary:', AlPAsSb
assert AlPAsSb(x=0, y=0) == AlPAsSb(P=0, y=0)
assert AlPAsSb(x=0, y=0) == AlPAsSb(x=0, As=0)
assert AlPAsSb(x=0, y=0) == AlPAsSb(P=0, As=0)
assert AlPAsSb(x=0, y=0) == AlPAsSb(P=0, Sb=1)
assert AlPAsSb(x=0, y=0) != GaPAsSb(x=0, y=0)
assert AlPAsSb(x=0, y=0) != AlPAsSb(x=1, y=0)
assert AlPAsSb(x=0, y=0) != AlPAsSb(x=0, y=1)
print 'Type 2 Quaternary:', AlGaInAs
assert AlGaInAs(x=0, y=0) == AlGaInAs(Al=0, y=0)
assert AlGaInAs(x=0, y=0) == AlGaInAs(x=0, Ga=0)
assert AlGaInAs(x=0, y=0) == AlGaInAs(Al=0, Ga=0)
assert AlGaInAs(x=0, y=0) == AlGaInAs(Al=0, In=1)
assert AlGaInAs(x=0, y=0) != AlGaInSb(x=0, y=0)
assert AlGaInAs(x=0, y=0) != AlGaInAs(x=1, y=0)
assert AlGaInAs(x=0, y=0) != AlGaInAs(x=0, y=1)
print 'Type 3 Quaternary:', AlGaPAs
assert AlGaPAs(x=0, y=0) == AlGaPAs(Al=0, y=0)
assert AlGaPAs(x=0, y=0) == AlGaPAs(x=0, P=0)
assert AlGaPAs(x=0, y=0) == AlGaPAs(Al=0, P=0)
assert AlGaPAs(x=0, y=0) == AlGaPAs(Ga=1, P=0)
assert AlGaPAs(x=0, y=0) == AlGaPAs(Al=0, As=1)
assert AlGaPAs(x=0, y=0) == AlGaPAs(Ga=1, As=1)
assert AlGaPAs(x=0, y=0) != AlGaPSb(x=0, y=0)
assert AlGaPAs(x=0, y=0) != AlGaPAs(x=1, y=0)
assert AlGaPAs(x=0, y=0) != AlGaPAs(x=0, y=1)
print ''
print repr(GaInPAs(x=0, y=0)), '-->', GaInPAs(x=0, y=0)
print repr(AlPAsSb(x=0, y=0)), '-->', AlPAsSb(x=0, y=0)
assert eval(repr(GaInPAs(Ga=0, P=0))) == GaInPAs(x=0, P=0)
print ''
print 'Some GaInPAs alloys lattice matched to InP (at room temperature):'
print repr(GaInPAs(Ga=0.1, a=InP.a()))
print repr(GaInPAs(As=0.1, a=InP.a()))
print ''
print 'Some AlPAsSb alloys lattice matched to InP (at room temperature):'
print repr(AlPAsSb(P=0.1, a=InP.a()))
print repr(AlPAsSb(As=0.1, a=InP.a()))
print repr(AlPAsSb(Sb=0.5, a=InP.a()))