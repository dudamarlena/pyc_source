# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\gt\genotype.py
# Compiled at: 2012-02-03 05:34:19
"""
Enumerate haploid or diploid genotypes with two alleles at *n* loci.

.. inheritance-diagram:: cgp.utils.placevalue.Placevalue Genotype

These classes are suitable for studies enumerating or sampling from all possible
genotypes. For a single locus, the three genotypes *aa, Aa, AA* map to 0, 1, 2
respectively. Thus, for instance, the three-locus genotype *AabbCC* would be
``[1, 0, 2]``. Such a vector representation of a genotype could be fed into a
genotype-to-parameter map function. An efficient mapping of each genotype to a
unique integer index facilitates easy sampling and indexing. We can list all
vectors/genotypes of a placevalue/genotype object by converting it to an array.

Here is an example with two biallelic loci::

    >>> pv = Placevalue([3, 3])
    >>> pv.int2vec(0)  # Genotype aabb
    array([0, 0])
    >>> AaBB = [1, 2]
    >>> pv.vec2int(AaBB)  # 1 * 3**1 + 2 * 3**0
    5
    >>> np.array(pv)
    array([[0, 0],
           [0, 1],
           [0, 2],
           [1, 0],
           [1, 1],
           [1, 2],
           [2, 0],
           [2, 1],
           [2, 2]])

The difference between class Genotype and Placevalue lies in how they order
genotypes. Class :class:`Genotype` puts  heterozygotes first, ensuring that 
the first :math:`3^k` genotypes make up a :math:`3^k` full factorial design 
in the first *k* parameters::

    >>> np.array(Genotype([3, 3]))
    array([[1, 1],
           [1, 0],
           [1, 2],
           [0, 1],
           [0, 0],
           [0, 2],
           [2, 1],
           [2, 0],
           [2, 2]])
"""
import numpy as np
from ..utils.placevalue import Placevalue
from ..utils.unstruct import unstruct

class Genotype(Placevalue):
    """
    Enumerate haploid or diploid genotypes with two alleles at *n* loci.
    
    Within each locus, levels are given in order [1, 0, 2], for 
    the baseline heterozygote, low homozygote, and high homozygote.
    This ensures that the first 3**k genotypes make up a full factorial design 
    with k factors, keeping the remaining n-k loci as heterozygotes.
    
    See :mod:`genotype` for examples.
    
    If a *names* argument is given, *n* can be omitted and defaults to 
    [3] * len(names).
    
    >>> Genotype(names=["a", "b"])
    Genotype(rec.array([(3, 3)], dtype=[('a', '...'), ('b', '...

    """
    code = np.array([1, 0, 2])

    def int2vec(self, i):
        """
        Vector [i0, i1, ...] corresponding to an integer. Code order = 1, 0, 2.
        
        >>> gt = Genotype(np.rec.fromrecords([[3, 3]], names=["a", "b"]))

        The heterozygote (baseline) scenario comes first.
        
        >>> gt.int2vec(0) == np.array([(1, 1)], dtype=[('a', int), ('b', int)])
        array([ True], dtype=bool)        
        >>> np.concatenate(gt)
        array([(1, 1), (1, 0), (1, 2), 
               (0, 1), (0, 0), (0, 2), 
               (2, 1), (2, 0), (2, 2)], dtype=[('a', '<i...'), ('b', '<i...')])
        """
        v = super(Genotype, self).int2vec(i)
        vi = v.view(self.fieldtype)
        vi[:] = self.code[vi]
        return v

    def vec2int(self, v):
        """
        Integer corresponding to a vector [i0, i1, ...]. Code order = 1, 0, 2.
        
        >>> gt = Genotype(np.rec.fromrecords([[3, 3]], names=["a", "b"]))
        >>> gt.vec2int([1, 1])
        0
        >>> v = np.concatenate(gt)
        >>> gt.vec2int(v)
        array([0, 1, 2, 3, 4, 5, 6, 7, 8], dtype=object)
        """
        return super(Genotype, self).vec2int(self.code[unstruct(v)])

    def __init__--- This code section failed: ---

 L. 109         0  LOAD_FAST             1  'n'
                3  POP_JUMP_IF_TRUE     28  'to 28'

 L. 110         6  LOAD_CONST               3
                9  BUILD_LIST_1          1 
               12  LOAD_GLOBAL           0  'len'
               15  LOAD_FAST             3  'names'
               18  CALL_FUNCTION_1       1  None
               21  BINARY_MULTIPLY  
               22  STORE_FAST            1  'n'
               25  JUMP_FORWARD          0  'to 28'
             28_0  COME_FROM            25  '25'

 L. 111        28  LOAD_CONST               'Genotype only implemented for biallelic loci'
               31  STORE_FAST            4  'msg'

 L. 112        34  LOAD_GLOBAL           1  'all'
               37  LOAD_GLOBAL           2  'unstruct'
               40  LOAD_FAST             1  'n'
               43  CALL_FUNCTION_1       1  None
               46  LOAD_ATTR             3  'squeeze'
               49  CALL_FUNCTION_0       0  None
               52  LOAD_CONST               3
               55  COMPARE_OP            1  <=
               58  CALL_FUNCTION_1       1  None
               61  POP_JUMP_IF_TRUE     73  'to 73'
               64  LOAD_ASSERT              AssertionError
               67  LOAD_FAST             4  'msg'
               70  RAISE_VARARGS_2       2  None

 L. 113        73  LOAD_GLOBAL           5  'super'
               76  LOAD_GLOBAL           6  'Genotype'
               79  LOAD_FAST             0  'self'
               82  CALL_FUNCTION_2       2  None
               85  LOAD_ATTR             7  '__init__'
               88  LOAD_FAST             1  'n'
               91  LOAD_FAST             2  'msd_first'
               94  LOAD_FAST             3  'names'
               97  CALL_FUNCTION_3       3  None
              100  POP_TOP          

Parse error at or near `CALL_FUNCTION_3' instruction at offset 97


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)