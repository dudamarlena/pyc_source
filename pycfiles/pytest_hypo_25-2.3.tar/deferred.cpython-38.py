# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\strategies\_internal\deferred.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 3627 bytes
import inspect
from hypothesis.errors import InvalidArgument
from hypothesis.internal.reflection import get_pretty_function_description
from hypothesis.strategies._internal.strategies import SearchStrategy

class DeferredStrategy(SearchStrategy):
    __doc__ = 'A strategy which may be used before it is fully defined.'

    def __init__(self, definition):
        SearchStrategy.__init__(self)
        self._DeferredStrategy__wrapped_strategy = None
        self._DeferredStrategy__in_repr = False
        self._DeferredStrategy__definition = definition

    @property
    def wrapped_strategy(self):
        if self._DeferredStrategy__wrapped_strategy is None:
            if not inspect.isfunction(self._DeferredStrategy__definition):
                raise InvalidArgument('Excepted a definition to be a function but got %r of type %s instead.' % (
                 self._DeferredStrategy__definition, type(self._DeferredStrategy__definition).__name__))
            else:
                result = self._DeferredStrategy__definition()
                if result is self:
                    raise InvalidArgument('Cannot define a deferred strategy to be itself')
                assert isinstance(result, SearchStrategy), 'Expected definition to return a SearchStrategy but returned %r of type %s' % (
                 result, type(result).__name__)
            self._DeferredStrategy__wrapped_strategy = result
            del self._DeferredStrategy__definition
        return self._DeferredStrategy__wrapped_strategy

    @property
    def branches(self):
        return self.wrapped_strategy.branches

    @property
    def supports_find(self):
        return self.wrapped_strategy.supports_find

    def calc_label(self):
        """Deferred strategies don't have a calculated label, because we would
        end up having to calculate the fixed point of some hash function in
        order to calculate it when they recursively refer to themself!

        The label for the wrapped strategy will still appear because it
        will be passed to draw.
        """
        return self.class_label

    def calc_is_empty(self, recur):
        return recur(self.wrapped_strategy)

    def calc_has_reusable_values(self, recur):
        return recur(self.wrapped_strategy)

    def __repr__--- This code section failed: ---

 L.  86         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _DeferredStrategy__wrapped_strategy
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    62  'to 62'

 L.  87        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _DeferredStrategy__in_repr
               14  POP_JUMP_IF_FALSE    30  'to 30'

 L.  88        16  LOAD_STR                 '(deferred@%r)'
               18  LOAD_GLOBAL              id
               20  LOAD_FAST                'self'
               22  CALL_FUNCTION_1       1  ''
               24  BUILD_TUPLE_1         1 
               26  BINARY_MODULO    
               28  RETURN_VALUE     
             30_0  COME_FROM            14  '14'

 L.  89        30  SETUP_FINALLY        52  'to 52'

 L.  90        32  LOAD_CONST               True
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _DeferredStrategy__in_repr

 L.  91        38  LOAD_GLOBAL              repr
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                _DeferredStrategy__wrapped_strategy
               44  CALL_FUNCTION_1       1  ''
               46  POP_BLOCK        
               48  CALL_FINALLY         52  'to 52'
               50  RETURN_VALUE     
             52_0  COME_FROM            48  '48'
             52_1  COME_FROM_FINALLY    30  '30'

 L.  93        52  LOAD_CONST               False
               54  LOAD_FAST                'self'
               56  STORE_ATTR               _DeferredStrategy__in_repr
               58  END_FINALLY      
               60  JUMP_FORWARD         76  'to 76'
             62_0  COME_FROM             8  '8'

 L.  95        62  LOAD_STR                 'deferred(%s)'
               64  LOAD_GLOBAL              get_pretty_function_description
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                _DeferredStrategy__definition
               70  CALL_FUNCTION_1       1  ''
               72  BINARY_MODULO    
               74  RETURN_VALUE     
             76_0  COME_FROM            60  '60'

Parse error at or near `CALL_FINALLY' instruction at offset 48

    def do_draw(self, data):
        return data.draw(self.wrapped_strategy)