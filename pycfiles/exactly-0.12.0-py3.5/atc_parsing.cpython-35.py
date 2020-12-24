# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/execution/partial_execution/impl/atc_parsing.py
# Compiled at: 2019-12-27 10:07:31
# Size of source mod 2**32: 2062 bytes
from exactly_lib.execution import phase_step
from exactly_lib.execution.impl import phase_step_execution
from exactly_lib.execution.result import PhaseStepFailureException, ExecutionFailureStatus
from exactly_lib.section_document.model import SectionContents, ElementType
from exactly_lib.test_case.actor import Actor, ActionToCheck, ParseException
from exactly_lib.test_case.phases.act import ActPhaseInstruction
from exactly_lib.test_case.result.failure_details import FailureDetails

class ActionToCheckParser:

    def __init__(self, actor: Actor):
        self._actor = actor

    def parse--- This code section failed: ---

 L.  18         0  LOAD_GLOBAL              phase_step_execution
                3  LOAD_ATTR                PhaseStepFailureResultConstructor
                6  LOAD_GLOBAL              phase_step
                9  LOAD_ATTR                ACT__PARSE
               12  CALL_FUNCTION_1       1  '1 positional, 0 named'
               15  STORE_DEREF              'failure_con'

 L.  20        18  BUILD_LIST_0          0 
               21  STORE_DEREF              'instructions'

 L.  21        24  SETUP_LOOP          183  'to 183'
               27  LOAD_FAST                'act_phase'
               30  LOAD_ATTR                elements
               33  GET_ITER         
               34  FOR_ITER            182  'to 182'
               37  STORE_FAST               'element'

 L.  22        40  LOAD_FAST                'element'
               43  LOAD_ATTR                element_type
               46  LOAD_GLOBAL              ElementType
               49  LOAD_ATTR                INSTRUCTION
               52  COMPARE_OP               is
               55  POP_JUMP_IF_FALSE   139  'to 139'

 L.  23        58  LOAD_FAST                'element'
               61  LOAD_ATTR                instruction_info
               64  LOAD_ATTR                instruction
               67  STORE_FAST               'instruction'

 L.  24        70  LOAD_GLOBAL              isinstance
               73  LOAD_FAST                'instruction'
               76  LOAD_GLOBAL              ActPhaseInstruction
               79  CALL_FUNCTION_2       2  '2 positional, 0 named'
               82  UNARY_NOT        
               83  POP_JUMP_IF_FALSE   123  'to 123'

 L.  25        86  LOAD_STR                 'Instruction is not an instance of '
               89  LOAD_GLOBAL              str
               92  LOAD_GLOBAL              ActPhaseInstruction
               95  CALL_FUNCTION_1       1  '1 positional, 0 named'
               98  BINARY_ADD       
               99  STORE_FAST               'msg'

 L.  26       102  LOAD_GLOBAL              PhaseStepFailureException
              105  LOAD_DEREF               'failure_con'
              108  LOAD_ATTR                implementation_error_msg
              111  LOAD_FAST                'msg'
              114  CALL_FUNCTION_1       1  '1 positional, 0 named'
              117  CALL_FUNCTION_1       1  '1 positional, 0 named'
              120  RAISE_VARARGS_1       1  'exception'
            123_0  COME_FROM            83  '83'

 L.  27       123  LOAD_DEREF               'instructions'
              126  LOAD_ATTR                append
              129  LOAD_FAST                'instruction'
              132  CALL_FUNCTION_1       1  '1 positional, 0 named'
              135  POP_TOP          
              136  JUMP_FORWARD        179  'to 179'
              139  ELSE                     '179'

 L.  29       139  LOAD_STR                 'Act phase contains an element that is not an instruction: '
              142  LOAD_GLOBAL              str
              145  LOAD_FAST                'element'
              148  LOAD_ATTR                element_type
              151  CALL_FUNCTION_1       1  '1 positional, 0 named'
              154  BINARY_ADD       
              155  STORE_FAST               'msg'

 L.  30       158  LOAD_GLOBAL              PhaseStepFailureException
              161  LOAD_DEREF               'failure_con'
              164  LOAD_ATTR                implementation_error_msg
              167  LOAD_FAST                'msg'
              170  CALL_FUNCTION_1       1  '1 positional, 0 named'
              173  CALL_FUNCTION_1       1  '1 positional, 0 named'
              176  RAISE_VARARGS_1       1  'exception'
            179_0  COME_FROM           136  '136'
              179  JUMP_BACK            34  'to 34'
              182  POP_BLOCK        
            183_0  COME_FROM_LOOP       24  '24'

 L.  32       183  LOAD_FAST                'self'
              186  LOAD_ATTR                _actor
              189  STORE_DEREF              'actor'

 L.  34       192  LOAD_GLOBAL              ActionToCheck
              195  LOAD_CONST               ('return',)
              198  LOAD_CLOSURE             'actor'
              201  LOAD_CLOSURE             'failure_con'
              204  LOAD_CLOSURE             'instructions'
              207  BUILD_TUPLE_3         3 
              210  LOAD_CODE                <code_object parse_action>
              213  LOAD_STR                 'ActionToCheckParser.parse.<locals>.parse_action'
              216  MAKE_CLOSURE_A_2_0        '0 positional, 0 keyword only, 2 annotated'
              222  STORE_FAST               'parse_action'

 L.  41       225  LOAD_GLOBAL              phase_step_execution
              228  LOAD_ATTR                execute_action_and_catch_implementation_exception
              231  LOAD_FAST                'parse_action'
              234  LOAD_DEREF               'failure_con'
              237  CALL_FUNCTION_2       2  '2 positional, 0 named'
              240  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CODE' instruction at offset 210