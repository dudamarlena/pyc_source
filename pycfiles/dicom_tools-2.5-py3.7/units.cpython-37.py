# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/units.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 1402 bytes
SI_PREFIXES = 'yzafpnum kMGTPEZY'
UNITS = 'm,s,g,W,J,V,A,F,T,Hz,Ohm,S,N,C,px,b,B'.split(',')
allUnits = {}

def addUnit(p, n):
    g = globals()
    v = 1000 ** n
    for u in UNITS:
        g[p + u] = v
        allUnits[p + u] = v


for p in SI_PREFIXES:
    if p == ' ':
        p = ''
        n = 0
    else:
        if p == 'u':
            n = -2
        else:
            n = SI_PREFIXES.index(p) - 8
    addUnit(p, n)

cm = 0.01

def evalUnits(unitStr):
    """
    Evaluate a unit string into ([numerators,...], [denominators,...])
    Examples:
        N m/s^2   =>  ([N, m], [s, s])
        A*s / V   =>  ([A, s], [V,])
    """
    pass


def formatUnits(units):
    """
    Format a unit specification ([numerators,...], [denominators,...])
    into a string (this is the inverse of evalUnits)
    """
    pass


def simplify(units):
    """
    Cancel units that appear in both numerator and denominator, then attempt to replace 
    groups of units with single units where possible (ie, J/s => W)
    """
    pass