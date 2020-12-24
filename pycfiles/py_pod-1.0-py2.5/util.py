# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pod/util.py
# Compiled at: 2011-08-26 11:36:36
"""
Operations on matrices and various tools.

@author: Christophe Alexandre <ch.alexandre at bluewin dot ch>

@license:
Copyright(C) 2010 Christophe Alexandre

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/lgpl.txt>.
"""
import math, logging

class NullHandler(logging.Handler):
    """
  Null logging in order to avoid warning messages in client applications.
  """

    def emit(self, record):
        pass


_h = NullHandler()
_logger = logging.getLogger('util')
_logger.addHandler(_h)

def numbering(v):
    """ Maps every element of to its position."""
    return zip(range(len(v)), v)


def prod_scalar(v1, v2):
    assert len(v1) == len(v2), 'input vectors must be of the same size'
    prod = map(lambda x: x[0] * x[1], zip(v1, v2))
    return sum(prod)


def norm(v):
    return math.sqrt(prod_scalar(v, v))


def gauss_jordan(m, eps=1e-10):
    """
  Puts given matrix (2D array) into the Reduced Row Echelon Form.
  
  NOTE: make sure all the matrix items support fractions! Int matrix will NOT work!
  Written by Jarno Elonen in April 2005, released into Public Domain
     
  @return: True if successful, False if 'm' is singular.
  """
    h, w = len(m), len(m[0])
    for y in range(0, h):
        maxrow = y
        for y2 in range(y + 1, h):
            if abs(m[y2][y]) > abs(m[maxrow][y]):
                maxrow = y2

        m[y], m[maxrow] = m[maxrow], m[y]
        if abs(m[y][y]) <= eps:
            return False
        for y2 in range(y + 1, h):
            c = m[y2][y] / m[y][y]
            for x in range(y, w):
                m[y2][x] -= m[y][x] * c

    for y in range(h - 1, -1, -1):
        c = m[y][y]
        for y2 in range(0, y):
            for x in range(w - 1, y - 1, -1):
                m[y2][x] -= m[y][x] * m[y2][y] / c

        m[y][y] /= c
        for x in range(h, w):
            m[y][x] /= c

    return True


def system_solve(M, b):
    """
  solves M*x = b
  @param M: a matrix in the form of a list of list
  @param b: a vector in the form of a simple list of scalars
  @return: vector x so that M*x = b
  """
    m2 = [ row[:] + [right] for (row, right) in zip(M, b) ]
    return [ row[(-1)] for row in m2 ] if gauss_jordan(m2) else None


def mat_inverse(M):
    """
  @return: the inverse of the matrix M
  """
    m2 = [ row[:] + [ int(i == j) for j in range(len(M)) ] for (i, row) in enumerate(M) ]
    return [ row[len(M[0]):] for row in m2 ] if gauss_jordan(m2) else None


def zeros(size, zero=0):
    """
  @param size: a tuple containing dimensions of the matrix
  @param zero: the value to use to fill the matrix (zero by default)
  @return: matrix of dimension size
  """
    return [ zeros(s[1:]) for i in range(s[0]) ] if not len(s) else zero