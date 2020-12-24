# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\internal\conjecture\pareto.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 13919 bytes
from enum import Enum
from sortedcontainers import SortedList
from hypothesis.internal.conjecture.data import ConjectureData, ConjectureResult, Status
from hypothesis.internal.conjecture.junkdrawer import LazySequenceCopy, swap
from hypothesis.internal.conjecture.shrinker import sort_key
NO_SCORE = float('-inf')

class DominanceRelation(Enum):
    NO_DOMINANCE = 0
    EQUAL = 1
    LEFT_DOMINATES = 2
    RIGHT_DOMINATES = 3


def dominance(left, right):
    """Returns the dominance relation between ``left`` and ``right``, according
    to the rules that one ConjectureResult dominates another if and only if it
    is better in every way.

    The things we currently consider to be "better" are:

        * Something that is smaller in shrinking order is better.
        * Something that has higher status is better.
        * Each ``interesting_origin`` is treated as its own score, so if two
          interesting examples have different origins then neither dominates
          the other.
        * For each target observation, a higher score is better.

    In "normal" operation where there are no bugs or target observations, the
    pareto front only has one element (the smallest valid test case), but for
    more structured or failing tests it can be useful to track, and future work
    will depend on it more."""
    if left.buffer == right.buffer:
        return DominanceRelation.EQUAL
    else:
        if sort_key(right.buffer) < sort_key(left.buffer):
            result = dominance(right, left)
            if result == DominanceRelation.LEFT_DOMINATES:
                return DominanceRelation.RIGHT_DOMINATES
        else:
            assert result == DominanceRelation.NO_DOMINANCE
            return result
            assert sort_key(left.buffer) < sort_key(right.buffer)
            if left.status < right.status:
                return DominanceRelation.NO_DOMINANCE
            return right.tags.issubset(left.tags) or DominanceRelation.NO_DOMINANCE
        if left.status == Status.INTERESTING and left.interesting_origin != right.interesting_origin:
            return DominanceRelation.NO_DOMINANCE
    for target in set(left.target_observations) | set(right.target_observations):
        left_score = left.target_observations.get(target, NO_SCORE)
        right_score = right.target_observations.get(target, NO_SCORE)
        if right_score > left_score:
            return DominanceRelation.NO_DOMINANCE
        return DominanceRelation.LEFT_DOMINATES


class ParetoFront:
    __doc__ = 'Maintains an approximate pareto front of ConjectureData objects. That\n    is, we try to maintain a collection of objects such that no element of the\n    collection is pareto dominated by any other. In practice we don\'t quite\n    manage that, because doing so is computationally very expensive. Instead\n    we maintain a random sample of data objects that are "rarely" dominated by\n    any other element of the collection (roughly, no more than about 10%).\n\n    Only valid test cases are considered to belong to the pareto front - any\n    test case with a status less than valid is discarded.\n\n    Note that the pareto front is potentially quite large, and currently this\n    will store the entire front in memory. This is bounded by the number of\n    valid examples we run, which is max_examples in normal execution, and\n    currently we do not support workflows with large max_examples which have\n    large values of max_examples very well anyway, so this isn\'t a major issue.\n    In future we may weish to implement some sort of paging out to disk so that\n    we can work with larger fronts.\n\n    Additionally, because this is only an approximate pareto front, there are\n    scenarios where it can be much larger than the actual pareto front. There\n    isn\'t a huge amount we can do about this - checking an exact pareto front\n    is intrinsically quadratic.\n\n    "Most" of the time we should be relatively close to the true pareto front,\n    say within an order of magnitude, but it\'s not hard to construct scenarios\n    where this is not the case. e.g. suppose we enumerate all valid test cases\n    in increasing shortlex order as s_1, ..., s_n, ... and have scores f and\n    g such that f(s_i) = min(i, N) and g(s_i) = 1 if i >= N, then the pareto\n    front is the set {s_1, ..., S_N}, but the only element of the front that\n    will dominate s_i when i > N is S_N, which we select with probability\n    1 / N. A better data structure could solve this, but at the cost of more\n    expensive operations and higher per element memory use, so we\'ll wait to\n    see how much of a problem this is in practice before we try that.\n    '

    def __init__(self, random):
        self._ParetoFront__random = random
        self._ParetoFront__eviction_listeners = []
        self.front = SortedList(key=(lambda d: sort_key(d.buffer)))
        self._ParetoFront__pending = None

    def add--- This code section failed: ---

 L. 141         0  LOAD_FAST                'data'
                2  LOAD_METHOD              as_result
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'data'

 L. 142         8  LOAD_FAST                'data'
               10  LOAD_ATTR                status
               12  LOAD_GLOBAL              Status
               14  LOAD_ATTR                VALID
               16  COMPARE_OP               <
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L. 143        20  LOAD_CONST               False
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L. 145        24  LOAD_FAST                'self'
               26  LOAD_ATTR                front
               28  POP_JUMP_IF_TRUE     46  'to 46'

 L. 146        30  LOAD_FAST                'self'
               32  LOAD_ATTR                front
               34  LOAD_METHOD              add
               36  LOAD_FAST                'data'
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          

 L. 147        42  LOAD_CONST               True
               44  RETURN_VALUE     
             46_0  COME_FROM            28  '28'

 L. 149        46  LOAD_FAST                'data'
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                front
               52  COMPARE_OP               in
               54  POP_JUMP_IF_FALSE    60  'to 60'

 L. 150        56  LOAD_CONST               True
               58  RETURN_VALUE     
             60_0  COME_FROM            54  '54'

 L. 156        60  LOAD_FAST                'self'
               62  LOAD_ATTR                front
               64  LOAD_METHOD              add
               66  LOAD_FAST                'data'
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          

 L. 157        72  LOAD_FAST                'self'
               74  LOAD_ATTR                _ParetoFront__pending
               76  LOAD_CONST               None
               78  COMPARE_OP               is
               80  POP_JUMP_IF_TRUE     86  'to 86'
               82  LOAD_ASSERT              AssertionError
               84  RAISE_VARARGS_1       1  'exception instance'
             86_0  COME_FROM            80  '80'

 L. 158     86_88  SETUP_FINALLY       566  'to 566'

 L. 159        90  LOAD_FAST                'data'
               92  LOAD_FAST                'self'
               94  STORE_ATTR               _ParetoFront__pending

 L. 165        96  LOAD_GLOBAL              LazySequenceCopy
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                front
              102  CALL_FUNCTION_1       1  ''
              104  STORE_FAST               'front'

 L. 170       106  BUILD_LIST_0          0 
              108  STORE_FAST               'to_remove'

 L. 177       110  LOAD_FAST                'self'
              112  LOAD_ATTR                front
              114  LOAD_METHOD              index
              116  LOAD_FAST                'data'
              118  CALL_METHOD_1         1  ''
              120  STORE_FAST               'i'

 L. 183       122  LOAD_CONST               0
              124  STORE_FAST               'failures'

 L. 184       126  LOAD_FAST                'i'
              128  LOAD_CONST               1
              130  BINARY_ADD       
              132  LOAD_GLOBAL              len
              134  LOAD_FAST                'front'
              136  CALL_FUNCTION_1       1  ''
              138  COMPARE_OP               <
          140_142  POP_JUMP_IF_FALSE   264  'to 264'
              144  LOAD_FAST                'failures'
              146  LOAD_CONST               10
              148  COMPARE_OP               <
          150_152  POP_JUMP_IF_FALSE   264  'to 264'

 L. 185       154  LOAD_FAST                'self'
              156  LOAD_ATTR                _ParetoFront__random
              158  LOAD_METHOD              randrange
              160  LOAD_FAST                'i'
              162  LOAD_CONST               1
              164  BINARY_ADD       
              166  LOAD_GLOBAL              len
              168  LOAD_FAST                'front'
              170  CALL_FUNCTION_1       1  ''
              172  CALL_METHOD_2         2  ''
              174  STORE_FAST               'j'

 L. 186       176  LOAD_GLOBAL              swap
              178  LOAD_FAST                'front'
              180  LOAD_FAST                'j'
              182  LOAD_GLOBAL              len
              184  LOAD_FAST                'front'
              186  CALL_FUNCTION_1       1  ''
              188  LOAD_CONST               1
              190  BINARY_SUBTRACT  
              192  CALL_FUNCTION_3       3  ''
              194  POP_TOP          

 L. 187       196  LOAD_FAST                'front'
              198  LOAD_METHOD              pop
              200  CALL_METHOD_0         0  ''
              202  STORE_FAST               'candidate'

 L. 188       204  LOAD_GLOBAL              dominance
              206  LOAD_FAST                'data'
              208  LOAD_FAST                'candidate'
              210  CALL_FUNCTION_2       2  ''
              212  STORE_FAST               'dom'

 L. 189       214  LOAD_FAST                'dom'
              216  LOAD_GLOBAL              DominanceRelation
              218  LOAD_ATTR                RIGHT_DOMINATES
              220  COMPARE_OP               !=
              222  POP_JUMP_IF_TRUE    228  'to 228'
              224  LOAD_ASSERT              AssertionError
              226  RAISE_VARARGS_1       1  'exception instance'
            228_0  COME_FROM           222  '222'

 L. 190       228  LOAD_FAST                'dom'
              230  LOAD_GLOBAL              DominanceRelation
              232  LOAD_ATTR                LEFT_DOMINATES
              234  COMPARE_OP               ==
              236  POP_JUMP_IF_FALSE   254  'to 254'

 L. 191       238  LOAD_FAST                'to_remove'
              240  LOAD_METHOD              append
              242  LOAD_FAST                'candidate'
              244  CALL_METHOD_1         1  ''
              246  POP_TOP          

 L. 192       248  LOAD_CONST               0
              250  STORE_FAST               'failures'
              252  JUMP_BACK           126  'to 126'
            254_0  COME_FROM           236  '236'

 L. 194       254  LOAD_FAST                'failures'
              256  LOAD_CONST               1
              258  INPLACE_ADD      
              260  STORE_FAST               'failures'
              262  JUMP_BACK           126  'to 126'
            264_0  COME_FROM           150  '150'
            264_1  COME_FROM           140  '140'

 L. 201       264  LOAD_FAST                'data'
              266  BUILD_LIST_1          1 
              268  STORE_FAST               'dominators'

 L. 203       270  LOAD_FAST                'i'
              272  LOAD_CONST               0
              274  COMPARE_OP               >=
          276_278  POP_JUMP_IF_FALSE   530  'to 530'
              280  LOAD_GLOBAL              len
              282  LOAD_FAST                'dominators'
              284  CALL_FUNCTION_1       1  ''
              286  LOAD_CONST               10
              288  COMPARE_OP               <
          290_292  POP_JUMP_IF_FALSE   530  'to 530'

 L. 204       294  LOAD_GLOBAL              swap
              296  LOAD_FAST                'front'
              298  LOAD_FAST                'i'
              300  LOAD_FAST                'self'
              302  LOAD_ATTR                _ParetoFront__random
              304  LOAD_METHOD              randint
              306  LOAD_CONST               0
              308  LOAD_FAST                'i'
              310  CALL_METHOD_2         2  ''
              312  CALL_FUNCTION_3       3  ''
              314  POP_TOP          

 L. 206       316  LOAD_FAST                'front'
              318  LOAD_FAST                'i'
              320  BINARY_SUBSCR    
              322  STORE_FAST               'candidate'

 L. 208       324  LOAD_CONST               False
              326  STORE_FAST               'already_replaced'

 L. 209       328  LOAD_CONST               0
              330  STORE_FAST               'j'

 L. 210       332  LOAD_FAST                'j'
              334  LOAD_GLOBAL              len
              336  LOAD_FAST                'dominators'
              338  CALL_FUNCTION_1       1  ''
              340  COMPARE_OP               <
          342_344  POP_JUMP_IF_FALSE   508  'to 508'

 L. 211       346  LOAD_FAST                'dominators'
              348  LOAD_FAST                'j'
              350  BINARY_SUBSCR    
              352  STORE_FAST               'v'

 L. 213       354  LOAD_GLOBAL              dominance
              356  LOAD_FAST                'candidate'
              358  LOAD_FAST                'v'
              360  CALL_FUNCTION_2       2  ''
              362  STORE_FAST               'dom'

 L. 214       364  LOAD_FAST                'dom'
              366  LOAD_GLOBAL              DominanceRelation
              368  LOAD_ATTR                LEFT_DOMINATES
              370  COMPARE_OP               ==
          372_374  POP_JUMP_IF_FALSE   450  'to 450'

 L. 215       376  LOAD_FAST                'already_replaced'
          378_380  POP_JUMP_IF_TRUE    404  'to 404'

 L. 216       382  LOAD_CONST               True
              384  STORE_FAST               'already_replaced'

 L. 217       386  LOAD_FAST                'candidate'
              388  LOAD_FAST                'dominators'
              390  LOAD_FAST                'j'
              392  STORE_SUBSCR     

 L. 218       394  LOAD_FAST                'j'
              396  LOAD_CONST               1
              398  INPLACE_ADD      
              400  STORE_FAST               'j'
              402  JUMP_FORWARD        438  'to 438'
            404_0  COME_FROM           378  '378'

 L. 221       404  LOAD_FAST                'dominators'
              406  LOAD_CONST               -1
              408  BINARY_SUBSCR    

 L. 222       410  LOAD_FAST                'dominators'
              412  LOAD_FAST                'j'
              414  BINARY_SUBSCR    

 L. 220       416  ROT_TWO          
              418  LOAD_FAST                'dominators'
              420  LOAD_FAST                'j'
              422  STORE_SUBSCR     
              424  LOAD_FAST                'dominators'
              426  LOAD_CONST               -1
              428  STORE_SUBSCR     

 L. 224       430  LOAD_FAST                'dominators'
              432  LOAD_METHOD              pop
              434  CALL_METHOD_0         0  ''
              436  POP_TOP          
            438_0  COME_FROM           402  '402'

 L. 225       438  LOAD_FAST                'to_remove'
              440  LOAD_METHOD              append
              442  LOAD_FAST                'v'
              444  CALL_METHOD_1         1  ''
              446  POP_TOP          
              448  JUMP_BACK           332  'to 332'
            450_0  COME_FROM           372  '372'

 L. 226       450  LOAD_FAST                'dom'
              452  LOAD_GLOBAL              DominanceRelation
              454  LOAD_ATTR                RIGHT_DOMINATES
              456  COMPARE_OP               ==
          458_460  POP_JUMP_IF_FALSE   478  'to 478'

 L. 227       462  LOAD_FAST                'to_remove'
              464  LOAD_METHOD              append
              466  LOAD_FAST                'candidate'
              468  CALL_METHOD_1         1  ''
              470  POP_TOP          

 L. 228   472_474  BREAK_LOOP          518  'to 518'
              476  JUMP_BACK           332  'to 332'
            478_0  COME_FROM           458  '458'

 L. 229       478  LOAD_FAST                'dom'
              480  LOAD_GLOBAL              DominanceRelation
              482  LOAD_ATTR                EQUAL
              484  COMPARE_OP               ==
          486_488  POP_JUMP_IF_FALSE   496  'to 496'

 L. 230   490_492  BREAK_LOOP          518  'to 518'
              494  JUMP_BACK           332  'to 332'
            496_0  COME_FROM           486  '486'

 L. 232       496  LOAD_FAST                'j'
              498  LOAD_CONST               1
              500  INPLACE_ADD      
              502  STORE_FAST               'j'
          504_506  JUMP_BACK           332  'to 332'
            508_0  COME_FROM           342  '342'

 L. 234       508  LOAD_FAST                'dominators'
              510  LOAD_METHOD              append
              512  LOAD_FAST                'candidate'
              514  CALL_METHOD_1         1  ''
              516  POP_TOP          

 L. 235       518  LOAD_FAST                'i'
              520  LOAD_CONST               1
              522  INPLACE_SUBTRACT 
              524  STORE_FAST               'i'
          526_528  JUMP_BACK           270  'to 270'
            530_0  COME_FROM           290  '290'
            530_1  COME_FROM           276  '276'

 L. 237       530  LOAD_FAST                'to_remove'
              532  GET_ITER         
              534  FOR_ITER            552  'to 552'
              536  STORE_FAST               'v'

 L. 238       538  LOAD_FAST                'self'
              540  LOAD_METHOD              _ParetoFront__remove
              542  LOAD_FAST                'v'
              544  CALL_METHOD_1         1  ''
              546  POP_TOP          
          548_550  JUMP_BACK           534  'to 534'

 L. 239       552  LOAD_FAST                'data'
              554  LOAD_FAST                'self'
              556  LOAD_ATTR                front
              558  COMPARE_OP               in
              560  POP_BLOCK        
              562  CALL_FINALLY        566  'to 566'
              564  RETURN_VALUE     
            566_0  COME_FROM           562  '562'
            566_1  COME_FROM_FINALLY    86  '86'

 L. 241       566  LOAD_CONST               None
              568  LOAD_FAST                'self'
              570  STORE_ATTR               _ParetoFront__pending
              572  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 562

    def on_evict(self, f):
        """Register a listener function that will be called with data when it
        gets removed from the front because something else dominates it."""
        self._ParetoFront__eviction_listeners.append(f)

    def __contains__(self, data):
        return isinstance(data, (ConjectureData, ConjectureResult)) and data.as_result in self.front

    def __iter__(self):
        return iter(self.front)

    def __getitem__(self, i):
        return self.front[i]

    def __len__(self):
        return len(self.front)

    def __remove(self, data):
        try:
            self.front.remove(data)
        except ValueError:
            return
        else:
            if data is not self._ParetoFront__pending:
                for f in self._ParetoFront__eviction_listeners:
                    f(data)


class ParetoOptimiser:
    __doc__ = 'Class for managing optimisation of the pareto front. That is, given the\n    current best known pareto front, this class runs an optimisation process\n    that attempts to bring it closer to the actual pareto front.\n\n    Currently this is fairly basic and only handles pareto optimisation that\n    works by reducing the test case in the shortlex order. We expect it will\n    grow more powerful over time.\n    '

    def __init__(self, engine):
        self._ParetoOptimiser__engine = engine
        self.front = self._ParetoOptimiser__engine.pareto_front

    def run(self):
        seen = set()
        i = len(self.front) - 1
        while i >= 0:
            assert self.front
            i = min(i, len(self.front) - 1)
            target = self.front[i]
            if target.buffer in seen:
                i -= 1
            else:
                shrunk = self._ParetoOptimiser__engine.shrink(target, lambda data: data.status >= Status.VALID and dominance(data, target) in (
                 DominanceRelation.EQUAL, DominanceRelation.LEFT_DOMINATES))
                seen.add(shrunk.buffer)
                i = self.front.front.bisect_left(target)