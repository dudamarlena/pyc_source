# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\strategies\_internal\recursive.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 3865 bytes
from contextlib import contextmanager
from hypothesis.errors import InvalidArgument
import hypothesis.internal.lazyformat as lazyformat
from hypothesis.internal.reflection import get_pretty_function_description
from hypothesis.strategies._internal.strategies import OneOfStrategy, SearchStrategy

class LimitReached(BaseException):
    pass


class LimitedStrategy(SearchStrategy):

    def __init__(self, strategy):
        super().__init__()
        self.base_strategy = strategy
        self.marker = 0
        self.currently_capped = False

    def __repr__(self):
        return 'LimitedStrategy(%r)' % (self.base_strategy,)

    def do_validate(self):
        self.base_strategy.validate()

    def do_draw(self, data):
        assert self.currently_capped
        if self.marker <= 0:
            raise LimitReached()
        self.marker -= 1
        return data.draw(self.base_strategy)

    @contextmanager
    def capped(self, max_templates):
        assert not self.currently_capped
        try:
            self.currently_capped = True
            self.marker = max_templates
            (yield)
        finally:
            self.currently_capped = False


class RecursiveStrategy(SearchStrategy):

    def __init__(self, base, extend, max_leaves):
        self.max_leaves = max_leaves
        self.base = base
        self.limited_base = LimitedStrategy(base)
        self.extend = extend
        strategies = [
         self.limited_base, self.extend(self.limited_base)]
        while 2 ** (len(strategies) - 1) <= max_leaves:
            strategies.append(extend(OneOfStrategy(tuple(strategies))))

        self.strategy = OneOfStrategy(strategies)

    def __repr__(self):
        if not hasattr(self, '_cached_repr'):
            self._cached_repr = 'recursive(%r, %s, max_leaves=%d)' % (
             self.base,
             get_pretty_function_description(self.extend),
             self.max_leaves)
        return self._cached_repr

    def do_validate(self):
        if not isinstance(self.base, SearchStrategy):
            raise InvalidArgument('Expected base to be SearchStrategy but got %r' % (self.base,))
        extended = self.extend(self.limited_base)
        if not isinstance(extended, SearchStrategy):
            raise InvalidArgument('Expected extend(%r) to be a SearchStrategy but got %r' % (
             self.limited_base, extended))
        self.limited_base.validate()
        self.extend(self.limited_base).validate()

    def do_draw--- This code section failed: ---

 L.  95         0  LOAD_CONST               0
                2  STORE_FAST               'count'

 L.  97         4  SETUP_FINALLY        58  'to 58'

 L.  98         6  LOAD_FAST                'self'
                8  LOAD_ATTR                limited_base
               10  LOAD_METHOD              capped
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                max_leaves
               16  CALL_METHOD_1         1  ''
               18  SETUP_WITH           48  'to 48'
               20  POP_TOP          

 L.  99        22  LOAD_FAST                'data'
               24  LOAD_METHOD              draw
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                strategy
               30  CALL_METHOD_1         1  ''
               32  POP_BLOCK        
               34  ROT_TWO          
               36  BEGIN_FINALLY    
               38  WITH_CLEANUP_START
               40  WITH_CLEANUP_FINISH
               42  POP_FINALLY           0  ''
               44  POP_BLOCK        
               46  RETURN_VALUE     
             48_0  COME_FROM_WITH       18  '18'
               48  WITH_CLEANUP_START
               50  WITH_CLEANUP_FINISH
               52  END_FINALLY      
               54  POP_BLOCK        
               56  JUMP_BACK             4  'to 4'
             58_0  COME_FROM_FINALLY     4  '4'

 L. 100        58  DUP_TOP          
               60  LOAD_GLOBAL              LimitReached
               62  COMPARE_OP               exception-match
               64  POP_JUMP_IF_FALSE   108  'to 108'
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L. 103        72  LOAD_FAST                'count'
               74  LOAD_CONST               0
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE    96  'to 96'

 L. 104        80  LOAD_FAST                'data'
               82  LOAD_METHOD              note_event

 L. 105        84  LOAD_GLOBAL              lazyformat

 L. 106        86  LOAD_STR                 'Draw for %r exceeded max_leaves and had to be retried'

 L. 107        88  LOAD_FAST                'self'

 L. 105        90  CALL_FUNCTION_2       2  ''

 L. 104        92  CALL_METHOD_1         1  ''
               94  POP_TOP          
             96_0  COME_FROM            78  '78'

 L. 110        96  LOAD_FAST                'count'
               98  LOAD_CONST               1
              100  INPLACE_ADD      
              102  STORE_FAST               'count'
              104  POP_EXCEPT       
              106  JUMP_BACK             4  'to 4'
            108_0  COME_FROM            64  '64'
              108  END_FINALLY      
              110  JUMP_BACK             4  'to 4'

Parse error at or near `ROT_TWO' instruction at offset 34