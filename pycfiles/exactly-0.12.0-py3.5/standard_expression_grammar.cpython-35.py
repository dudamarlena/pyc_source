# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/matcher/standard_expression_grammar.py
# Compiled at: 2020-01-31 11:01:50
# Size of source mod 2**32: 2806 bytes
from typing import Sequence, TypeVar
from exactly_lib.definitions import logic
from exactly_lib.symbol.logic.matcher import MatcherSdv
from exactly_lib.test_case_utils.expression import grammar
from exactly_lib.test_case_utils.expression.grammar_elements import OperatorExpressionDescriptionFromFunctions
from exactly_lib.test_case_utils.matcher.impls import combinator_sdvs, symbol_reference, parse_constant
from exactly_lib.type_system.value_type import ValueType
from exactly_lib.util.name import NameWithGenderWithFormatting
from exactly_lib.util.name_and_value import NameAndValue
from exactly_lib.util.textformat.textformat_parser import TextParser
MODEL = TypeVar('MODEL')

def new_grammar--- This code section failed: ---

 L.  21         0  LOAD_GLOBAL              TextParser

 L.  22         3  LOAD_STR                 'model'
                6  LOAD_FAST                'model'
                9  BUILD_MAP_1           1 
               12  CALL_FUNCTION_1       1  '1 positional, 0 named'
               15  STORE_FAST               'tp'

 L.  25        18  LOAD_GLOBAL              list
               21  LOAD_FAST                'simple_expressions'
               24  CALL_FUNCTION_1       1  '1 positional, 0 named'
               27  LOAD_GLOBAL              parse_constant
               30  LOAD_ATTR                CONSTANT_PRIMITIVE
               33  BUILD_LIST_1          1 
               36  BINARY_ADD       
               37  STORE_FAST               'all_simple_expressions'

 L.  27        40  LOAD_GLOBAL              str
               43  LOAD_GLOBAL              MatcherSdv
               46  LOAD_GLOBAL              MODEL
               49  BINARY_SUBSCR    
               50  LOAD_CONST               ('symbol_name', 'return')
               53  LOAD_CLOSURE             'value_type'
               56  BUILD_TUPLE_1         1 
               59  LOAD_CODE                <code_object mk_reference>
               62  LOAD_STR                 'new_grammar.<locals>.mk_reference'
               65  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
               71  STORE_FAST               'mk_reference'

 L.  30        74  LOAD_GLOBAL              grammar
               77  LOAD_ATTR                Grammar

 L.  31        80  LOAD_FAST                'concept'
               83  LOAD_STR                 'mk_reference'

 L.  32        86  LOAD_FAST                'mk_reference'
               89  LOAD_STR                 'simple_expressions'

 L.  33        92  LOAD_FAST                'all_simple_expressions'
               95  LOAD_STR                 'complex_expressions'

 L.  35        98  LOAD_GLOBAL              NameAndValue

 L.  36       101  LOAD_GLOBAL              logic
              104  LOAD_ATTR                AND_OPERATOR_NAME

 L.  37       107  LOAD_GLOBAL              grammar
              110  LOAD_ATTR                ComplexExpression
              113  LOAD_GLOBAL              combinator_sdvs
              116  LOAD_ATTR                Conjunction

 L.  38       119  LOAD_GLOBAL              OperatorExpressionDescriptionFromFunctions

 L.  39       122  LOAD_FAST                'tp'
              125  LOAD_ATTR                fnap__fun
              128  LOAD_GLOBAL              _AND_SED_DESCRIPTION
              131  CALL_FUNCTION_1       1  '1 positional, 0 named'
              134  CALL_FUNCTION_1       1  '1 positional, 0 named'
              137  CALL_FUNCTION_2       2  '2 positional, 0 named'
              140  CALL_FUNCTION_2       2  '2 positional, 0 named'

 L.  42       143  LOAD_GLOBAL              NameAndValue

 L.  43       146  LOAD_GLOBAL              logic
              149  LOAD_ATTR                OR_OPERATOR_NAME

 L.  44       152  LOAD_GLOBAL              grammar
              155  LOAD_ATTR                ComplexExpression
              158  LOAD_GLOBAL              combinator_sdvs
              161  LOAD_ATTR                Disjunction

 L.  45       164  LOAD_GLOBAL              OperatorExpressionDescriptionFromFunctions

 L.  46       167  LOAD_FAST                'tp'
              170  LOAD_ATTR                fnap__fun
              173  LOAD_GLOBAL              _OR_SED_DESCRIPTION
              176  CALL_FUNCTION_1       1  '1 positional, 0 named'
              179  CALL_FUNCTION_1       1  '1 positional, 0 named'
              182  CALL_FUNCTION_2       2  '2 positional, 0 named'
              185  CALL_FUNCTION_2       2  '2 positional, 0 named'
              188  BUILD_LIST_2          2 
              191  LOAD_STR                 'prefix_expressions'

 L.  51       194  LOAD_GLOBAL              NameAndValue

 L.  52       197  LOAD_GLOBAL              logic
              200  LOAD_ATTR                NOT_OPERATOR_NAME

 L.  53       203  LOAD_GLOBAL              grammar
              206  LOAD_ATTR                PrefixExpression
              209  LOAD_GLOBAL              combinator_sdvs
              212  LOAD_ATTR                Negation

 L.  54       215  LOAD_GLOBAL              OperatorExpressionDescriptionFromFunctions

 L.  55       218  LOAD_FAST                'tp'
              221  LOAD_ATTR                fnap__fun
              224  LOAD_GLOBAL              _NOT_SED_DESCRIPTION
              227  CALL_FUNCTION_1       1  '1 positional, 0 named'
              230  CALL_FUNCTION_1       1  '1 positional, 0 named'
              233  CALL_FUNCTION_2       2  '2 positional, 0 named'
              236  CALL_FUNCTION_2       2  '2 positional, 0 named'
              239  BUILD_LIST_1          1 
              242  CALL_FUNCTION_1025  1025  '1 positional, 4 named'
              245  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CODE' instruction at offset 59


_NOT_SED_DESCRIPTION = 'Matches {model:s} not matched by the given matcher.\n'
_AND_SED_DESCRIPTION = 'Matches {model:s} matched by every matcher.\n'
_OR_SED_DESCRIPTION = 'Matches {model:s} matched by any matcher.\n'