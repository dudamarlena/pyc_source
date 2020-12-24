# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\strategies\_internal\strategies.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 27908 bytes
import sys, warnings
from collections import defaultdict
from random import choice as random_choice
from typing import Any, Callable, Generic, List, TypeVar
import hypothesis.internal.conjecture.utils as cu
from hypothesis._settings import HealthCheck, Phase, Verbosity, settings
from hypothesis.control import _current_build_context, assume
from hypothesis.errors import HypothesisException, NonInteractiveExampleWarning, UnsatisfiedAssumption
from hypothesis.internal.conjecture.data import ConjectureData
from hypothesis.internal.conjecture.utils import calc_label_from_cls, calc_label_from_name, combine_labels
from hypothesis.internal.coverage import check_function
import hypothesis.internal.lazyformat as lazyformat
from hypothesis.internal.reflection import get_pretty_function_description
from hypothesis.internal.validation import check_type
from hypothesis.utils.conventions import UniqueIdentifier
Ex = TypeVar('Ex', covariant=True)
T = TypeVar('T')
calculating = UniqueIdentifier('calculating')
MAPPED_SEARCH_STRATEGY_DO_DRAW_LABEL = calc_label_from_name('another attempted draw in MappedSearchStrategy')

def one_of_strategies(xs):
    """Helper function for unioning multiple strategies."""
    xs = tuple(xs)
    if not xs:
        raise ValueError('Cannot join an empty list of strategies')
    return OneOfStrategy(xs)


def recursive_property(name, default):
    """Handle properties which may be mutually recursive among a set of
    strategies.

    These are essentially lazily cached properties, with the ability to set
    an override: If the property has not been explicitly set, we calculate
    it on first access and memoize the result for later.

    The problem is that for properties that depend on each other, a naive
    calculation strategy may hit infinite recursion. Consider for example
    the property is_empty. A strategy defined as x = st.deferred(lambda: x)
    is certainly empty (in order to draw a value from x we would have to
    draw a value from x, for which we would have to draw a value from x,
    ...), but in order to calculate it the naive approach would end up
    calling x.is_empty in order to calculate x.is_empty in order to etc.

    The solution is one of fixed point calculation. We start with a default
    value that is the value of the property in the absence of evidence to
    the contrary, and then update the values of the property for all
    dependent strategies until we reach a fixed point.

    The approach taken roughly follows that in section 4.2 of Adams,
    Michael D., Celeste Hollenbeck, and Matthew Might. "On the complexity
    and performance of parsing with derivatives." ACM SIGPLAN Notices 51.6
    (2016): 224-236.
    """
    cache_key = 'cached_' + name
    calculation = 'calc_' + name
    force_key = 'force_' + name

    def forced_value--- This code section failed: ---

 L.  91         0  SETUP_FINALLY        14  'to 14'

 L.  92         2  LOAD_GLOBAL              getattr
                4  LOAD_FAST                'target'
                6  LOAD_DEREF               'force_key'
                8  CALL_FUNCTION_2       2  ''
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L.  93        14  DUP_TOP          
               16  LOAD_GLOBAL              AttributeError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    42  'to 42'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.  94        28  LOAD_GLOBAL              getattr
               30  LOAD_FAST                'target'
               32  LOAD_DEREF               'cache_key'
               34  CALL_FUNCTION_2       2  ''
               36  ROT_FOUR         
               38  POP_EXCEPT       
               40  RETURN_VALUE     
             42_0  COME_FROM            20  '20'
               42  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 24

    def accept--- This code section failed: ---

 L.  97         0  SETUP_FINALLY        12  'to 12'

 L.  98         2  LOAD_DEREF               'forced_value'
                4  LOAD_FAST                'self'
                6  CALL_FUNCTION_1       1  ''
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L.  99        12  DUP_TOP          
               14  LOAD_GLOBAL              AttributeError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    30  'to 30'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 100        26  POP_EXCEPT       
               28  JUMP_FORWARD         32  'to 32'
             30_0  COME_FROM            18  '18'
               30  END_FINALLY      
             32_0  COME_FROM            28  '28'

 L. 102        32  BUILD_MAP_0           0 
               34  STORE_DEREF              'mapping'

 L. 103        36  LOAD_GLOBAL              object
               38  CALL_FUNCTION_0       0  ''
               40  STORE_DEREF              'sentinel'

 L. 104        42  LOAD_CONST               False
               44  BUILD_LIST_1          1 
               46  STORE_DEREF              'hit_recursion'

 L. 110        48  LOAD_CLOSURE             'calculation'
               50  LOAD_CLOSURE             'default'
               52  LOAD_CLOSURE             'forced_value'
               54  LOAD_CLOSURE             'hit_recursion'
               56  LOAD_CLOSURE             'mapping'
               58  LOAD_CLOSURE             'recur'
               60  LOAD_CLOSURE             'sentinel'
               62  BUILD_TUPLE_7         7 
               64  LOAD_CODE                <code_object recur>
               66  LOAD_STR                 'recursive_property.<locals>.accept.<locals>.recur'
               68  MAKE_FUNCTION_8          'closure'
               70  STORE_DEREF              'recur'

 L. 125        72  LOAD_DEREF               'recur'
               74  LOAD_FAST                'self'
               76  CALL_FUNCTION_1       1  ''
               78  POP_TOP          

 L. 133        80  LOAD_DEREF               'hit_recursion'
               82  LOAD_CONST               0
               84  BINARY_SUBSCR    
               86  POP_JUMP_IF_FALSE   106  'to 106'

 L. 134        88  LOAD_GLOBAL              set
               90  LOAD_DEREF               'mapping'
               92  CALL_FUNCTION_1       1  ''
               94  STORE_DEREF              'needs_update'

 L. 141        96  LOAD_GLOBAL              defaultdict
               98  LOAD_GLOBAL              set
              100  CALL_FUNCTION_1       1  ''
              102  STORE_DEREF              'listeners'
              104  JUMP_FORWARD        110  'to 110'
            106_0  COME_FROM            86  '86'

 L. 143       106  LOAD_CONST               None
              108  STORE_DEREF              'needs_update'
            110_0  COME_FROM           104  '104'

 L. 145       110  LOAD_CLOSURE             'default'
              112  LOAD_CLOSURE             'forced_value'
              114  LOAD_CLOSURE             'listeners'
              116  LOAD_CLOSURE             'mapping'
              118  LOAD_CLOSURE             'needs_update'
              120  LOAD_CLOSURE             'sentinel'
              122  BUILD_TUPLE_6         6 
              124  LOAD_CODE                <code_object recur2>
              126  LOAD_STR                 'recursive_property.<locals>.accept.<locals>.recur2'
              128  MAKE_FUNCTION_8          'closure'
              130  STORE_FAST               'recur2'

 L. 161       132  LOAD_CONST               0
              134  STORE_FAST               'count'

 L. 162       136  LOAD_GLOBAL              set
              138  CALL_FUNCTION_0       0  ''
              140  STORE_FAST               'seen'

 L. 163       142  LOAD_DEREF               'needs_update'
          144_146  POP_JUMP_IF_FALSE   280  'to 280'

 L. 164       148  LOAD_FAST                'count'
              150  LOAD_CONST               1
              152  INPLACE_ADD      
              154  STORE_FAST               'count'

 L. 176       156  LOAD_FAST                'count'
              158  LOAD_CONST               50
              160  COMPARE_OP               >
              162  POP_JUMP_IF_FALSE   206  'to 206'

 L. 177       164  LOAD_GLOBAL              frozenset
              166  LOAD_DEREF               'mapping'
              168  LOAD_METHOD              items
              170  CALL_METHOD_0         0  ''
              172  CALL_FUNCTION_1       1  ''
              174  STORE_FAST               'key'

 L. 178       176  LOAD_FAST                'key'
              178  LOAD_FAST                'seen'
              180  COMPARE_OP               not-in
              182  POP_JUMP_IF_TRUE    196  'to 196'
              184  LOAD_ASSERT              AssertionError
              186  LOAD_FAST                'key'
              188  LOAD_DEREF               'name'
              190  BUILD_TUPLE_2         2 
              192  CALL_FUNCTION_1       1  ''
              194  RAISE_VARARGS_1       1  'exception instance'
            196_0  COME_FROM           182  '182'

 L. 179       196  LOAD_FAST                'seen'
              198  LOAD_METHOD              add
              200  LOAD_FAST                'key'
              202  CALL_METHOD_1         1  ''
              204  POP_TOP          
            206_0  COME_FROM           162  '162'

 L. 180       206  LOAD_DEREF               'needs_update'
              208  STORE_FAST               'to_update'

 L. 181       210  LOAD_GLOBAL              set
              212  CALL_FUNCTION_0       0  ''
              214  STORE_DEREF              'needs_update'

 L. 182       216  LOAD_FAST                'to_update'
              218  GET_ITER         
            220_0  COME_FROM           252  '252'
              220  FOR_ITER            278  'to 278'
              222  STORE_FAST               'strat'

 L. 183       224  LOAD_GLOBAL              getattr
              226  LOAD_FAST                'strat'
              228  LOAD_DEREF               'calculation'
              230  CALL_FUNCTION_2       2  ''
              232  LOAD_FAST                'recur2'
              234  LOAD_FAST                'strat'
              236  CALL_FUNCTION_1       1  ''
              238  CALL_FUNCTION_1       1  ''
              240  STORE_FAST               'new_value'

 L. 184       242  LOAD_FAST                'new_value'
              244  LOAD_DEREF               'mapping'
              246  LOAD_FAST                'strat'
              248  BINARY_SUBSCR    
              250  COMPARE_OP               !=
              252  POP_JUMP_IF_FALSE   220  'to 220'

 L. 185       254  LOAD_DEREF               'needs_update'
              256  LOAD_METHOD              update
              258  LOAD_DEREF               'listeners'
              260  LOAD_FAST                'strat'
              262  BINARY_SUBSCR    
              264  CALL_METHOD_1         1  ''
              266  POP_TOP          

 L. 186       268  LOAD_FAST                'new_value'
              270  LOAD_DEREF               'mapping'
              272  LOAD_FAST                'strat'
              274  STORE_SUBSCR     
              276  JUMP_BACK           220  'to 220'
              278  JUMP_BACK           142  'to 142'
            280_0  COME_FROM           144  '144'

 L. 192       280  LOAD_DEREF               'mapping'
              282  LOAD_METHOD              items
              284  CALL_METHOD_0         0  ''
              286  GET_ITER         
              288  FOR_ITER            312  'to 312'
              290  UNPACK_SEQUENCE_2     2 
              292  STORE_FAST               'k'
              294  STORE_FAST               'v'

 L. 193       296  LOAD_GLOBAL              setattr
              298  LOAD_FAST                'k'
              300  LOAD_DEREF               'cache_key'
              302  LOAD_FAST                'v'
              304  CALL_FUNCTION_3       3  ''
              306  POP_TOP          
          308_310  JUMP_BACK           288  'to 288'

 L. 194       312  LOAD_GLOBAL              getattr
              314  LOAD_FAST                'self'
              316  LOAD_DEREF               'cache_key'
              318  CALL_FUNCTION_2       2  ''
              320  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 22

    accept.__name__ = name
    return property(accept)


class SearchStrategy(Generic[Ex]):
    __doc__ = 'A SearchStrategy is an object that knows how to explore data of a given\n    type.\n\n    Except where noted otherwise, methods on this class are not part of\n    the public API and their behaviour may change significantly between\n    minor version releases. They will generally be stable between patch\n    releases.\n    '
    supports_find = True
    validate_called = False
    _SearchStrategy__label = None

    def available(self, data):
        """Returns whether this strategy can *currently* draw any
        values. This typically useful for stateful testing where ``Bundle``
        grows over time a list of value to choose from.

        Unlike ``empty`` property, this method's return value may change
        over time.
        Note: ``data`` parameter will only be used for introspection and no
        value drawn from it.
        """
        return not self.is_empty

    is_empty = recursive_property'is_empty'True
    has_reusable_values = recursive_property'has_reusable_values'True
    is_cacheable = recursive_property'is_cacheable'True

    def calc_is_cacheable(self, recur):
        return True

    def calc_is_empty(self, recur):
        return False

    def calc_has_reusable_values(self, recur):
        return False

    def example(self) -> Ex:
        """Provide an example of the sort of value that this strategy
        generates. This is biased to be slightly simpler than is typical for
        values from this strategy, for clarity purposes.

        This method shouldn't be taken too seriously. It's here for interactive
        exploration of the API, not for any sort of real testing.

        This method is part of the public API.
        """
        if getattr(sys, 'ps1', None) is None:
            warnings.warn('The `.example()` method is good for exploring strategies, but should only be used interactively.  We recommend using `@given` for tests - it performs better, saves and replays failures to avoid flakiness, and reports minimal examples. (strategy: %r)' % (
             self,), NonInteractiveExampleWarning)
        else:
            context = _current_build_context.value
            if context is not None:
                if context.data is not None and context.data.depth > 0:
                    raise HypothesisException('Using example() inside a strategy definition is a bad idea. Instead consider using hypothesis.strategies.builds() or @hypothesis.strategies.composite to define your strategy. See https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.builds or https://hypothesis.readthedocs.io/en/latest/data.html#composite-strategies for more details.')
                else:
                    raise HypothesisException('Using example() inside a test function is a bad idea. Instead consider using hypothesis.strategies.data() to draw more examples during testing. See https://hypothesis.readthedocs.io/en/latest/data.html#drawing-interactively-in-tests for more details.')
        from hypothesis.core import given

        @given(self)
        @settings(database=None,
          max_examples=10,
          deadline=None,
          verbosity=(Verbosity.quiet),
          phases=(
         Phase.generate,),
          suppress_health_check=(HealthCheck.all))
        def example_generating_inner_function(ex):
            examples.appendex

        examples = []
        example_generating_inner_function
        return random_choice(examples)

    def map(self, pack: Callable[([Ex], T)]) -> 'SearchStrategy[T]':
        """Returns a new strategy that generates values by generating a value
        from this strategy and then calling pack() on the result, giving that.

        This method is part of the public API.
        """
        return MappedSearchStrategy(pack=pack, strategy=self)

    def flatmap(self, expand: Callable[([Ex], 'SearchStrategy[T]')]) -> 'SearchStrategy[T]':
        """Returns a new strategy that generates values by generating a value
        from this strategy, say x, then generating a value from
        strategy(expand(x))

        This method is part of the public API.
        """
        from hypothesis.strategies._internal.flatmapped import FlatMapStrategy
        return FlatMapStrategy(expand=expand, strategy=self)

    def filter(self, condition: Callable[([Ex], Any)]) -> 'SearchStrategy[Ex]':
        """Returns a new strategy that generates values from this strategy
        which satisfy the provided condition. Note that if the condition is too
        hard to satisfy this might result in your tests failing with
        Unsatisfiable.

        This method is part of the public API.
        """
        return FilteredStrategy(conditions=(condition,), strategy=self)

    def do_filtered_draw(self, data, filter_strategy):
        return filter_strategy.default_do_filtered_drawdata

    @property
    def branches(self) -> List['SearchStrategy[Ex]']:
        return [self]

    def __or__(self, other):
        """Return a strategy which produces values by randomly drawing from one
        of this strategy or the other strategy.

        This method is part of the public API.
        """
        if not isinstanceotherSearchStrategy:
            raise ValueError('Cannot | a SearchStrategy with %r' % (other,))
        return one_of_strategies((self, other))

    def validate(self) -> None:
        """Throw an exception if the strategy is not valid.

        This can happen due to lazy construction
        """
        if self.validate_called:
            return
        try:
            self.validate_called = True
            self.do_validate
            self.is_empty
            self.has_reusable_values
        except Exception:
            self.validate_called = False
            raise

    LABELS = {}

    @property
    def class_label--- This code section failed: ---

 L. 388         0  LOAD_FAST                'self'
                2  LOAD_ATTR                __class__
                4  STORE_FAST               'cls'

 L. 389         6  SETUP_FINALLY        20  'to 20'

 L. 390         8  LOAD_FAST                'cls'
               10  LOAD_ATTR                LABELS
               12  LOAD_FAST                'cls'
               14  BINARY_SUBSCR    
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     6  '6'

 L. 391        20  DUP_TOP          
               22  LOAD_GLOBAL              KeyError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    38  'to 38'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 392        34  POP_EXCEPT       
               36  JUMP_FORWARD         40  'to 40'
             38_0  COME_FROM            26  '26'
               38  END_FINALLY      
             40_0  COME_FROM            36  '36'

 L. 393        40  LOAD_GLOBAL              calc_label_from_cls
               42  LOAD_FAST                'cls'
               44  CALL_FUNCTION_1       1  ''
               46  STORE_FAST               'result'

 L. 394        48  LOAD_FAST                'result'
               50  LOAD_FAST                'cls'
               52  LOAD_ATTR                LABELS
               54  LOAD_FAST                'cls'
               56  STORE_SUBSCR     

 L. 395        58  LOAD_FAST                'result'
               60  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 30

    @property
    def label(self):
        if self._SearchStrategy__label is calculating:
            return 0
        if self._SearchStrategy__label is None:
            self._SearchStrategy__label = calculating
            self._SearchStrategy__label = self.calc_label
        return self._SearchStrategy__label

    def calc_label(self):
        return self.class_label

    def do_validate(self):
        pass

    def do_draw(self, data: ConjectureData) -> Ex:
        raise NotImplementedError('%s.do_draw' % (type(self).__name__,))

    def __init__(self):
        pass


def is_simple_data--- This code section failed: ---

 L. 420         0  SETUP_FINALLY        16  'to 16'

 L. 421         2  LOAD_GLOBAL              hash
                4  LOAD_FAST                'value'
                6  CALL_FUNCTION_1       1  ''
                8  POP_TOP          

 L. 422        10  POP_BLOCK        
               12  LOAD_CONST               True
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 423        16  DUP_TOP          
               18  LOAD_GLOBAL              TypeError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    36  'to 36'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 424        30  POP_EXCEPT       
               32  LOAD_CONST               False
               34  RETURN_VALUE     
             36_0  COME_FROM            22  '22'
               36  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 14


class SampledFromStrategy(SearchStrategy):
    __doc__ = 'A strategy which samples from a set of elements. This is essentially\n    equivalent to using a OneOfStrategy over Just strategies but may be more\n    efficient and convenient.\n\n    The conditional distribution chooses uniformly at random from some\n    non-empty subset of the elements.\n    '

    def __init__(self, elements):
        SearchStrategy.__init__self
        self.elements = cu.check_sample(elements, 'sampled_from')
        assert self.elements

    def __repr__(self):
        return 'sampled_from(%s)' % ', '.joinmapreprself.elements

    def calc_has_reusable_values(self, recur):
        return True

    def calc_is_cacheable(self, recur):
        return is_simple_data(self.elements)

    def do_draw(self, data):
        return cu.choice(data, self.elements)

    def do_filtered_draw(self, data, filter_strategy):
        known_bad_indices = set

        def check_index(i):
            if i in known_bad_indices:
                return False
            ok = filter_strategy.conditionself.elements[i]
            if not ok:
                if not known_bad_indices:
                    filter_strategy.note_retrieddata
                known_bad_indices.addi
            return ok

        for _ in range(3):
            i = cu.integer_range(data, 0, len(self.elements) - 1)
            if check_index(i):
                return self.elements[i]
        else:
            max_good_indices = len(self.elements) - len(known_bad_indices)
            if not max_good_indices:
                return filter_not_satisfied
            write_length = len(self.elements).bit_length
            cutoff = 10000
            max_good_indices = minmax_good_indicescutoff
            speculative_index = cu.integer_range(data, 0, max_good_indices - 1)
            allowed_indices = []

        for i in range(minlen(self.elements)cutoff):
            if check_index(i):
                allowed_indices.appendi
                if len(allowed_indices) > speculative_index:
                    data.draw_bits(write_length, forced=i)
                    return self.elements[i]
                if allowed_indices:
                    i = cu.choice(data, allowed_indices)
                    data.draw_bits(write_length, forced=i)
                    return self.elements[i]
            return filter_not_satisfied


class OneOfStrategy(SearchStrategy):
    __doc__ = 'Implements a union of strategies. Given a number of strategies this\n    generates values which could have come from any of them.\n\n    The conditional distribution draws uniformly at random from some\n    non-empty subset of these strategies and then draws from the\n    conditional distribution of that strategy.\n    '

    def __init__(self, strategies):
        SearchStrategy.__init__self
        strategies = tuple(strategies)
        self.original_strategies = list(strategies)
        self._OneOfStrategy__element_strategies = None
        self._OneOfStrategy__in_branches = False

    def calc_is_empty(self, recur):
        return all((recur(e) for e in self.original_strategies))

    def calc_has_reusable_values(self, recur):
        return all((recur(e) for e in self.original_strategies))

    def calc_is_cacheable(self, recur):
        return all((recur(e) for e in self.original_strategies))

    @property
    def element_strategies(self):
        if self._OneOfStrategy__element_strategies is None:
            strategies = []
            for arg in self.original_strategies:
                check_strategy(arg)
                if not arg.is_empty:
                    strategies.extend[s for s in arg.branches if not s.is_empty]
            else:
                pruned = []
                seen = set
                for s in strategies:
                    if s is self:
                        pass
                    elif s in seen:
                        pass
                    else:
                        seen.adds
                        pruned.appends
                else:
                    self._OneOfStrategy__element_strategies = pruned

        return self._OneOfStrategy__element_strategies

    def calc_label(self):
        return combine_labels(self.class_label, *[p.label for p in self.original_strategies])

    def do_draw(self, data: ConjectureData) -> Ex:
        strategy = data.drawSampledFromStrategy(self.element_strategies).filter(lambda s: s.availabledata)
        return data.drawstrategy

    def __repr__(self):
        return 'one_of(%s)' % ', '.joinmapreprself.original_strategies

    def do_validate(self):
        for e in self.element_strategies:
            e.validate

    @property
    def branches--- This code section failed: ---

 L. 589         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _OneOfStrategy__in_branches
                4  POP_JUMP_IF_TRUE     34  'to 34'

 L. 590         6  SETUP_FINALLY        24  'to 24'

 L. 591         8  LOAD_CONST               True
               10  LOAD_FAST                'self'
               12  STORE_ATTR               _OneOfStrategy__in_branches

 L. 592        14  LOAD_FAST                'self'
               16  LOAD_ATTR                element_strategies
               18  POP_BLOCK        
               20  CALL_FINALLY         24  'to 24'
               22  RETURN_VALUE     
             24_0  COME_FROM            20  '20'
             24_1  COME_FROM_FINALLY     6  '6'

 L. 594        24  LOAD_CONST               False
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _OneOfStrategy__in_branches
               30  END_FINALLY      
               32  JUMP_FORWARD         40  'to 40'
             34_0  COME_FROM             4  '4'

 L. 596        34  LOAD_FAST                'self'
               36  BUILD_LIST_1          1 
               38  RETURN_VALUE     
             40_0  COME_FROM            32  '32'

Parse error at or near `CALL_FINALLY' instruction at offset 20


class MappedSearchStrategy(SearchStrategy):
    __doc__ = 'A strategy which is defined purely by conversion to and from another\n    strategy.\n\n    Its parameter and distribution come from that other strategy.\n    '

    def __init__(self, strategy, pack=None):
        SearchStrategy.__init__self
        self.mapped_strategy = strategy
        if pack is not None:
            self.pack = pack

    def calc_is_empty(self, recur):
        return recur(self.mapped_strategy)

    def calc_is_cacheable(self, recur):
        return recur(self.mapped_strategy)

    def __repr__(self):
        if not hasattrself'_cached_repr':
            self._cached_repr = '%r.map(%s)' % (
             self.mapped_strategy,
             get_pretty_function_description(self.pack))
        return self._cached_repr

    def do_validate(self):
        self.mapped_strategy.validate

    def pack(self, x):
        """Take a value produced by the underlying mapped_strategy and turn it
        into a value suitable for outputting from this strategy."""
        raise NotImplementedError('%s.pack()' % self.__class__.__name__)

    def do_draw--- This code section failed: ---

 L. 635         0  LOAD_GLOBAL              range
                2  LOAD_CONST               3
                4  CALL_FUNCTION_1       1  ''
                6  GET_ITER         
                8  FOR_ITER            112  'to 112'
               10  STORE_FAST               '_'

 L. 636        12  LOAD_FAST                'data'
               14  LOAD_ATTR                index
               16  STORE_FAST               'i'

 L. 637        18  SETUP_FINALLY        66  'to 66'

 L. 638        20  LOAD_FAST                'data'
               22  LOAD_METHOD              start_example
               24  LOAD_GLOBAL              MAPPED_SEARCH_STRATEGY_DO_DRAW_LABEL
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          

 L. 639        30  LOAD_FAST                'self'
               32  LOAD_METHOD              pack
               34  LOAD_FAST                'data'
               36  LOAD_METHOD              draw
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                mapped_strategy
               42  CALL_METHOD_1         1  ''
               44  CALL_METHOD_1         1  ''
               46  STORE_FAST               'result'

 L. 640        48  LOAD_FAST                'data'
               50  LOAD_METHOD              stop_example
               52  CALL_METHOD_0         0  ''
               54  POP_TOP          

 L. 641        56  LOAD_FAST                'result'
               58  POP_BLOCK        
               60  ROT_TWO          
               62  POP_TOP          
               64  RETURN_VALUE     
             66_0  COME_FROM_FINALLY    18  '18'

 L. 642        66  DUP_TOP          
               68  LOAD_GLOBAL              UnsatisfiedAssumption
               70  COMPARE_OP               exception-match
               72  POP_JUMP_IF_FALSE   108  'to 108'
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          

 L. 643        80  LOAD_FAST                'data'
               82  LOAD_ATTR                stop_example
               84  LOAD_CONST               True
               86  LOAD_CONST               ('discard',)
               88  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               90  POP_TOP          

 L. 644        92  LOAD_FAST                'data'
               94  LOAD_ATTR                index
               96  LOAD_FAST                'i'
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE   104  'to 104'

 L. 645       102  RAISE_VARARGS_0       0  'reraise'
            104_0  COME_FROM           100  '100'
              104  POP_EXCEPT       
              106  JUMP_BACK             8  'to 8'
            108_0  COME_FROM            72  '72'
              108  END_FINALLY      
              110  JUMP_BACK             8  'to 8'

 L. 646       112  LOAD_GLOBAL              UnsatisfiedAssumption
              114  CALL_FUNCTION_0       0  ''
              116  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `ROT_TWO' instruction at offset 60

    @property
    def branches(self) -> List[SearchStrategy[Ex]]:
        return [MappedSearchStrategy(pack=(self.pack), strategy=strategy) for strategy in self.mapped_strategy.branches]


filter_not_satisfied = UniqueIdentifier('filter not satisfied')

class FilteredStrategy(SearchStrategy):

    def __init__(self, strategy, conditions):
        super.__init__
        if isinstancestrategyFilteredStrategy:
            self.flat_conditions = strategy.flat_conditions + conditions
            self.filtered_strategy = strategy.filtered_strategy
        else:
            self.flat_conditions = conditions
            self.filtered_strategy = strategy
        assert self.flat_conditions
        assert isinstanceself.flat_conditionstuple
        assert not isinstanceself.filtered_strategyFilteredStrategy
        self._FilteredStrategy__condition = None

    def calc_is_empty(self, recur):
        return recur(self.filtered_strategy)

    def calc_is_cacheable(self, recur):
        return recur(self.filtered_strategy)

    def __repr__(self):
        if not hasattrself'_cached_repr':
            self._cached_repr = '%r%s' % (
             self.filtered_strategy,
             ''.join('.filter(%s)' % get_pretty_function_description(cond) for cond in self.flat_conditions))
        return self._cached_repr

    def do_validate(self):
        self.filtered_strategy.validate

    @property
    def condition(self):
        if self._FilteredStrategy__condition is None:
            if not self.flat_conditions:
                raise AssertionError
            elif len(self.flat_conditions) == 1:
                self._FilteredStrategy__condition = self.flat_conditions[0]
            else:
                self._FilteredStrategy__condition = lambda x: all((cond(x) for cond in self.flat_conditions))
        return self._FilteredStrategy__condition

    def do_draw(self, data: ConjectureData) -> Ex:
        result = self.filtered_strategy.do_filtered_draw(data=data,
          filter_strategy=self)
        if result is not filter_not_satisfied:
            return result
        data.note_event('Aborted test because unable to satisfy %r' % (self,))
        data.mark_invalid
        raise AssertionError('Unreachable, for Mypy')

    def note_retried(self, data):
        data.note_eventlazyformat'Retried draw from %r to satisfy filter'self

    def default_do_filtered_draw(self, data):
        for i in range(3):
            start_index = data.index
            value = data.drawself.filtered_strategy
            if self.conditionvalue:
                return value
            if i == 0:
                self.note_retrieddata
            assume(data.index > start_index)
        else:
            return filter_not_satisfied

    @property
    def branches(self) -> List[SearchStrategy[Ex]]:
        return [FilteredStrategy(strategy=strategy, conditions=(self.flat_conditions)) for strategy in self.filtered_strategy.branches]


@check_function
def check_strategy(arg, name=''):
    check_type(SearchStrategy, arg, name)