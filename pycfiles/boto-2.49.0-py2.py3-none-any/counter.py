# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/counter.py
# Compiled at: 2012-08-08 13:08:12
from operator import itemgetter
from heapq import nlargest
from itertools import repeat, ifilter
from ordereddict import OrderedDict

class Counter(dict):
    """Dict subclass for counting hashable objects.  Sometimes called a bag
    or multiset.  Elements are stored as dictionary keys and their counts
    are stored as dictionary values.

    >>> Counter('zyzygy')
    Counter({'y': 3, 'z': 2, 'g': 1})

    """

    def __init__(self, iterable=None, **kwds):
        """Create a new, empty Counter object.  And if given, count elements
        from an input iterable.  Or, initialize the count from another mapping
        of elements to their counts.

        >>> c = Counter()                           # a new, empty counter
        >>> c = Counter('gallahad')                 # a new counter from an iterable
        >>> c = Counter({'a': 4, 'b': 2})           # a new counter from a mapping
        >>> c = Counter(a=4, b=2)                   # a new counter from keyword args

        """
        self.update(iterable, **kwds)

    def __missing__(self, key):
        return 0

    def most_common(self, n=None):
        """List the n most common elements and their counts from the most
        common to the least.  If n is None, then list all element counts.

        >>> Counter('abracadabra').most_common(3)
        [('a', 5), ('r', 2), ('b', 2)]

        """
        if n is None:
            return sorted(self.iteritems(), key=itemgetter(1), reverse=True)
        else:
            return nlargest(n, self.iteritems(), key=itemgetter(1))

    def elements(self):
        """Iterator over elements repeating each as many times as its count.

        >>> c = Counter('ABCABC')
        >>> sorted(c.elements())
        ['A', 'A', 'B', 'B', 'C', 'C']

        If an element's count has been set to zero or is a negative number,
        elements() will ignore it.

        """
        for (elem, count) in self.iteritems():
            for _ in repeat(None, count):
                yield elem

        return

    @classmethod
    def fromkeys(cls, iterable, v=None):
        raise NotImplementedError('Counter.fromkeys() is undefined.  Use Counter(iterable) instead.')

    def update--- This code section failed: ---

 L.  79         0  LOAD_FAST             1  'iterable'
                3  LOAD_CONST               None
                6  COMPARE_OP            9  is-not
                9  JUMP_IF_FALSE       161  'to 173'
             12_0  THEN                     174
               12  POP_TOP          

 L.  80        13  LOAD_GLOBAL           1  'hasattr'
               16  LOAD_FAST             1  'iterable'
               19  LOAD_CONST               'iteritems'
               22  CALL_FUNCTION_2       2  None
               25  JUMP_IF_FALSE        92  'to 120'
             28_0  THEN                     170
               28  POP_TOP          

 L.  81        29  LOAD_FAST             0  'self'
               32  JUMP_IF_FALSE        65  'to 100'
               35  POP_TOP          

 L.  82        36  LOAD_FAST             0  'self'
               39  LOAD_ATTR             2  'get'
               42  STORE_FAST            3  'self_get'

 L.  83        45  SETUP_LOOP           69  'to 117'
               48  LOAD_FAST             1  'iterable'
               51  LOAD_ATTR             3  'iteritems'
               54  CALL_FUNCTION_0       0  None
               57  GET_ITER         
               58  FOR_ITER             35  'to 96'
               61  UNPACK_SEQUENCE_2     2 
               64  STORE_FAST            4  'elem'
               67  STORE_FAST            5  'count'

 L.  84        70  LOAD_FAST             3  'self_get'
               73  LOAD_FAST             4  'elem'
               76  LOAD_CONST               0
               79  CALL_FUNCTION_2       2  None
               82  LOAD_FAST             5  'count'
               85  BINARY_ADD       
               86  LOAD_FAST             0  'self'
               89  LOAD_FAST             4  'elem'
               92  STORE_SUBSCR     
               93  JUMP_BACK            58  'to 58'
               96  POP_BLOCK        
               97  JUMP_ABSOLUTE       170  'to 170'
            100_0  COME_FROM            32  '32'
              100  POP_TOP          

 L.  86       101  LOAD_GLOBAL           4  'dict'
              104  LOAD_ATTR             5  'update'
              107  LOAD_FAST             0  'self'
              110  LOAD_FAST             1  'iterable'
              113  CALL_FUNCTION_2       2  None
              116  POP_TOP          
            117_0  COME_FROM            45  '45'
              117  JUMP_ABSOLUTE       174  'to 174'
            120_0  COME_FROM            25  '25'
              120  POP_TOP          

 L.  88       121  LOAD_FAST             0  'self'
              124  LOAD_ATTR             2  'get'
              127  STORE_FAST            3  'self_get'

 L.  89       130  SETUP_LOOP           41  'to 174'
              133  LOAD_FAST             1  'iterable'
              136  GET_ITER         
              137  FOR_ITER             29  'to 169'
              140  STORE_FAST            4  'elem'

 L.  90       143  LOAD_FAST             3  'self_get'
              146  LOAD_FAST             4  'elem'
              149  LOAD_CONST               0
              152  CALL_FUNCTION_2       2  None
              155  LOAD_CONST               1
              158  BINARY_ADD       
              159  LOAD_FAST             0  'self'
              162  LOAD_FAST             4  'elem'
              165  STORE_SUBSCR     
              166  JUMP_BACK           137  'to 137'
              169  POP_BLOCK        
              170  JUMP_FORWARD          1  'to 174'
            173_0  COME_FROM             9  '9'
              173  POP_TOP          
            174_0  COME_FROM           130  '130'

 L.  91       174  LOAD_FAST             2  'kwds'
              177  JUMP_IF_FALSE        17  'to 197'
            180_0  THEN                     198
              180  POP_TOP          

 L.  92       181  LOAD_FAST             0  'self'
              184  LOAD_ATTR             5  'update'
              187  LOAD_FAST             2  'kwds'
              190  CALL_FUNCTION_1       1  None
              193  POP_TOP          
              194  JUMP_FORWARD          1  'to 198'
            197_0  COME_FROM           177  '177'
              197  POP_TOP          
            198_0  COME_FROM           194  '194'
              198  LOAD_CONST               None
              201  RETURN_VALUE     

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 117

    def copy(self):
        """Like dict.copy() but returns a Counter instance instead of a dict."""
        return Counter(self)

    def __delitem__(self, elem):
        """Like dict.__delitem__() but does not raise KeyError for missing values."""
        if elem in self:
            dict.__delitem__(self, elem)

    def __repr__(self):
        if not self:
            return '%s()' % self.__class__.__name__
        items = (', ').join(map(('%r: %r').__mod__, self.most_common()))
        return '%s({%s})' % (self.__class__.__name__, items)

    def __add__(self, other):
        """Add counts from two counters.

        >>> Counter('abbb') + Counter('bcc')
        Counter({'b': 4, 'c': 2, 'a': 1})

        """
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem in set(self) | set(other):
            newcount = self[elem] + other[elem]
            if newcount > 0:
                result[elem] = newcount

        return result

    def __sub__(self, other):
        """ Subtract count, but keep only results with positive counts.

        >>> Counter('abbbc') - Counter('bccd')
        Counter({'b': 2, 'a': 1})

        """
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem in set(self) | set(other):
            newcount = self[elem] - other[elem]
            if newcount > 0:
                result[elem] = newcount

        return result

    def __or__(self, other):
        """Union is the maximum of value in either of the input counters.

        >>> Counter('abbb') | Counter('bcc')
        Counter({'b': 3, 'c': 2, 'a': 1})

        """
        if not isinstance(other, Counter):
            return NotImplemented
        _max = max
        result = Counter()
        for elem in set(self) | set(other):
            newcount = _max(self[elem], other[elem])
            if newcount > 0:
                result[elem] = newcount

        return result

    def __and__(self, other):
        """ Intersection is the minimum of corresponding counts.

        >>> Counter('abbb') & Counter('bcc')
        Counter({'b': 1})

        """
        if not isinstance(other, Counter):
            return NotImplemented
        _min = min
        result = Counter()
        if len(self) < len(other):
            self, other = other, self
        for elem in ifilter(self.__contains__, other):
            newcount = _min(self[elem], other[elem])
            if newcount > 0:
                result[elem] = newcount

        return result


class OrderedCounter(OrderedDict, Counter):
    """Counter that remembers the order elements are first encountered"""

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, OrderedDict(self))

    def __reduce__(self):
        return (
         self.__class__, (OrderedDict(self),))


if __name__ == '__main__':
    import doctest
    print doctest.testmod()