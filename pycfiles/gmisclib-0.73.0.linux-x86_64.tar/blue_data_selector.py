# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/blue_data_selector.py
# Compiled at: 2010-07-20 16:10:29
"""This takes anticorrelated samples from a sequence of data.
In other words, it tends to choose data that have not been seen
frequently before.   With blueness=1, it never shows a sample
n times until all samples have been shown n-1 times.

(Note that it is possible for an item to appear twice in sucession,
if it appears as the Nth item in a set of N, then appears as the first
item in the second set of N.)
"""
import heapq, random, math

class bluedata(object):

    def __init__(self, data, blueness=2.0, rng=None):
        """@param data: data to sample
                @type data: list(whatever)
                @param blueness: How much should you avoid choosing the same item
                        in succession?      If -0.5 < C{blueness} < 0, then you are
                        more likely to choose the same item several times in a row.
                        If 0 <  C{blueness} < 1, you are unlikely to choose the same
                        item twice in succession (though it is possible).
                        If C{blueness} > 1, you will never get the same item twice
                        until you've run through the entire list of data.
                @type blueness: float
                @param rng: a random number generator, per the L{random} module.
                                You can generate repeated sequences of data by
                                repeatedly passing it a random number generator in the
                                same state.
                """
        assert blueness > -0.5
        if rng is None:
            self.r = random.Random()
        else:
            self.r = rng
        self.blue = float(blueness)
        self.q = [ (self.r.random(), datum) for datum in data ]
        heapq.heapify(self.q)
        return

    def add(self, datum):
        """Add another datum to be sampled.
                @type datum: whatever
                @param datum: thing to be added.   It
                        has a probability of C{1/len(self)} of being the next sample.
                """
        heapq.heappush(self.q, (self.q[0][0] + self.r.random() - 1.0 / float(len(self.q) + 1), datum))

    def pickiter(self, n):
        """Pick C{n} items from the data set.
                @param n: how many items to pick.
                @type n: int
                """
        for i in range(n):
            yield self.pick1()

    def pick1(self):
        u, d = heapq.heappop(self.q)
        heapq.heappush(self.q, (math.floor(u) + self.blue + self.r.random(), d))
        return d

    def pick(self, n):
        """Pick C{n} items from the data set.
                @param n: how many items to pick.
                @type n: int
                @rtype: list(whatever), with length==n
                """
        return list(self.pickiter(n))

    def peek(self):
        """Inspect (but do not remove) the next item to be picked.
                @return: the next item to be picked.
                @rtype: whatever (not a list!)
                """
        return self.q[0][1]

    def split--- This code section failed: ---

 L.  93         0  LOAD_FAST             1  'n'
                3  LOAD_GLOBAL           0  'len'
                6  LOAD_FAST             0  'self'
                9  LOAD_ATTR             1  'q'
               12  CALL_FUNCTION_1       1  None
               15  COMPARE_OP            1  <=
               18  POP_JUMP_IF_TRUE     30  'to 30'
               21  LOAD_ASSERT              AssertionError
               24  LOAD_CONST               'Split requires 0 <= n <= len.'
               27  RAISE_VARARGS_2       2  None

 L.  94        30  BUILD_LIST_0          0 
               33  STORE_FAST            2  'o1'

 L.  95        36  BUILD_LIST_0          0 
               39  STORE_FAST            3  'o2'

 L.  96        42  BUILD_LIST_0          0 
               45  STORE_FAST            4  'nq'

 L.  97        48  SETUP_LOOP          107  'to 158'
               51  LOAD_GLOBAL           0  'len'
               54  LOAD_FAST             2  'o1'
               57  CALL_FUNCTION_1       1  None
               60  LOAD_FAST             1  'n'
               63  COMPARE_OP            0  <
               66  POP_JUMP_IF_FALSE   157  'to 157'

 L.  98        69  LOAD_GLOBAL           3  'heapq'
               72  LOAD_ATTR             4  'heappop'
               75  LOAD_FAST             0  'self'
               78  LOAD_ATTR             1  'q'
               81  CALL_FUNCTION_1       1  None
               84  UNPACK_SEQUENCE_2     2 
               87  STORE_FAST            5  'u'
               90  STORE_FAST            6  'd'

 L.  99        93  LOAD_FAST             2  'o1'
               96  LOAD_ATTR             5  'append'
               99  LOAD_FAST             6  'd'
              102  CALL_FUNCTION_1       1  None
              105  POP_TOP          

 L. 100       106  LOAD_GLOBAL           3  'heapq'
              109  LOAD_ATTR             6  'heappush'
              112  LOAD_FAST             4  'nq'
              115  LOAD_GLOBAL           7  'int'
              118  LOAD_FAST             5  'u'
              121  CALL_FUNCTION_1       1  None
              124  LOAD_FAST             0  'self'
              127  LOAD_ATTR             8  'blue'
              130  BINARY_ADD       
              131  LOAD_FAST             0  'self'
              134  LOAD_ATTR             9  'r'
              137  LOAD_ATTR            10  'random'
              140  CALL_FUNCTION_0       0  None
              143  BINARY_ADD       
              144  LOAD_FAST             6  'd'
              147  BUILD_TUPLE_2         2 
              150  CALL_FUNCTION_2       2  None
              153  POP_TOP          
              154  JUMP_BACK            51  'to 51'
              157  POP_BLOCK        
            158_0  COME_FROM            48  '48'

 L. 101       158  SETUP_LOOP           77  'to 238'
              161  LOAD_FAST             0  'self'
              164  LOAD_ATTR             1  'q'
              167  GET_ITER         
              168  FOR_ITER             66  'to 237'
              171  UNPACK_SEQUENCE_2     2 
              174  STORE_FAST            5  'u'
              177  STORE_FAST            6  'd'

 L. 102       180  LOAD_FAST             3  'o2'
              183  LOAD_ATTR             5  'append'
              186  LOAD_FAST             6  'd'
              189  CALL_FUNCTION_1       1  None
              192  POP_TOP          

 L. 103       193  LOAD_GLOBAL           3  'heapq'
              196  LOAD_ATTR             6  'heappush'
              199  LOAD_FAST             4  'nq'
              202  LOAD_GLOBAL           7  'int'
              205  LOAD_FAST             5  'u'
              208  CALL_FUNCTION_1       1  None
              211  LOAD_FAST             0  'self'
              214  LOAD_ATTR             9  'r'
              217  LOAD_ATTR            10  'random'
              220  CALL_FUNCTION_0       0  None
              223  BINARY_ADD       
              224  LOAD_FAST             6  'd'
              227  BUILD_TUPLE_2         2 
              230  CALL_FUNCTION_2       2  None
              233  POP_TOP          
              234  JUMP_BACK           168  'to 168'
              237  POP_BLOCK        
            238_0  COME_FROM           158  '158'

 L. 104       238  LOAD_FAST             4  'nq'
              241  LOAD_FAST             0  'self'
              244  STORE_ATTR            1  'q'

 L. 105       247  LOAD_FAST             2  'o1'
              250  LOAD_FAST             3  'o2'
              253  BUILD_TUPLE_2         2 
              256  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 256

    def __iter__(self):
        """This iterator will produce samples forever."""
        while True:
            u, d = heapq.heappop(self.q)
            heapq.heappush(self.q, (int(u) + self.blue + self.r.random(), d))
            yield d

    def __len__(self):
        return len(self.q)

    def reset(self):
        """Forget prior history of usage.   Choices after this
                call are uncorrelated with choices before this call."""
        self.q = [ (self.r.random(), d) for u, d in self.q ]
        heapq.heapify(self.q)


def test():
    data = [
     0, 1, 2, 3, 4, 5, 6]
    x = bluedata(data)
    data.sort()
    o1 = x.pick(3)
    o2 = x.pick(4)
    o = o1 + o2
    o.sort()
    assert o == data
    o1 = x.pick(2)
    o2 = x.pick(5)
    o = o1 + o2
    o.sort()
    assert o == data
    o1 = x.pick(1)
    o2 = x.pick(6)
    o = o1 + o2
    o.sort()
    assert o == data
    o1 = x.pick(7)
    o2 = x.pick(0)
    o = o1 + o2
    o.sort()
    assert o == data
    o = x.pick(len(data))
    o.sort()
    assert o == data
    assert len(x) == len(data)
    tmp = []
    for i, q in enumerate(x):
        tmp.append(q)
        if len(tmp) >= len(data):
            break

    tmp.sort()
    assert tmp == data


if __name__ == '__main__':
    test()