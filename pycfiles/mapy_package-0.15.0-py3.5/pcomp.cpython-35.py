# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mapy\model\properties\composite\pcomp.py
# Compiled at: 2017-04-12 19:32:03
# Size of source mod 2**32: 738 bytes
from mapy.model.properties.prop2d import Prop2D

class PropShellComp(Prop2D):
    __slots__ = [
     'card', 'entryclass', 'id', 'z0', 'nsm', 'sbmat', 'ft',
     'tref', 'dampc', 'lam', 'midlist', 'tlist', 'thetalist',
     'laminate']

    def __init__(self, inputs):
        super(PropShellComp, self).__init__()
        self.card = None
        self.entryclass = None
        self.id = None
        self.z0 = None
        self.nsm = None
        self.sbmat = None
        self.ft = None
        self.tref = None
        self.dampc = None
        self.lam = None
        self.midlist = []
        self.tlist = []
        self.thetalist = []
        self = user_setattr(self, inputs)