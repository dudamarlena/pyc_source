# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/patricia/patricia/modppi/./src/SBI/structure/header/BioMolecule.py
# Compiled at: 2018-02-02 06:38:52
import numpy as np
from SBI.beans.JSONer import JSONer

class BioMolecule(JSONer):

    def __init__(self, identifier):
        self._identifier = identifier
        self._matrices = []
        self._chains = set()

    @property
    def identifier(self):
        return self._identifier

    @property
    def chains(self):
        return self._chains

    @chains.setter
    def chains(self, value):
        if isinstance(value, list):
            self._chains.update(set(value))
        else:
            self._chains.add(value)

    @property
    def matrices(self):
        if len(self._matrices) > 0:
            return self._matrices
        else:
            return [
             MatrixAndVector.stillmatrix()]

    def new_matrix(self):
        self._matrices.append(MatrixAndVector.stillmatrix())

    def update_last_matrix(self, row, mx, my, mz, v):
        self._matrices[(-1)].update_matrix(row, mx, my, mz)
        self._matrices[(-1)].update_vector(row, v)

    def as_dict(self):
        data = {'id': self.identifier, 'chains': list(self.chains), 
           'matrices': [ x.as_dict() for x in self.matrices ]}
        return data

    def __len__(self):
        return len(self._matrices)


class MatrixAndVector(object):

    def __init__(self, matrix, vector):
        self._matrix = matrix
        self._vector = vector

    @property
    def matrix(self):
        return self._matrix

    @property
    def vector(self):
        return self._vector

    @staticmethod
    def stillmatrix():
        return MatrixAndVector(np.identity(3, float), np.zeros(3, float))

    def update_matrix(self, row, mx, my, mz):
        self._matrix[(int(row) - 1)][0] = float(mx)
        self._matrix[(int(row) - 1)][1] = float(my)
        self._matrix[(int(row) - 1)][2] = float(mz)

    def update_vector(self, row, v):
        self._vector[int(row) - 1] = float(v)

    def as_dict(self):
        data = {'matrix': self.matrix.tolist(), 'vector': self.vector.tolist()}
        return data