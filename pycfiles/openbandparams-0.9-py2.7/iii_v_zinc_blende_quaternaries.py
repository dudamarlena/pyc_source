# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/openbandparams/iii_v_zinc_blende_quaternaries.py
# Compiled at: 2015-04-09 02:47:55
from .iii_v_zinc_blende_quaternary import IIIVZincBlendeQuaternary
from .iii_v_zinc_blende_ternaries import AlGaN, AlInN, GaInN, AlGaP, AlInP, GaInP, AlGaAs, AlInAs, GaInAs, AlGaSb, AlInSb, GaInSb, AlNP, GaNP, InNP, AlNAs, GaNAs, InNAs, AlPAs, GaPAs, InPAs, AlPSb, GaPSb, InPSb, AlAsSb, GaAsSb, InAsSb
AlNPAs = IIIVZincBlendeQuaternary(name='AlNPAs', elements=('Al', 'N', 'P', 'As'), ternaries=(
 AlNP, AlNAs, AlPAs))
AlPAsSb = IIIVZincBlendeQuaternary(name='AlPAsSb', elements=('Al', 'P', 'As', 'Sb'), ternaries=(
 AlPAs, AlPSb, AlAsSb))
GaNPAs = IIIVZincBlendeQuaternary(name='GaNPAs', elements=('Ga', 'N', 'P', 'As'), ternaries=(
 GaNP, GaNAs, GaPAs))
GaPAsSb = IIIVZincBlendeQuaternary(name='GaPAsSb', elements=('Ga', 'P', 'As', 'Sb'), ternaries=(
 GaPAs, GaPSb, GaAsSb))
InNPAs = IIIVZincBlendeQuaternary(name='InNPAs', elements=('In', 'N', 'P', 'As'), ternaries=(
 InNP, InNAs, InPAs))
InPAsSb = IIIVZincBlendeQuaternary(name='InPAsSb', elements=('In', 'P', 'As', 'Sb'), ternaries=(
 InPAs, InPSb, InAsSb))
AlGaInN = IIIVZincBlendeQuaternary(name='AlGaInN', elements=('Al', 'Ga', 'In', 'N'), ternaries=(
 AlGaN, AlInN, GaInN))
AlGaInP = IIIVZincBlendeQuaternary(name='AlGaInP', elements=('Al', 'Ga', 'In', 'P'), ternaries=(
 AlGaP, AlInP, GaInP))
AlGaInAs = IIIVZincBlendeQuaternary(name='AlGaInAs', elements=('Al', 'Ga', 'In', 'As'), ternaries=(
 AlGaAs, AlInAs, GaInAs))
AlGaInSb = IIIVZincBlendeQuaternary(name='AlGaInSb', elements=('Al', 'Ga', 'In', 'Sb'), ternaries=(
 AlGaSb, AlInSb, GaInSb))
AlGaNP = IIIVZincBlendeQuaternary(name='AlGaNP', elements=('Al', 'Ga', 'N', 'P'), ternaries=(
 AlGaN, AlGaP, AlNP, GaNP))
AlGaNAs = IIIVZincBlendeQuaternary(name='AlGaNAs', elements=('Al', 'Ga', 'N', 'As'), ternaries=(
 AlGaN, AlGaAs, AlNAs, GaNAs))
AlGaPAs = IIIVZincBlendeQuaternary(name='AlGaPAs', elements=('Al', 'Ga', 'P', 'As'), ternaries=(
 AlGaP, AlGaAs, AlPAs, GaPAs))
AlGaPSb = IIIVZincBlendeQuaternary(name='AlGaPSb', elements=('Al', 'Ga', 'P', 'Sb'), ternaries=(
 AlGaP, AlGaSb, AlPSb, GaPSb))
AlGaAsSb = IIIVZincBlendeQuaternary(name='AlGaAsSb', elements=('Al', 'Ga', 'As', 'Sb'), ternaries=(
 AlGaAs, AlGaSb, AlAsSb, GaAsSb))
AlInNP = IIIVZincBlendeQuaternary(name='AlInNP', elements=('Al', 'In', 'N', 'P'), ternaries=(
 AlInN, AlInP, AlNP, InNP))
AlInNAs = IIIVZincBlendeQuaternary(name='AlInNAs', elements=('Al', 'In', 'N', 'As'), ternaries=(
 AlInN, AlInAs, AlNAs, InNAs))
AlInPAs = IIIVZincBlendeQuaternary(name='AlInPAs', elements=('Al', 'In', 'P', 'As'), ternaries=(
 AlInP, AlInAs, AlPAs, InPAs))
AlInPSb = IIIVZincBlendeQuaternary(name='AlInPSb', elements=('Al', 'In', 'P', 'Sb'), ternaries=(
 AlInP, AlInSb, AlPSb, InPSb))
AlInAsSb = IIIVZincBlendeQuaternary(name='AlInAsSb', elements=('Al', 'In', 'As', 'Sb'), ternaries=(
 AlInAs, AlInSb, AlAsSb, InAsSb))
GaInNP = IIIVZincBlendeQuaternary(name='GaInNP', elements=('Ga', 'In', 'N', 'P'), ternaries=(
 GaInN, GaInP, GaNP, InNP))
GaInNAs = IIIVZincBlendeQuaternary(name='GaInNAs', elements=('Ga', 'In', 'N', 'As'), ternaries=(
 GaInN, GaInAs, GaNAs, InNAs))
GaInPAs = IIIVZincBlendeQuaternary(name='GaInPAs', elements=('Ga', 'In', 'P', 'As'), ternaries=(
 GaInP, GaInAs, GaPAs, InPAs))
GaInPSb = IIIVZincBlendeQuaternary(name='GaInPSb', elements=('Ga', 'In', 'P', 'Sb'), ternaries=(
 GaInP, GaInSb, GaPSb, InPSb))
GaInAsSb = IIIVZincBlendeQuaternary(name='GaInAsSb', elements=('Ga', 'In', 'As', 'Sb'), ternaries=(
 GaInAs, GaInSb, GaAsSb, InAsSb))
iii_v_zinc_blende_quaternaries = [
 AlNPAs,
 AlPAsSb,
 GaNPAs,
 GaPAsSb,
 InNPAs,
 InPAsSb,
 AlGaInN, AlGaInP, AlGaInAs, AlGaInSb,
 AlGaNP, AlInNP, GaInNP,
 AlGaNAs, AlInNAs, GaInNAs,
 AlGaPAs, AlInPAs, GaInPAs,
 AlGaPSb, AlInPSb, GaInPSb,
 AlGaAsSb, AlInAsSb, GaInAsSb]
__all__ = [
 'iii_v_zinc_blende_quaternaries']
__all__ += [ quaternary.name for quaternary in iii_v_zinc_blende_quaternaries ]