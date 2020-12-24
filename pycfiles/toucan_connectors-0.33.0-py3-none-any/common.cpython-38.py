# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/common.py
# Compiled at: 2020-04-17 12:37:21
# Size of source mod 2**32: 6632 bytes
import ast, asyncio, re
from copy import deepcopy
import pyjq
from jinja2 import Environment, StrictUndefined, Template, meta
from pydantic import Field
from toucan_data_sdk.utils.helpers import slugify
RE_PARAM = '%\\(([^(%\\()]*)\\)s'
RE_JINJA = '{{([^({{)}]*)}}'
RE_PARAM_ALONE = '^' + RE_PARAM + '$'
RE_JINJA_ALONE = '^' + RE_JINJA + '$'
RE_JINJA_ALONE_IN_STRING = [
 RE_JINJA + '([ )])', RE_JINJA + '()$']
RE_SET_KEEP_TYPE = '{{__keep_type__\\1}}\\2'
RE_GET_KEEP_TYPE = '{{(__keep_type__[^({{)}]*)}}'

def nosql_apply_parameters_to_query(query, parameters):
    """
    WARNING : DO NOT USE THIS WITH VARIANTS OF SQL
    Instead use your client library parameter substitution method.
    https://www.owasp.org/index.php/Query_Parameterization_Cheat_Sheet
    """

    def _has_parameters(query):
        t = Environment().parse(query)
        return meta.find_undeclared_variables(t) or re.search(RE_PARAM, query)

    def _prepare_parameters--- This code section failed: ---

 L.  38         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'p'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L.  39        10  LOAD_GLOBAL              repr
               12  LOAD_FAST                'p'
               14  CALL_FUNCTION_1       1  ''
               16  RETURN_VALUE     
             18_0  COME_FROM             8  '8'

 L.  40        18  LOAD_GLOBAL              isinstance
               20  LOAD_FAST                'p'
               22  LOAD_GLOBAL              list
               24  CALL_FUNCTION_2       2  ''
               26  POP_JUMP_IF_FALSE    46  'to 46'

 L.  41        28  LOAD_CLOSURE             '_prepare_parameters'
               30  BUILD_TUPLE_1         1 
               32  LOAD_LISTCOMP            '<code_object <listcomp>>'
               34  LOAD_STR                 'nosql_apply_parameters_to_query.<locals>._prepare_parameters.<locals>.<listcomp>'
               36  MAKE_FUNCTION_8          'closure'
               38  LOAD_FAST                'p'
               40  GET_ITER         
               42  CALL_FUNCTION_1       1  ''
               44  RETURN_VALUE     
             46_0  COME_FROM            26  '26'

 L.  42        46  LOAD_GLOBAL              isinstance
               48  LOAD_FAST                'p'
               50  LOAD_GLOBAL              dict
               52  CALL_FUNCTION_2       2  ''
               54  POP_JUMP_IF_FALSE    78  'to 78'

 L.  43        56  LOAD_CLOSURE             '_prepare_parameters'
               58  BUILD_TUPLE_1         1 
               60  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               62  LOAD_STR                 'nosql_apply_parameters_to_query.<locals>._prepare_parameters.<locals>.<dictcomp>'
               64  MAKE_FUNCTION_8          'closure'
               66  LOAD_FAST                'p'
               68  LOAD_METHOD              items
               70  CALL_METHOD_0         0  ''
               72  GET_ITER         
               74  CALL_FUNCTION_1       1  ''
               76  RETURN_VALUE     
             78_0  COME_FROM            54  '54'

 L.  45        78  LOAD_FAST                'p'
               80  RETURN_VALUE     

Parse error at or near `LOAD_DICTCOMP' instruction at offset 60

    def _prepare_result--- This code section failed: ---

 L.  48         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'res'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L.  49        10  LOAD_GLOBAL              ast
               12  LOAD_METHOD              literal_eval
               14  LOAD_FAST                'res'
               16  CALL_METHOD_1         1  ''
               18  RETURN_VALUE     
             20_0  COME_FROM             8  '8'

 L.  50        20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'res'
               24  LOAD_GLOBAL              list
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_FALSE    48  'to 48'

 L.  51        30  LOAD_CLOSURE             '_prepare_result'
               32  BUILD_TUPLE_1         1 
               34  LOAD_LISTCOMP            '<code_object <listcomp>>'
               36  LOAD_STR                 'nosql_apply_parameters_to_query.<locals>._prepare_result.<locals>.<listcomp>'
               38  MAKE_FUNCTION_8          'closure'
               40  LOAD_FAST                'res'
               42  GET_ITER         
               44  CALL_FUNCTION_1       1  ''
               46  RETURN_VALUE     
             48_0  COME_FROM            28  '28'

 L.  52        48  LOAD_GLOBAL              isinstance
               50  LOAD_FAST                'res'
               52  LOAD_GLOBAL              dict
               54  CALL_FUNCTION_2       2  ''
               56  POP_JUMP_IF_FALSE    80  'to 80'

 L.  53        58  LOAD_CLOSURE             '_prepare_result'
               60  BUILD_TUPLE_1         1 
               62  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               64  LOAD_STR                 'nosql_apply_parameters_to_query.<locals>._prepare_result.<locals>.<dictcomp>'
               66  MAKE_FUNCTION_8          'closure'
               68  LOAD_FAST                'res'
               70  LOAD_METHOD              items
               72  CALL_METHOD_0         0  ''
               74  GET_ITER         
               76  CALL_FUNCTION_1       1  ''
               78  RETURN_VALUE     
             80_0  COME_FROM            56  '56'

 L.  55        80  LOAD_FAST                'res'
               82  RETURN_VALUE     

Parse error at or near `LOAD_DICTCOMP' instruction at offset 62

    def _render_query--- This code section failed: ---

 L.  62         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'query'
                4  LOAD_GLOBAL              dict
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    38  'to 38'

 L.  63        10  LOAD_CLOSURE             '_render_query'
               12  LOAD_CLOSURE             'parameters'
               14  BUILD_TUPLE_2         2 
               16  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               18  LOAD_STR                 'nosql_apply_parameters_to_query.<locals>._render_query.<locals>.<dictcomp>'
               20  MAKE_FUNCTION_8          'closure'
               22  LOAD_GLOBAL              deepcopy
               24  LOAD_FAST                'query'
               26  CALL_FUNCTION_1       1  ''
               28  LOAD_METHOD              items
               30  CALL_METHOD_0         0  ''
               32  GET_ITER         
               34  CALL_FUNCTION_1       1  ''
               36  RETURN_VALUE     
             38_0  COME_FROM             8  '8'

 L.  64        38  LOAD_GLOBAL              isinstance
               40  LOAD_FAST                'query'
               42  LOAD_GLOBAL              list
               44  CALL_FUNCTION_2       2  ''
               46  POP_JUMP_IF_FALSE    72  'to 72'

 L.  65        48  LOAD_CLOSURE             '_render_query'
               50  LOAD_CLOSURE             'parameters'
               52  BUILD_TUPLE_2         2 
               54  LOAD_LISTCOMP            '<code_object <listcomp>>'
               56  LOAD_STR                 'nosql_apply_parameters_to_query.<locals>._render_query.<locals>.<listcomp>'
               58  MAKE_FUNCTION_8          'closure'
               60  LOAD_GLOBAL              deepcopy
               62  LOAD_FAST                'query'
               64  CALL_FUNCTION_1       1  ''
               66  GET_ITER         
               68  CALL_FUNCTION_1       1  ''
               70  RETURN_VALUE     
             72_0  COME_FROM            46  '46'

 L.  66        72  LOAD_GLOBAL              type
               74  LOAD_FAST                'query'
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_GLOBAL              str
               80  COMPARE_OP               is
               82  POP_JUMP_IF_FALSE   226  'to 226'

 L.  67        84  LOAD_DEREF               '_has_parameters'
               86  LOAD_FAST                'query'
               88  CALL_FUNCTION_1       1  ''
               90  POP_JUMP_IF_TRUE     96  'to 96'

 L.  68        92  LOAD_FAST                'query'
               94  RETURN_VALUE     
             96_0  COME_FROM            90  '90'

 L.  69        96  LOAD_GLOBAL              deepcopy
               98  LOAD_DEREF               'parameters'
              100  CALL_FUNCTION_1       1  ''
              102  STORE_FAST               'clean_p'

 L.  71       104  LOAD_GLOBAL              re
              106  LOAD_METHOD              match
              108  LOAD_GLOBAL              RE_PARAM_ALONE
              110  LOAD_FAST                'query'
              112  CALL_METHOD_2         2  ''
              114  POP_JUMP_IF_TRUE    128  'to 128'
              116  LOAD_GLOBAL              re
              118  LOAD_METHOD              match
              120  LOAD_GLOBAL              RE_JINJA_ALONE
              122  LOAD_FAST                'query'
              124  CALL_METHOD_2         2  ''
              126  POP_JUMP_IF_FALSE   136  'to 136'
            128_0  COME_FROM           114  '114'

 L.  72       128  LOAD_DEREF               '_prepare_parameters'
              130  LOAD_FAST                'clean_p'
              132  CALL_FUNCTION_1       1  ''
              134  STORE_FAST               'clean_p'
            136_0  COME_FROM           126  '126'

 L.  75       136  LOAD_GLOBAL              Template
              138  LOAD_FAST                'query'
              140  CALL_FUNCTION_1       1  ''
              142  LOAD_METHOD              render
              144  LOAD_FAST                'clean_p'
              146  CALL_METHOD_1         1  ''
              148  LOAD_FAST                'clean_p'
              150  BINARY_MODULO    
              152  STORE_FAST               'res'

 L.  78       154  SETUP_FINALLY       196  'to 196'

 L.  79       156  LOAD_GLOBAL              ast
              158  LOAD_METHOD              literal_eval
              160  LOAD_FAST                'res'
              162  CALL_METHOD_1         1  ''
              164  STORE_FAST               'res'

 L.  80       166  LOAD_GLOBAL              isinstance
              168  LOAD_FAST                'res'
              170  LOAD_GLOBAL              str
              172  CALL_FUNCTION_2       2  ''
              174  POP_JUMP_IF_FALSE   182  'to 182'

 L.  81       176  LOAD_FAST                'res'
              178  POP_BLOCK        
              180  RETURN_VALUE     
            182_0  COME_FROM           174  '174'

 L.  83       182  LOAD_DEREF               '_prepare_result'
              184  LOAD_FAST                'res'
              186  CALL_FUNCTION_1       1  ''
              188  POP_BLOCK        
              190  RETURN_VALUE     
              192  POP_BLOCK        
              194  JUMP_ABSOLUTE       230  'to 230'
            196_0  COME_FROM_FINALLY   154  '154'

 L.  84       196  DUP_TOP          
              198  LOAD_GLOBAL              SyntaxError
              200  LOAD_GLOBAL              ValueError
              202  BUILD_TUPLE_2         2 
              204  COMPARE_OP               exception-match
              206  POP_JUMP_IF_FALSE   222  'to 222'
              208  POP_TOP          
              210  POP_TOP          
              212  POP_TOP          

 L.  85       214  LOAD_FAST                'res'
              216  ROT_FOUR         
              218  POP_EXCEPT       
              220  RETURN_VALUE     
            222_0  COME_FROM           206  '206'
              222  END_FINALLY      
              224  JUMP_FORWARD        230  'to 230'
            226_0  COME_FROM            82  '82'

 L.  87       226  LOAD_FAST                'query'
              228  RETURN_VALUE     
            230_0  COME_FROM           224  '224'

Parse error at or near `LOAD_DICTCOMP' instruction at offset 16

    def _handle_missing_params--- This code section failed: ---

 L.  95         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'elt'
                4  LOAD_GLOBAL              dict
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE   178  'to 178'

 L.  96        10  BUILD_MAP_0           0 
               12  STORE_FAST               'e'

 L.  97        14  LOAD_FAST                'elt'
               16  LOAD_METHOD              items
               18  CALL_METHOD_0         0  ''
               20  GET_ITER         
               22  FOR_ITER            174  'to 174'
               24  UNPACK_SEQUENCE_2     2 
               26  STORE_FAST               'k'
               28  STORE_FAST               'v'

 L.  98        30  LOAD_GLOBAL              isinstance
               32  LOAD_FAST                'v'
               34  LOAD_GLOBAL              str
               36  CALL_FUNCTION_2       2  ''
               38  POP_JUMP_IF_FALSE   158  'to 158'

 L.  99        40  LOAD_GLOBAL              re
               42  LOAD_METHOD              findall
               44  LOAD_GLOBAL              RE_PARAM
               46  LOAD_FAST                'v'
               48  CALL_METHOD_2         2  ''
               50  LOAD_GLOBAL              re
               52  LOAD_METHOD              findall
               54  LOAD_GLOBAL              RE_JINJA
               56  LOAD_FAST                'v'
               58  CALL_METHOD_2         2  ''
               60  BINARY_ADD       
               62  STORE_FAST               'matches'

 L. 100        64  BUILD_LIST_0          0 
               66  STORE_FAST               'missing_params'

 L. 101        68  LOAD_FAST                'matches'
               70  GET_ITER         
               72  FOR_ITER            136  'to 136'
               74  STORE_FAST               'm'

 L. 102        76  SETUP_FINALLY       104  'to 104'

 L. 103        78  LOAD_GLOBAL              Template
               80  LOAD_STR                 '{{ %s }}'
               82  LOAD_FAST                'm'
               84  BINARY_MODULO    
               86  LOAD_GLOBAL              StrictUndefined
               88  LOAD_CONST               ('undefined',)
               90  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               92  LOAD_METHOD              render
               94  LOAD_DEREF               'params'
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          
              100  POP_BLOCK        
              102  JUMP_BACK            72  'to 72'
            104_0  COME_FROM_FINALLY    76  '76'

 L. 104       104  DUP_TOP          
              106  LOAD_GLOBAL              Exception
              108  COMPARE_OP               exception-match
              110  POP_JUMP_IF_FALSE   132  'to 132'
              112  POP_TOP          
              114  POP_TOP          
              116  POP_TOP          

 L. 105       118  LOAD_FAST                'missing_params'
              120  LOAD_METHOD              append
              122  LOAD_FAST                'm'
              124  CALL_METHOD_1         1  ''
              126  POP_TOP          
              128  POP_EXCEPT       
              130  JUMP_BACK            72  'to 72'
            132_0  COME_FROM           110  '110'
              132  END_FINALLY      
              134  JUMP_BACK            72  'to 72'

 L. 106       136  LOAD_GLOBAL              any
              138  LOAD_FAST                'missing_params'
              140  CALL_FUNCTION_1       1  ''
              142  POP_JUMP_IF_FALSE   148  'to 148'

 L. 107       144  JUMP_BACK            22  'to 22'
              146  JUMP_ABSOLUTE       172  'to 172'
            148_0  COME_FROM           142  '142'

 L. 109       148  LOAD_FAST                'v'
              150  LOAD_FAST                'e'
              152  LOAD_FAST                'k'
              154  STORE_SUBSCR     
              156  JUMP_BACK            22  'to 22'
            158_0  COME_FROM            38  '38'

 L. 111       158  LOAD_DEREF               '_handle_missing_params'
              160  LOAD_FAST                'v'
              162  LOAD_DEREF               'params'
              164  CALL_FUNCTION_2       2  ''
              166  LOAD_FAST                'e'
              168  LOAD_FAST                'k'
              170  STORE_SUBSCR     
              172  JUMP_BACK            22  'to 22'

 L. 112       174  LOAD_FAST                'e'
              176  RETURN_VALUE     
            178_0  COME_FROM             8  '8'

 L. 113       178  LOAD_GLOBAL              isinstance
              180  LOAD_FAST                'elt'
              182  LOAD_GLOBAL              list
              184  CALL_FUNCTION_2       2  ''
              186  POP_JUMP_IF_FALSE   208  'to 208'

 L. 114       188  LOAD_CLOSURE             '_handle_missing_params'
              190  LOAD_CLOSURE             'params'
              192  BUILD_TUPLE_2         2 
              194  LOAD_LISTCOMP            '<code_object <listcomp>>'
              196  LOAD_STR                 'nosql_apply_parameters_to_query.<locals>._handle_missing_params.<locals>.<listcomp>'
              198  MAKE_FUNCTION_8          'closure'
              200  LOAD_FAST                'elt'
              202  GET_ITER         
              204  CALL_FUNCTION_1       1  ''
              206  RETURN_VALUE     
            208_0  COME_FROM           186  '186'

 L. 116       208  LOAD_FAST                'elt'
              210  RETURN_VALUE     

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 146

    query = _handle_missing_params(query, parameters)
    if parameters is None:
        return query
    query = _render_query(query, parameters)
    return query


def apply_query_parameters(query: str, parameters: dict) -> str:
    """
    Apply parameters to query

    Interpolate the query, which is a Jinja templates, with the provided parameters.
    """

    def _flatten_dict(p, parent_key=''):
        new_p = {}
        for k, v in deepcopy(p).items:
            new_key = f"{parent_key}_{k}" if parent_key else k
            new_p[new_key] = v
            if isinstance(v, list):
                v = {elt:idx for idx, elt in enumerate(v)}
            if isinstance(v, dict):
                new_p.update(_flatten_dict(v, new_key))
            elif isinstance(v, str):
                new_p.update({new_key: f'"{v}"'})
            else:
                new_p.update({new_key: v})
        else:
            return new_p

    if parameters is None:
        return query
    for pattern in RE_JINJA_ALONE_IN_STRING:
        query = re.sub(pattern, RE_SET_KEEP_TYPE, query)
    else:
        p_keep_type = re.findall(RE_GET_KEEP_TYPE, query)
        for key in p_keep_type:
            query = query.replace(key, slugify(key, separator='_'))
        else:
            if len(p_keep_type):
                p_keep_type = _flatten_dict(parameters, parent_key='__keep_type_')
                parameters.update(p_keep_type)
            return Template(query).render(parameters)


def transform_with_jq(data: object, jq_filter: str) -> list:
    data = pyjq.all(jq_filter, data)
    multiple_output = len(data) == 1 and isinstance(data[0], list)
    single_cols_dict = isinstance(data[0], dict) and isinstance(list(data[0].values)[0], list)
    if multiple_output or single_cols_dict:
        return data[0]
    return data


FilterSchema = Field('.',
  description='You can apply filters to json response if data is nested. As we rely on a library called jq, we suggest the refer to the dedicated <a href="https://stedolan.github.io/jq/manual/">documentation</a>')

def get_loop():
    """Sets up event loop"""
    try:
        loop = asyncio.get_event_loop
    except RuntimeError:
        loop = asyncio.new_event_loop
        asyncio.set_event_loop(loop)
    else:
        return loop