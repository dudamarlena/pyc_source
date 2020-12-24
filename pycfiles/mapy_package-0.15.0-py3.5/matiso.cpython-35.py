# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mapy\model\materials\matiso.py
# Compiled at: 2017-04-20 23:14:18
# Size of source mod 2**32: 1758 bytes
from mapy.model.materials import Materials
from mapy.reader import user_setattr

class MatIso(Materials):
    __doc__ = '\n    Defines an isotropic material.\n\n    Attributes:\n    ____________________________________________________________________________\n    card       the card name (NASTRAN etc)\n    entryclass path to the class name\n    id         material id\n    e          Young Modulus\n    g          shear modulus\n    nu         Poisson\'s ratio\n    rho        especific mass (mass / volume)\n    a          thermal expansion coeffiecient\n    tref       reference temperature\n    damp       structural damping coefficient\n    st         allowable stress for tension\n    sc         allowable stress for compression\n    ss         allowable stress for shear\n    mcsid      material coordinate system NOT USED\n    ____________________________________________________________________________\n\n    Note: when the user defines "nu" and "g", the "g" will be recaculated\n          based on equation: e = 2*(1+nu)*g\n    ____________________________________________________________________________\n    '
    __slots__ = ['card', 'entryclass', 'id', 'e', 'g', 'nu', 'rho', 'a', 'tref',
     'damp', 'st', 'sc', 'ss', 'mcsid']

    def __init__(self, id=None, e=None, nu=None):
        super(MatIso, self).__init__()
        self.id = id
        self.e = e
        self.nu = nu
        self.g = None
        self.rho = None
        self.a = None
        self.tref = None
        self.dampcoe = None
        self.st = None
        self.sc = None
        self.ss = None
        self.mcsid = None

    def read_inputs(self, inputs={}):
        if len(inputs) > 0:
            self = user_setattr(self, inputs)