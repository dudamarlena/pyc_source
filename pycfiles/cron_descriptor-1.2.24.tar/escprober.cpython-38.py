# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./vendor/chardet/escprober.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 3950 bytes
from .charsetprober import CharSetProber
from .codingstatemachine import CodingStateMachine
from .enums import LanguageFilter, ProbingState, MachineState
from .escsm import HZ_SM_MODEL, ISO2022CN_SM_MODEL, ISO2022JP_SM_MODEL, ISO2022KR_SM_MODEL

class EscCharSetProber(CharSetProber):
    """EscCharSetProber"""

    def __init__(self, lang_filter=None):
        super(EscCharSetProber, self).__init__(lang_filter=lang_filter)
        self.coding_sm = []
        if self.lang_filter & LanguageFilter.CHINESE_SIMPLIFIED:
            self.coding_sm.append(CodingStateMachine(HZ_SM_MODEL))
            self.coding_sm.append(CodingStateMachine(ISO2022CN_SM_MODEL))
        if self.lang_filter & LanguageFilter.JAPANESE:
            self.coding_sm.append(CodingStateMachine(ISO2022JP_SM_MODEL))
        if self.lang_filter & LanguageFilter.KOREAN:
            self.coding_sm.append(CodingStateMachine(ISO2022KR_SM_MODEL))
        self.active_sm_count = None
        self._detected_charset = None
        self._detected_language = None
        self._state = None
        self.reset()

    def reset(self):
        super(EscCharSetProber, self).reset()
        for coding_sm in self.coding_sm:
            if not coding_sm:
                pass
            else:
                coding_sm.active = True
                coding_sm.reset()

        self.active_sm_count = len(self.coding_sm)
        self._detected_charset = None
        self._detected_language = None

    @property
    def charset_name(self):
        return self._detected_charset

    @property
    def language(self):
        return self._detected_language

    def get_confidence(self):
        if self._detected_charset:
            return 0.99
        return 0.0

    def feed--- This code section failed: ---

 L.  84         0  LOAD_FAST                'byte_str'
                2  GET_ITER         
                4  FOR_ITER            158  'to 158'
                6  STORE_FAST               'c'

 L.  85         8  LOAD_FAST                'self'
               10  LOAD_ATTR                coding_sm
               12  GET_ITER         
             14_0  COME_FROM           112  '112'
             14_1  COME_FROM            20  '20'
               14  FOR_ITER            156  'to 156'
               16  STORE_FAST               'coding_sm'

 L.  86        18  LOAD_FAST                'coding_sm'
               20  POP_JUMP_IF_FALSE    14  'to 14'
               22  LOAD_FAST                'coding_sm'
               24  LOAD_ATTR                active
               26  POP_JUMP_IF_TRUE     30  'to 30'

 L.  87        28  JUMP_BACK            14  'to 14'
             30_0  COME_FROM            26  '26'

 L.  88        30  LOAD_FAST                'coding_sm'
               32  LOAD_METHOD              next_state
               34  LOAD_FAST                'c'
               36  CALL_METHOD_1         1  ''
               38  STORE_FAST               'coding_state'

 L.  89        40  LOAD_FAST                'coding_state'
               42  LOAD_GLOBAL              MachineState
               44  LOAD_ATTR                ERROR
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE   104  'to 104'

 L.  90        50  LOAD_CONST               False
               52  LOAD_FAST                'coding_sm'
               54  STORE_ATTR               active

 L.  91        56  LOAD_FAST                'self'
               58  DUP_TOP          
               60  LOAD_ATTR                active_sm_count
               62  LOAD_CONST               1
               64  INPLACE_SUBTRACT 
               66  ROT_TWO          
               68  STORE_ATTR               active_sm_count

 L.  92        70  LOAD_FAST                'self'
               72  LOAD_ATTR                active_sm_count
               74  LOAD_CONST               0
               76  COMPARE_OP               <=
               78  POP_JUMP_IF_FALSE   154  'to 154'

 L.  93        80  LOAD_GLOBAL              ProbingState
               82  LOAD_ATTR                NOT_ME
               84  LOAD_FAST                'self'
               86  STORE_ATTR               _state

 L.  94        88  LOAD_FAST                'self'
               90  LOAD_ATTR                state
               92  ROT_TWO          
               94  POP_TOP          
               96  ROT_TWO          
               98  POP_TOP          
              100  RETURN_VALUE     
              102  JUMP_BACK            14  'to 14'
            104_0  COME_FROM            48  '48'

 L.  95       104  LOAD_FAST                'coding_state'
              106  LOAD_GLOBAL              MachineState
              108  LOAD_ATTR                ITS_ME
              110  COMPARE_OP               ==
              112  POP_JUMP_IF_FALSE    14  'to 14'

 L.  96       114  LOAD_GLOBAL              ProbingState
              116  LOAD_ATTR                FOUND_IT
              118  LOAD_FAST                'self'
              120  STORE_ATTR               _state

 L.  97       122  LOAD_FAST                'coding_sm'
              124  LOAD_METHOD              get_coding_state_machine
              126  CALL_METHOD_0         0  ''
              128  LOAD_FAST                'self'
              130  STORE_ATTR               _detected_charset

 L.  98       132  LOAD_FAST                'coding_sm'
              134  LOAD_ATTR                language
              136  LOAD_FAST                'self'
              138  STORE_ATTR               _detected_language

 L.  99       140  LOAD_FAST                'self'
              142  LOAD_ATTR                state
              144  ROT_TWO          
              146  POP_TOP          
              148  ROT_TWO          
              150  POP_TOP          
              152  RETURN_VALUE     
            154_0  COME_FROM            78  '78'
              154  JUMP_BACK            14  'to 14'
              156  JUMP_BACK             4  'to 4'

 L. 101       158  LOAD_FAST                'self'
              160  LOAD_ATTR                state
              162  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_TWO' instruction at offset 96