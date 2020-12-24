# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/patricia/patricia/modppi/./src/SBI/structure/header/MiniRes.py
# Compiled at: 2018-02-02 06:38:52
from SBI.beans.IndexedNum import IndexedNum
from SBI.beans.JSONer import JSONer

class MiniResidue(JSONer):

    def __init__(self, restype, position):
        self._type = restype
        self._chain = None
        self._pos = None
        self._parse_position(position)
        return

    @property
    def restype(self):
        return self._type

    @property
    def chain(self):
        return self._chain

    @property
    def position(self):
        return int(self._pos)

    @property
    def idxp(self):
        return self._pos.index

    def _parse_position(self, position):
        self._chain = position[0]
        self._pos = IndexedNum(position[1:].strip())

    def as_dict(self):
        nobj = {}
        nobj['type'] = self.restype
        nobj['chain'] = self.chain
        nobj['pos'] = self.position
        nobj['idxp'] = self.idxp
        return nobj