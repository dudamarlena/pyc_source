# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mapy\model\grids.py
# Compiled at: 2017-04-20 23:08:42
# Size of source mod 2**32: 6897 bytes
import random as rdm, numpy as np
from alg3dpy.point import Point
from mapy.reader import user_setattr
from mapy.constants import CSYSGLOBAL, MAXID, FLOAT

class Grid(Point):
    __doc__ = '\n    The inheritance from the alg3dpy.Point class exists.\n    The array attribute is from Point class.\n\n    Attributes:\n    ____________________________________________________________________________\n    card       the card name (NASTRAN etc)\n    entryclass path to the class name\n    id         grid id\n    rcid       reference coordinate system id\n    rcobj      pointer to the reference coordinate system object\n    x1, x2, x3 coordinates\n    ocid       output coordsys id\n    ocobj      pointer to the ouptut coordsys\n    perm_cons  permanent constraints, applied to all load cases\n    seid       superelement id\n    cons       dictionary that will be filled with all constraints applied\n               to this grid\n    loads      dictionary that will be filled with all loads applied to\n               this grid\n    displ      dictionary that will store displacement resiults\n    pos        defines the grid position in the stiffness matrix\n               (for the solver)\n    k_offset   used by the solver to store positions in the stiffness\n               matrix, for each subcase\n    elements   all elements connected to this grid\n    garray     stores in a numpy array the original coordinates of this\n               grid\n    array      point-like coordinates, always given in the basic cartesian\n               coordinate system, used to create other coordsys\n    model      pointer to the model it belong to\n    rebuilt    pointer to the model it belong to\n    ____________________________________________________________________________\n\n    '
    __slots__ = ['card', 'entryclass', 'id', 'rcid', 'rcobj', 'x1', 'x2', 'x3',
     'ocid', 'ocobj', 'perm_cons', 'seid', 'loads', 'cons', 'displ',
     'pos', 'k_offset', 'elements', 'garray', 'array', 'model']

    def __init__(self, inputs={}):
        self.card = None
        self.entryclass = None
        self.id = int(MAXID * rdm.random())
        self.rcid = None
        self.rcobj = None
        self.x1 = None
        self.x2 = None
        self.x3 = None
        self.ocid = None
        self.ocobj = None
        self.perm_cons = set()
        self.seid = None
        self.cons = {}
        self.loads = {}
        self.displ = {}
        self.pos = -1
        self.k_offset = {}
        self.elements = {}
        self.garray = None
        self.array = None
        self.model = None
        self.rebuilt = False
        self = self.read_inputs(inputs)

    def read_inputs(self, inputs={}):
        self = user_setattr(self, inputs)
        if self.perm_cons.__class__.__name__ != 'set':
            str_perm_cons = self.perm_cons
            self.perm_cons = set([int(dof) for dof in str_perm_cons])
        if self.rcid == '' or self.rcid == None:
            self.rcid = 0
        if self.ocid == '' or self.ocid == None:
            self.ocid = 0
        if self.rcid == 0:
            self.rcobj = CSYSGLOBAL
        if self.ocid == 0:
            self.ocobj = CSYSGLOBAL
        self.garray = np.array([self.x1, self.x2, self.x3], dtype=FLOAT)

    def check_to_rebuild(self):
        self.rcobj = self.model.coorddict[int(self.rcid)]
        if self.rcobj.rebuilt:
            return True
        else:
            return False

    def rebuild(self):
        self.cons = {}
        self.loads = {}
        self.displ = {}
        self.pos = -1
        self.k_offset = {}
        self.elements = {}
        if self.rcobj.rebuilt:
            if self.rcobj.card == 'CORD1C' or self.rcobj.card == 'CORD2C':
                self.garray[1] = self.garray[1] * np.pi / 180.0
            if self.rcobj.card == 'CORD1S' or self.rcobj.card == 'CORD2S':
                self.garray[1] = self.garray[1] * np.pi / 180.0
                self.garray[2] = self.garray[2] * np.pi / 180.0
            array = self.rcobj.transform(self.garray, CSYSGLOBAL)
            super(Grid, self).__init__(array, self.id)
        else:
            print('The grid cannot be rebuilt, the coordsys has not')
            print('been updated...')
            raise ValueError()
        self.rebuilt = True

    def transform(self, new_csys=None):
        """
        This function checks for an existing reference coordinate system and it
        performs the transformation if necessary.
        See further description in mapy.model.coords.Coord().transform().
        """
        if self.rcobj == None:
            return self.array
        if self.rcobj.rebuilt:
            return self.rcobj.transform(self.array, new_csys)
        print('The transformation can not be done.')
        print('The grid rcobj (coordsys) was not rebuilt...')
        raise ValueError()

    def add2model(self, model):
        self.model = model
        model.griddict[self.id] = self

    def add_load(self, sub_id, dof, load):
        if int(sub_id) not in self.loads.keys():
            self.loads[sub_id] = [0 for i in range(6)]
        self.loads[sub_id][(dof - 1)] += load

    def add_cons(self, sub_id, dof):
        if int(sub_id) not in self.cons.keys():
            self.cons[sub_id] = set([])
        if dof not in self.cons[sub_id]:
            self.cons[sub_id].add(dof)
        else:
            print('Duplicated CONSTRAINT for GRID %d, dof %d' % (self.id, dof))

    def attach_displ(self, sub_id, displ_vec):
        self.displ[sub_id] = displ_vec

    def read_card():
        pass

    def print_card():
        pass

    def print_displ(self, sub_id):
        if sub_id in self.displ.keys():
            d = self.displ[sub_id]
            print('GRID,%d,SUB,%d,DISPL,%f,%f,%f,%f,%f,%f' % tuple([self.id, sub_id] + [t for t in d]))

    def __str__(self):
        return 'Grid ID %d:\n                \tCoord Sys ID %d:\n                \tx1 = %2.3f, x2 = %2.3f, x3 = %2.3f' % (
         self.id, self.rcid, self.array[0], self.array[1], self.array[2])

    def __repr__(self):
        return 'mapy.model.Grid class'