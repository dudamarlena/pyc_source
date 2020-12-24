# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\strategies\_internal\lazy.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 5219 bytes
from inspect import getfullargspec
from typing import Dict
from hypothesis.internal.reflection import arg_string, convert_keyword_arguments, convert_positional_arguments
from hypothesis.strategies._internal.strategies import SearchStrategy
unwrap_cache = {}
unwrap_depth = 0

def unwrap_strategies--- This code section failed: ---

 L.  33         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                's'
                4  LOAD_GLOBAL              SearchStrategy
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'

 L.  34        10  LOAD_FAST                's'
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L.  35        14  SETUP_FINALLY        26  'to 26'

 L.  36        16  LOAD_GLOBAL              unwrap_cache
               18  LOAD_FAST                's'
               20  BINARY_SUBSCR    
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY    14  '14'

 L.  37        26  DUP_TOP          
               28  LOAD_GLOBAL              KeyError
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    44  'to 44'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L.  38        40  POP_EXCEPT       
               42  JUMP_FORWARD         46  'to 46'
             44_0  COME_FROM            32  '32'
               44  END_FINALLY      
             46_0  COME_FROM            42  '42'

 L.  40        46  LOAD_FAST                's'
               48  LOAD_GLOBAL              unwrap_cache
               50  LOAD_FAST                's'
               52  STORE_SUBSCR     

 L.  42        54  SETUP_FINALLY       202  'to 202'

 L.  43        56  LOAD_GLOBAL              unwrap_depth
               58  LOAD_CONST               1
               60  INPLACE_ADD      
               62  STORE_GLOBAL             unwrap_depth

 L.  44        64  SETUP_FINALLY       170  'to 170'

 L.  45        66  LOAD_GLOBAL              unwrap_strategies
               68  LOAD_FAST                's'
               70  LOAD_ATTR                wrapped_strategy
               72  CALL_FUNCTION_1       1  ''
               74  STORE_FAST               'result'

 L.  46        76  LOAD_FAST                'result'
               78  LOAD_GLOBAL              unwrap_cache
               80  LOAD_FAST                's'
               82  STORE_SUBSCR     

 L.  47        84  SETUP_FINALLY       106  'to 106'

 L.  48        86  LOAD_FAST                'result'
               88  LOAD_ATTR                force_has_reusable_values
               90  LOAD_FAST                's'
               92  LOAD_ATTR                force_has_reusable_values
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_TRUE    102  'to 102'
               98  LOAD_ASSERT              AssertionError
              100  RAISE_VARARGS_1       1  'exception instance'
            102_0  COME_FROM            96  '96'
              102  POP_BLOCK        
              104  JUMP_FORWARD        126  'to 126'
            106_0  COME_FROM_FINALLY    84  '84'

 L.  49       106  DUP_TOP          
              108  LOAD_GLOBAL              AttributeError
              110  COMPARE_OP               exception-match
              112  POP_JUMP_IF_FALSE   124  'to 124'
              114  POP_TOP          
              116  POP_TOP          
              118  POP_TOP          

 L.  50       120  POP_EXCEPT       
              122  JUMP_FORWARD        126  'to 126'
            124_0  COME_FROM           112  '112'
              124  END_FINALLY      
            126_0  COME_FROM           122  '122'
            126_1  COME_FROM           104  '104'

 L.  52       126  SETUP_FINALLY       140  'to 140'

 L.  53       128  LOAD_FAST                's'
              130  LOAD_ATTR                force_has_reusable_values
              132  LOAD_FAST                'result'
              134  STORE_ATTR               force_has_reusable_values
              136  POP_BLOCK        
              138  JUMP_FORWARD        160  'to 160'
            140_0  COME_FROM_FINALLY   126  '126'

 L.  54       140  DUP_TOP          
              142  LOAD_GLOBAL              AttributeError
              144  COMPARE_OP               exception-match
              146  POP_JUMP_IF_FALSE   158  'to 158'
              148  POP_TOP          
              150  POP_TOP          
              152  POP_TOP          

 L.  55       154  POP_EXCEPT       
              156  JUMP_FORWARD        160  'to 160'
            158_0  COME_FROM           146  '146'
              158  END_FINALLY      
            160_0  COME_FROM           156  '156'
            160_1  COME_FROM           138  '138'

 L.  56       160  LOAD_FAST                'result'
              162  POP_BLOCK        
              164  POP_BLOCK        
              166  CALL_FINALLY        202  'to 202'
              168  RETURN_VALUE     
            170_0  COME_FROM_FINALLY    64  '64'

 L.  57       170  DUP_TOP          
              172  LOAD_GLOBAL              AttributeError
              174  COMPARE_OP               exception-match
              176  POP_JUMP_IF_FALSE   196  'to 196'
              178  POP_TOP          
              180  POP_TOP          
              182  POP_TOP          

 L.  58       184  LOAD_FAST                's'
              186  ROT_FOUR         
              188  POP_EXCEPT       
              190  POP_BLOCK        
              192  CALL_FINALLY        202  'to 202'
              194  RETURN_VALUE     
            196_0  COME_FROM           176  '176'
              196  END_FINALLY      
              198  POP_BLOCK        
              200  BEGIN_FINALLY    
            202_0  COME_FROM           192  '192'
            202_1  COME_FROM           166  '166'
            202_2  COME_FROM_FINALLY    54  '54'

 L.  60       202  LOAD_GLOBAL              unwrap_depth
              204  LOAD_CONST               1
              206  INPLACE_SUBTRACT 
              208  STORE_GLOBAL             unwrap_depth

 L.  61       210  LOAD_GLOBAL              unwrap_depth
              212  LOAD_CONST               0
              214  COMPARE_OP               <=
              216  POP_JUMP_IF_FALSE   226  'to 226'

 L.  62       218  LOAD_GLOBAL              unwrap_cache
              220  LOAD_METHOD              clear
              222  CALL_METHOD_0         0  ''
              224  POP_TOP          
            226_0  COME_FROM           216  '216'

 L.  63       226  LOAD_GLOBAL              unwrap_depth
              228  LOAD_CONST               0
              230  COMPARE_OP               >=
              232  POP_JUMP_IF_TRUE    238  'to 238'
              234  LOAD_ASSERT              AssertionError
              236  RAISE_VARARGS_1       1  'exception instance'
            238_0  COME_FROM           232  '232'
              238  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 36


class LazyStrategy(SearchStrategy):
    __doc__ = 'A strategy which is defined purely by conversion to and from another\n    strategy.\n\n    Its parameter and distribution come from that other strategy.\n    '

    def __init__(self, function, args, kwargs):
        SearchStrategy.__init__(self)
        self._LazyStrategy__wrapped_strategy = None
        self._LazyStrategy__representation = None
        self.function = function
        self._LazyStrategy__args = args
        self._LazyStrategy__kwargs = kwargs

    @property
    def supports_find(self):
        return self.wrapped_strategy.supports_find

    def calc_is_empty(self, recur):
        return recur(self.wrapped_strategy)

    def calc_has_reusable_values(self, recur):
        return recur(self.wrapped_strategy)

    def calc_is_cacheable(self, recur):
        for source in (
         self._LazyStrategy__args, self._LazyStrategy__kwargs.values):
            for v in source:
                if isinstancevSearchStrategy and not v.is_cacheable:
                    return False
            else:
                return True

    @property
    def wrapped_strategy(self):
        if self._LazyStrategy__wrapped_strategy is None:
            unwrapped_args = tuple((unwrap_strategies(s) for s in self._LazyStrategy__args))
            unwrapped_kwargs = {unwrap_strategies(v):k for k, v in self._LazyStrategy__kwargs.items}
            base = (self.function)(*self._LazyStrategy__args, **self._LazyStrategy__kwargs)
            if unwrapped_args == self._LazyStrategy__args and unwrapped_kwargs == self._LazyStrategy__kwargs:
                self._LazyStrategy__wrapped_strategy = base
            else:
                self._LazyStrategy__wrapped_strategy = (self.function)(*unwrapped_args, **unwrapped_kwargs)
        return self._LazyStrategy__wrapped_strategy

    def do_validate(self):
        w = self.wrapped_strategy
        assert isinstancewSearchStrategy, '%r returned non-strategy %r' % (self, w)
        w.validate

    def __repr__(self):
        if self._LazyStrategy__representation is None:
            _args = self._LazyStrategy__args
            _kwargs = self._LazyStrategy__kwargs
            argspec = getfullargspec(self.function)
            defaults = dict(argspec.kwonlydefaults or {})
            if argspec.defaults is not None:
                for name, value in zipreversed(argspec.args)reversed(argspec.defaults):
                    defaults[name] = value

            else:
                if len(argspec.args) > 1 or argspec.defaults:
                    _args, _kwargs = convert_positional_arguments(self.function, _args, _kwargs)
                else:
                    _args, _kwargs = convert_keyword_arguments(self.function, _args, _kwargs)
                kwargs_for_repr = dict(_kwargs)
                for k, v in defaults.items:
                    if k in kwargs_for_repr and kwargs_for_repr[k] is v:
                        del kwargs_for_repr[k]
                else:
                    self._LazyStrategy__representation = '%s(%s)' % (
                     self.function.__name__,
                     arg_string((self.function), _args, kwargs_for_repr, reorder=False))

        return self._LazyStrategy__representation

    def do_draw(self, data):
        return data.draw(self.wrapped_strategy)

    def do_filtered_draw(self, data, filter_strategy):
        return self.wrapped_strategy.do_filtered_draw(data=data,
          filter_strategy=filter_strategy)

    @property
    def label(self):
        return self.wrapped_strategy.label


# global unwrap_depth ## Warning: Unused global