# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\cgp\utils\thinrange.py
# Compiled at: 2012-01-20 11:02:16
__doc__ = 'Thinning a sequence (list, array, ...) to a specified number of elements.'
import numpy as np

def thin(before, after, eps=1e-08):
    """
    Thinning a sequence (list, array, ...) to a specified number of elements.
    
    The second argument specifies how many elements to return. The indices of 
    these elements will be evenly spaced except for roundoff. Pass after=None 
    for no thinning.
    The first argument may be the sequence to thin. If the first argument is an 
    integer N, the sequence to thin will be numpy.arange(N).
    
    Indices to thin from 7 to 4 elements:
    
    >>> before = 7; after = 4
    >>> thin(before, after)
    array([0, 2, 4, 6])

    Using "after" > "before" performs nearest-value interpolation:
    
    >>> thin(4, 7)
    array([0, 0, 1, 1, 2, 3, 3])
    
    Thinning a list:
    
    >>> a = range(12, 78)
    >>> thin(a, 7)
    [12, 22, 33, 44, 55, 66, 77]
    
    Thinning an array:
    
    >>> a = np.reshape(range(56), (14, 4))
    >>> thin(a, 3)
    array([[ 0,  1,  2,  3],
           [24, 25, 26, 27],
           [52, 53, 54, 55]])
    
    Verify that after=None returns the original sequence.
    
    >>> thin(4, None)
    array([0, 1, 2, 3])
    
    Verifying that there are no duplicate elements in the result:
    
    >>> LL = [thin(before, after).tolist() for after in 1 + np.arange(before)]
    >>> all(len(L)==len(np.unique(L)) for L in LL)
    True
    >>> LL # doctest: +NORMALIZE_WHITESPACE
    [[0],
     [0, 6],
     [0, 3, 6],
     [0, 2, 4, 6],
     [0, 1, 3, 5, 6],
     [0, 1, 2, 4, 5, 6],
     [0, 1, 2, 3, 4, 5, 6]]
    """
    try:
        x = before
        before = len(before)
    except TypeError:
        x = None

    if after is None:
        after = before
    i = np.linspace(0, before - eps, after).astype(int)
    if x is None:
        return i
    else:
        try:
            return x[i]
        except TypeError:
            return [ x[j] for j in i ]

        return


if __name__ == '__main__':
    import doctest
    doctest.testmod()