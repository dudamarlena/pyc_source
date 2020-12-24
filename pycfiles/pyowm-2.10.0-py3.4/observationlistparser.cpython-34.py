# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/weatherapi25/parsers/observationlistparser.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 2702 bytes
"""
Module containing a concrete implementation for JSONParser abstract class,
returning lists of Observation objects
"""
import json
from pyowm.abstractions.jsonparser import JSONParser
from pyowm.weatherapi25.parsers.observationparser import ObservationParser
from pyowm.exceptions.parse_response_error import ParseResponseError
from pyowm.exceptions.api_response_error import APIResponseError

class ObservationListParser(JSONParser):
    __doc__ = '\n    Concrete *JSONParser* implementation building a list of *Observation*\n    instances out of raw JSON data coming from OWM Weather API responses.\n\n    '

    def parse_JSON--- This code section failed: ---

 L.  35         0  LOAD_FAST                'JSON_string'
                3  LOAD_CONST               None
                6  COMPARE_OP               is
                9  POP_JUMP_IF_FALSE    27  'to 27'

 L.  36        12  LOAD_GLOBAL              ParseResponseError
               15  LOAD_STR                 'JSON data is None'
               18  CALL_FUNCTION_1       1  '1 positional, 0 named'
               21  RAISE_VARARGS_1       1  'exception'
               24  JUMP_FORWARD         27  'to 27'
             27_0  COME_FROM            24  '24'

 L.  37        27  LOAD_GLOBAL              json
               30  LOAD_ATTR                loads
               33  LOAD_FAST                'JSON_string'
               36  CALL_FUNCTION_1       1  '1 positional, 0 named'
               39  STORE_FAST               'd'

 L.  38        42  LOAD_GLOBAL              ObservationParser
               45  CALL_FUNCTION_0       0  '0 positional, 0 named'
               48  STORE_DEREF              'observation_parser'

 L.  39        51  LOAD_STR                 'cod'
               54  LOAD_FAST                'd'
               57  COMPARE_OP               in
               60  POP_JUMP_IF_FALSE   198  'to 198'

 L.  44        63  LOAD_FAST                'd'
               66  LOAD_STR                 'cod'
               69  BINARY_SUBSCR    
               70  LOAD_STR                 '200'
               73  COMPARE_OP               ==
               76  POP_JUMP_IF_TRUE    195  'to 195'
               79  LOAD_FAST                'd'
               82  LOAD_STR                 'cod'
               85  BINARY_SUBSCR    
               86  LOAD_CONST               200
               89  COMPARE_OP               ==
             92_0  COME_FROM            76  '76'
               92  POP_JUMP_IF_FALSE    98  'to 98'

 L.  45        95  JUMP_ABSOLUTE       198  'to 198'
               98  ELSE                     '195'

 L.  47        98  LOAD_FAST                'd'
              101  LOAD_STR                 'cod'
              104  BINARY_SUBSCR    
              105  LOAD_STR                 '404'
              108  COMPARE_OP               ==
              111  POP_JUMP_IF_TRUE    130  'to 130'
              114  LOAD_FAST                'd'
              117  LOAD_STR                 'cod'
              120  BINARY_SUBSCR    
              121  LOAD_CONST               404
              124  COMPARE_OP               ==
            127_0  COME_FROM           111  '111'
              127  POP_JUMP_IF_FALSE   157  'to 157'

 L.  48       130  LOAD_GLOBAL              print
              133  LOAD_STR                 'OWM API: data not found - response payload: '
              136  LOAD_GLOBAL              json
              139  LOAD_ATTR                dumps
              142  LOAD_FAST                'd'
              145  CALL_FUNCTION_1       1  '1 positional, 0 named'
              148  BINARY_ADD       
              149  CALL_FUNCTION_1       1  '1 positional, 0 named'
              152  POP_TOP          

 L.  49       153  LOAD_CONST               None
              156  RETURN_END_IF    
            157_0  COME_FROM           127  '127'

 L.  51       157  LOAD_GLOBAL              APIResponseError
              160  LOAD_STR                 'OWM API: error - response payload: '
              163  LOAD_GLOBAL              json
              166  LOAD_ATTR                dumps
              169  LOAD_FAST                'd'
              172  CALL_FUNCTION_1       1  '1 positional, 0 named'
              175  BINARY_ADD       
              176  LOAD_GLOBAL              str
              179  LOAD_FAST                'd'
              182  LOAD_STR                 'cod'
              185  BINARY_SUBSCR    
              186  CALL_FUNCTION_1       1  '1 positional, 0 named'
              189  CALL_FUNCTION_2       2  '2 positional, 0 named'
              192  RAISE_VARARGS_1       1  'exception'
              195  JUMP_FORWARD        198  'to 198'
            198_0  COME_FROM           195  '195'

 L.  54       198  LOAD_STR                 'count'
              201  LOAD_FAST                'd'
              204  COMPARE_OP               in
              207  POP_JUMP_IF_FALSE   230  'to 230'
              210  LOAD_FAST                'd'
              213  LOAD_STR                 'count'
              216  BINARY_SUBSCR    
              217  LOAD_STR                 '0'
              220  COMPARE_OP               ==
            223_0  COME_FROM           207  '207'
              223  POP_JUMP_IF_FALSE   230  'to 230'

 L.  55       226  BUILD_LIST_0          0 
              229  RETURN_END_IF    
            230_0  COME_FROM           223  '223'

 L.  56       230  LOAD_STR                 'cnt'
              233  LOAD_FAST                'd'
              236  COMPARE_OP               in
              239  POP_JUMP_IF_FALSE   262  'to 262'
              242  LOAD_FAST                'd'
              245  LOAD_STR                 'cnt'
              248  BINARY_SUBSCR    
              249  LOAD_CONST               0
              252  COMPARE_OP               ==
            255_0  COME_FROM           239  '239'
              255  POP_JUMP_IF_FALSE   262  'to 262'

 L.  57       258  BUILD_LIST_0          0 
              261  RETURN_END_IF    
            262_0  COME_FROM           255  '255'

 L.  58       262  LOAD_STR                 'list'
              265  LOAD_FAST                'd'
              268  COMPARE_OP               in
              271  POP_JUMP_IF_FALSE   301  'to 301'

 L.  59       274  LOAD_CLOSURE             'observation_parser'
              277  BUILD_TUPLE_1         1 
              280  LOAD_LISTCOMP            '<code_object <listcomp>>'
              283  LOAD_STR                 'ObservationListParser.parse_JSON.<locals>.<listcomp>'
              286  MAKE_CLOSURE_0           '0 positional, 0 keyword only, 0 annotated'

 L.  60       289  LOAD_FAST                'd'
              292  LOAD_STR                 'list'
              295  BINARY_SUBSCR    
              296  GET_ITER         
              297  CALL_FUNCTION_1       1  '1 positional, 0 named'
              300  RETURN_END_IF    
            301_0  COME_FROM           271  '271'

 L.  63       301  LOAD_GLOBAL              ParseResponseError
              304  LOAD_STR                 ''
              307  LOAD_ATTR                join
              310  LOAD_GLOBAL              __name__

 L.  64       313  LOAD_STR                 ': impossible to read JSON data'
              316  BUILD_LIST_2          2 
              319  CALL_FUNCTION_1       1  '1 positional, 0 named'
              322  CALL_FUNCTION_1       1  '1 positional, 0 named'
              325  RAISE_VARARGS_1       1  'exception'

Parse error at or near `JUMP_FORWARD' instruction at offset 195

    def __repr__(self):
        return '<%s.%s>' % (__name__, self.__class__.__name__)