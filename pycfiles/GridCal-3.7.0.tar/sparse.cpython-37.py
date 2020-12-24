# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/santi/Documentos/GitHub/GridCal/src/GridCal/ThirdParty/pulp/sparse.py
# Compiled at: 2019-07-13 06:16:34
# Size of source mod 2**32: 3801 bytes
"""
sparse this module provides basic pure python sparse matrix implementation
notably this allows the sparse matrix to be output in various formats
"""

class Matrix(dict):
    __doc__ = '\n    This is a dictionary based sparse matrix class\n    '

    def __init__(self, rows, cols):
        """initialises the class by creating a matrix that will have the given
        rows and columns
        """
        self.rows = rows
        self.cols = cols
        self.rowdict = dict([(row, {}) for row in rows])
        self.coldict = dict([(col, {}) for col in cols])

    def add(self, row, col, item, colcheck=False, rowcheck=False):
        """

        :param row:
        :param col:
        :param item:
        :param colcheck:
        :param rowcheck:
        :return:
        """
        if rowcheck:
            if not row not in self.rows:
                if colcheck:
                    col not in self.cols or dict.__setitem__(self, (row, col), item)
                    self.rowdict[row][col] = item
                    self.coldict[col][row] = item
                else:
                    print(self.cols)
                    raise RuntimeError('col %s is not in the matrix columns' % col)
        else:
            raise RuntimeError('row %s is not in the matrix rows' % row)

    def addcol(self, col, rowitems):
        """
        adds a column
        :param col:
        :param rowitems:
        :return:
        """
        if col in self.cols:
            for row, item in rowitems.items():
                self.add(row, col, item, colcheck=False)

        else:
            raise RuntimeError('col is not in the matrix columns')

    def get(self, k, d=0):
        """

        :param k:
        :param d:
        :return:
        """
        return dict.get(self, k, d)

    def col_based_arrays(self):
        """

        :return:
        """
        numEls = len(self)
        elemBase = []
        startsBase = []
        indBase = []
        lenBase = []
        for i, col in enumerate(self.cols):
            startsBase.append(len(elemBase))
            elemBase.extend(list(self.coldict[col].values()))
            indBase.extend(list(self.coldict[col].keys()))
            lenBase.append(len(elemBase) - startsBase[(-1)])

        startsBase.append(len(elemBase))
        return (numEls, startsBase, lenBase, indBase, elemBase)


if __name__ == '__main__':
    rows = list(range(10))
    cols = list(range(50, 60))
    mat = Matrix(rows, cols)
    mat.add(1, 52, 'item')
    mat.add(2, 54, 'stuff')
    print(mat.col_based_arrays())