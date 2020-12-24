# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\strategies\_internal\featureflags.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 5383 bytes
import hypothesis.internal.conjecture.utils as cu
from hypothesis.strategies._internal.strategies import SearchStrategy
FEATURE_LABEL = cu.calc_label_from_name('feature flag')

class FeatureFlags:
    __doc__ = 'Object that can be used to control a number of feature flags for a\n    given test run.\n\n    This enables an approach to data generation called swarm testing (\n    see Groce, Alex, et al. "Swarm testing." Proceedings of the 2012\n    International Symposium on Software Testing and Analysis. ACM, 2012), in\n    which generation is biased by selectively turning some features off for\n    each test case generated. When there are many interacting features this can\n    find bugs that a pure generation strategy would otherwise have missed.\n\n    FeatureFlags are designed to "shrink open", so that during shrinking they\n    become less restrictive. This allows us to potentially shrink to smaller\n    test cases that were forbidden during the generation phase because they\n    required disabled features.\n    '

    def __init__(self, data=None, enabled=(), disabled=()):
        self._FeatureFlags__data = data
        self._FeatureFlags__decisions = {}
        for f in enabled:
            self._FeatureFlags__decisions[f] = 0
        else:
            for f in disabled:
                self._FeatureFlags__decisions[f] = 255
            else:
                if self._FeatureFlags__data is not None:
                    self._FeatureFlags__baseline = data.draw_bits(8)
                else:
                    self._FeatureFlags__baseline = 1

    def is_enabled--- This code section failed: ---

 L.  69         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _FeatureFlags__data
                4  LOAD_CONST               None
                6  COMPARE_OP               is
                8  POP_JUMP_IF_TRUE     18  'to 18'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _FeatureFlags__data
               14  LOAD_ATTR                frozen
               16  POP_JUMP_IF_FALSE    60  'to 60'
             18_0  COME_FROM             8  '8'

 L.  75        18  SETUP_FINALLY        38  'to 38'

 L.  76        20  LOAD_FAST                'self'
               22  LOAD_METHOD              _FeatureFlags__is_value_enabled
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                _FeatureFlags__decisions
               28  LOAD_FAST                'name'
               30  BINARY_SUBSCR    
               32  CALL_METHOD_1         1  ''
               34  POP_BLOCK        
               36  RETURN_VALUE     
             38_0  COME_FROM_FINALLY    18  '18'

 L.  77        38  DUP_TOP          
               40  LOAD_GLOBAL              KeyError
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE    58  'to 58'
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L.  78        52  POP_EXCEPT       
               54  LOAD_CONST               True
               56  RETURN_VALUE     
             58_0  COME_FROM            44  '44'
               58  END_FINALLY      
             60_0  COME_FROM            16  '16'

 L.  80        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _FeatureFlags__data
               64  STORE_FAST               'data'

 L.  82        66  LOAD_FAST                'data'
               68  LOAD_ATTR                start_example
               70  LOAD_GLOBAL              FEATURE_LABEL
               72  LOAD_CONST               ('label',)
               74  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               76  POP_TOP          

 L.  83        78  LOAD_FAST                'name'
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                _FeatureFlags__decisions
               84  COMPARE_OP               in
               86  POP_JUMP_IF_FALSE   114  'to 114'

 L.  91        88  LOAD_FAST                'self'
               90  LOAD_ATTR                _FeatureFlags__decisions
               92  LOAD_FAST                'name'
               94  BINARY_SUBSCR    
               96  STORE_FAST               'value'

 L.  92        98  LOAD_FAST                'data'
              100  LOAD_ATTR                draw_bits
              102  LOAD_CONST               8
              104  LOAD_FAST                'value'
              106  LOAD_CONST               ('forced',)
              108  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              110  POP_TOP          
              112  JUMP_FORWARD        164  'to 164'
            114_0  COME_FROM            86  '86'

 L.  97       114  LOAD_FAST                'self'
              116  LOAD_ATTR                _FeatureFlags__baseline
              118  LOAD_CONST               0
              120  COMPARE_OP               ==
              122  POP_JUMP_IF_FALSE   144  'to 144'

 L.  98       124  LOAD_CONST               0
              126  STORE_FAST               'value'

 L.  99       128  LOAD_FAST                'data'
              130  LOAD_ATTR                draw_bits
              132  LOAD_CONST               8
              134  LOAD_CONST               0
              136  LOAD_CONST               ('forced',)
              138  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              140  POP_TOP          
              142  JUMP_FORWARD        154  'to 154'
            144_0  COME_FROM           122  '122'

 L. 101       144  LOAD_FAST                'data'
              146  LOAD_METHOD              draw_bits
              148  LOAD_CONST               8
              150  CALL_METHOD_1         1  ''
              152  STORE_FAST               'value'
            154_0  COME_FROM           142  '142'

 L. 102       154  LOAD_FAST                'value'
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                _FeatureFlags__decisions
              160  LOAD_FAST                'name'
              162  STORE_SUBSCR     
            164_0  COME_FROM           112  '112'

 L. 103       164  LOAD_FAST                'data'
              166  LOAD_METHOD              stop_example
              168  CALL_METHOD_0         0  ''
              170  POP_TOP          

 L. 104       172  LOAD_FAST                'self'
              174  LOAD_METHOD              _FeatureFlags__is_value_enabled
              176  LOAD_FAST                'value'
              178  CALL_METHOD_1         1  ''
              180  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 48

    def __is_value_enabled(self, value):
        """Check if a given value drawn for a feature counts as enabled. Note
        that low values are more likely to be enabled. This is again in aid of
        shrinking open. In particular a value of 255 is always enabled."""
        return 255 - value >= self._FeatureFlags__baseline

    def __repr__(self):
        enabled = []
        disabled = []
        for k, v in self._FeatureFlags__decisions.items:
            if self._FeatureFlags__is_value_enabled(v):
                enabled.append(k)
            else:
                disabled.append(k)
        else:
            return 'FeatureFlags(enabled=%r, disabled=%r)' % (enabled, disabled)


class FeatureStrategy(SearchStrategy):

    def do_draw(self, data):
        return FeatureFlags(data)