# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\cgp\utils\placevalue.py
# Compiled at: 2013-01-14 06:47:43
__doc__ = '\nMapping of integers to vectors [i0, i1, ...] with [n0, n1, ...] possible values.\n\nA Placevalue object can be indexed, iterated over, or converted to a list, \nreturning vectors corresponding to successive integers.\nConversely, vec2int() gives the integer corresponding to a given vector.\n\n.. rubric:: Usage\n\nDefault is most significant digit first, so that the last digit changes fastest.\n\n>>> p = Placevalue([2, 3, 4])\n\nIteration over vectors.\n\n>>> for i in p: print i                                     # doctest: +ELLIPSIS\n[0 0 0]\n[0 0 1]\n...\n[1 2 2]\n[1 2 3]\n\nIndexing.\n\n>>> p[13]                   # 1 * (3*4) + 0 * (4) + 1\narray([1, 0, 1])\n\nConversion from vector to integer.\n\n>>> p.vec2int([1,2,3])      # 1 * (3*4) + 2 * (4) + 3\n23\n\nConverting to list, equivalent to [i for i in p].\n\n>>> list(p)\n[array([0, 0, 0]), array([0, 0, 1]), ..., array([1, 2, 3])]\n\nA single array is more compact.\n\n>>> np.array(p)\narray([[0, 0, 0], [0, 0, 1], ..., [1, 2, 3]])\n\n.. rubric:: Named positions\n\nUsing a structured array with named fields to construct the Placevalue object.\n\n>>> dtype = [("a", np.int16), ("b", np.int16)]\n>>> pr = Placevalue(np.rec.fromrecords([[2,3]], dtype=dtype))\n>>> pr[7]\narray([(2, 1)], dtype=[(\'a\', \'<i2\'), (\'b\', \'<i2\')])\n>>> np.concatenate(pr)\narray([(0, 0), (0, 1), ..., (1, 1), (1, 2)], dtype=[(\'a\', \'<i2\'), (\'b\', \'<i2\')])\n\n.. rubric:: Details\n\nThe i-vectors correspond to a place-value system with prod(n) unique values.\nIf i[0] is the least significant digit, position j has value prod(n[:j]).\nThe default is to have i[0] as the most significant digit, as when reading \nnumbers left-to-right.\n\nThe integer is computed by multiplying each vector element with its place value \nand summing the result, just like 123 = 1*100 + 2*10 + 3*1.\n'
import operator, numpy as np
from .unstruct import unstruct

class Placevalue(object):
    """
    Map integers to vectors [i0, i1, ...] with [n0, n1, ...] possible values
    
    Default endianness is most significant digit first, like binary numbers.
    Endianness affects the value of digit positions and conversion from 
    integer to vector. Conversion from vector to integer is always sum(v*posval)
    
    >>> p = Placevalue([4, 3, 2])
    >>> np.array([p.int2vec(i) for i in range(p.maxint)])
    array([[0, 0, 0], [0, 0, 1], [0, 1, 0]...[3, 1, 1], [3, 2, 0], [3, 2, 1]])
    >>> b = Placevalue([2] * 8) # eight binary digits
    >>> b.int2vec(15)     # most significant digit first!
    array([0, 0, 0, 0, 1, 1, 1, 1])
    >>> Placevalue([3], names=["a"])
    Placevalue(rec.array([(3,)], dtype=[('a', '<i...
    
    .. rubric:: Named positions
    
    Passing a *names* argument makes the Placevalue object generate structured 
    ndarrays.
    
    >>> Placevalue([3, 4], names=["a", "b"])[0]
    array([(0, 0)], dtype=[('a', '...'), ('b', '...')])
    
    If a structured array is used to construct the Placevalue object, the same 
    dtype and field names are used for the vectors returned by int2vec(), 
    indexing or iterating.
    
    >>> dtype = [("a", np.int8), ("b", np.int8)]
    >>> pr = Placevalue(np.rec.fromrecords([[3, 4]], dtype=dtype))
    >>> pr[11]
    array([(2, 3)], dtype=[('a', '|i1'), ('b', '|i1')])
    
    To convert a structured ndarray to a recarray, use .view().
    
    >>> pr[11].view(np.recarray)
    rec.array([(2, 3)], dtype=[('a', '|i1'), ('b', '|i1')])    
    """

    def __init__(self, n=None, msd_first=True, names=None):
        """Constructor for :class:`Placevalue`."""
        if names:
            n = np.rec.fromrecords([n], names=names)
        self.n = np.atleast_1d(n).copy()
        self.u = np.atleast_1d(np.squeeze(unstruct(self.n)))
        self.fieldtype = self.u.dtype
        self.dtype = self.n.dtype
        self.msd_first = msd_first
        self.maxint = reduce(operator.mul, [ int(i) for i in self.u ])
        if msd_first:
            self.posval = np.r_[(1, self.u[:0:-1].astype(object).cumprod())][::-1]
        else:
            self.posval = np.r_[(1, self.u[:-1].astype(object).cumprod())]

    def __getitem__(self, i):
        """p[i] is a synonym for p.int2vec(i)."""
        return self.int2vec(i)

    def vec2int(self, v):
        """
        Integer corresponding to a vector [i0, i1, ...]
        
        The integer is computed by multiplying each element of i with its 
        place value and summing the result.
        
        >>> p = Placevalue([4, 3, 2])
        >>> p.vec2int([1, 2, 0])
        10
        >>> vmax = p.n - 1
        >>> vmax
        array([3, 2, 1])
        >>> p.vec2int(vmax) == p.maxint - 1 == 23
        True
        
        This function is vectorized:
        
        >>> arr = p.int2vec(range(3))
        >>> p.vec2int(arr)
        array([0, 1, 2], dtype=object)
        >>> arr = p.int2vec(range(p.maxint))
        >>> p.vec2int(arr.reshape(4,6,-1))
        array([[0, 1, 2, 3, 4, 5],
               [6, 7, 8, 9, 10, 11],
               [12, 13, 14, 15, 16, 17],
               [18, 19, 20, 21, 22, 23]], dtype=object)
        
        Structured dtype.
        
        >>> dtype = [("a", np.int8), ("b", np.int8)]
        >>> pr = Placevalue(np.rec.fromrecords([[3, 4]], dtype=dtype))
        >>> pr.vec2int(pr.int2vec(11))
        array([11], dtype=object)
        >>> pr.vec2int(np.concatenate(pr))
        array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], dtype=object)
        """
        v = unstruct(v)
        if False and len(v) != len(self.u):
            msg = 'Expected vector with {} elements, got {}: {}'
            raise ValueError(msg.format(len(self.u), len(v), v))
        if (v >= self.u).any():
            raise OverflowError('Digit exceeds allowed range of %s' % self.u)
        return (self.posval * v).sum(axis=v.ndim - 1)

    def int2vec(self, i):
        """
        Vector [i0, i1, ...] corresponding to an integer.
        
        >>> p = Placevalue([4, 3, 2])
        >>> p.int2vec(13)
        array([2, 0, 1])
        >>> sum(p.posval * p.int2vec(13)) # analogous to 123 == 1*100+2*10+3*1
        13
        
        This function is vectorized:
        
        >>> p.int2vec(range(p.maxint))
        array([[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [0, 2, 0], [0, 2, 1],
        ...    [3, 0, 0], [3, 0, 1], [3, 1, 0], [3, 1, 1], [3, 2, 0], [3, 2, 1]])
        
        Compare with "least significant first" place values:
        
        >>> p = Placevalue([4, 3, 2], msd_first=False)
        >>> p.int2vec(range(p.maxint))
        array([[0, 0, 0], [1, 0, 0], [2, 0, 0], [3, 0, 0], 
               [0, 1, 0], [1, 1, 0], [2, 1, 0], [3, 1, 0],
        ...    [0, 1, 1], [1, 1, 1], [2, 1, 1], [3, 1, 1],
               [0, 2, 1], [1, 2, 1], [2, 2, 1], [3, 2, 1]])
        
        Structured dtype.
        
        >>> dtype = [("a", np.int8), ("b", np.int8)]
        >>> pr = Placevalue(np.rec.fromrecords([[3, 4]], dtype=dtype))
        >>> pr.int2vec(11)
        array([(2, 3)], dtype=[('a', '|i1'), ('b', '|i1')])
        >>> np.concatenate(pr)
        array([(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), ..., (2, 3)],
            dtype=[('a', '|i1'), ('b', '|i1')])
        """
        i = np.atleast_1d(i).copy()
        result = np.zeros(i.shape + self.posval.shape, dtype=self.fieldtype)
        if self.msd_first:
            for pos, posval in enumerate(self.posval):
                result[:, pos], i = divmod(i, posval)

            result = result.squeeze()
        else:
            for pos, posval in enumerate(self.posval[::-1]):
                result[:, pos], i = divmod(i, posval)

            result = result[:, ::-1].squeeze()
        if len(self.u) == 1 and len(i) > 1:
            result = np.c_[result]
        return np.ascontiguousarray(result).view(self.dtype)

    def __repr__(self):
        """
        String representation of :class:`Placevalue`.
        
        >>> Placevalue([4, 3, 2])
        Placevalue(array([4, 3, 2]), msd_first=True)
        
        >>> dtype = [("a", np.int8), ("b", np.int8)]
        >>> Placevalue(np.rec.fromrecords([[3, 4]], dtype=dtype))
        Placevalue(rec.array([(3, 4)],
              dtype=[('a', '|i1'), ('b', '|i1')]), msd_first=True)
        """
        return '%s(%r, msd_first=%r)' % (
         self.__class__.__name__, self.n, self.msd_first)

    def __len__(self):
        """
        Alias for Placevalue.maxint.
        
        Defining len() for Placevalue objects allows concatenation with 
        numpy.concatenate(). Se also __array__().
        
        >>> dtype = [("a", np.int8), ("b", np.int8)]
        >>> pv = Placevalue(np.rec.fromrecords([[2, 2]], dtype=dtype))
        >>> len(pv)
        4
        >>> np.concatenate(pv)
        array([(0, 0), (0, 1), (1, 0), (1, 1)], 
              dtype=[('a', '|i1'), ('b', '|i1')])
        
        Use maxint instead if __len__ exceeds the range of fixed-size integers.
        
        >>> len(Placevalue([[2] * 64]))
        Traceback (most recent call last):
        OverflowError: long int too large to convert to int
        >>> Placevalue([[2] * 64]).maxint
        18446744073709551616L
        """
        return self.maxint

    def __array__(self):
        """
        Return an array enumerating all vectors of a Placevalue object.
        
        Without named fields, this returns a 2-d ndarray.
        
        >>> np.array(Placevalue([2, 2]))
        array([[0, 0],
        [0, 1],
        [1, 0],
        [1, 1]])
        
        With named fields, this returns a 1-d recarray.
        
        >>> dtype = [("a", np.int8), ("b", np.int8)]
        >>> pv = Placevalue(np.rec.fromrecords([[2, 2]], dtype=dtype))
        >>> np.array(pv)
        array([(0, 0), (0, 1), (1, 0), (1, 1)],
              dtype=[('a', '|i1'), ('b', '|i1')])
        """
        if self.dtype.names:
            return np.concatenate(self)
        else:
            return np.vstack(self)

    def __iter__(self):
        """
        Iterating over a Placevalue object returns successive vectors.
        
        >>> p = Placevalue([4, 3, 2])
        >>> np.array([i for i in p])
        array([[0, 0, 0], [0, 0, 1], [0, 1, 0]...[3, 1, 1], [3, 2, 0], [3, 2, 1]])
        """
        return (self.int2vec(i) for i in range(self.maxint))


def binarray(i, ndigits=0, dtype=int):
    """
    Numpy array of binary digits (most significant digit in position 0).
    
    >>> binarray(13)
    array([1, 1, 0, 1])
    >>> binarray(13, 8)
    array([0, 0, 0, 0, 1, 1, 0, 1])
    """
    result = [
     '0'] * ndigits
    s = bin(i)[2:]
    result[(-len(s)):] = s
    return np.array(result, dtype=dtype)


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)