# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\braces\token_transform.py
# Compiled at: 2020-04-26 20:18:59
# Size of source mod 2**32: 2794 bytes
from collections import namedtuple
from io import StringIO
import tokenize, black
from .const import EXCEPT, INDENT, NEWLINE, TOKEN
__all__ = ('test_compile', 'transform', 'SmallToken')
SmallToken = namedtuple('SmallToken', 'type string')

def test_compile(code: str) -> None:
    compile(code, '<test>', 'exec')


def transform--- This code section failed: ---

 L.  19         0  LOAD_GLOBAL              list
                2  LOAD_GLOBAL              tokenize
                4  LOAD_METHOD              generate_tokens
                6  LOAD_GLOBAL              StringIO
                8  LOAD_FAST                'code'
               10  CALL_FUNCTION_1       1  ''
               12  LOAD_ATTR                readline
               14  CALL_METHOD_1         1  ''
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'tokens'

 L.  21        20  LOAD_LISTCOMP            '<code_object <listcomp>>'
               22  LOAD_STR                 'transform.<locals>.<listcomp>'
               24  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               26  LOAD_FAST                'tokens'
               28  GET_ITER         
               30  CALL_FUNCTION_1       1  ''
               32  STORE_FAST               'result'

 L.  23        34  BUILD_LIST_0          0 
               36  STORE_FAST               'braces'

 L.  24        38  LOAD_CONST               False
               40  STORE_FAST               'in_dict_or_set'

 L.  25        42  LOAD_CONST               None
               44  STORE_FAST               'previous'

 L.  27        46  LOAD_FAST                'tokens'
               48  GET_ITER         
               50  FOR_ITER            134  'to 134'
               52  STORE_FAST               'token'

 L.  28        54  LOAD_FAST                'token'
               56  LOAD_ATTR                exact_type
               58  LOAD_GLOBAL              TOKEN
               60  LOAD_ATTR                LBRACE
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    96  'to 96'

 L.  29        66  LOAD_FAST                'previous'
               68  POP_JUMP_IF_FALSE    80  'to 80'
               70  LOAD_FAST                'previous'
               72  LOAD_ATTR                exact_type
               74  LOAD_GLOBAL              EXCEPT
               76  COMPARE_OP               in
               78  POP_JUMP_IF_FALSE    86  'to 86'
             80_0  COME_FROM            68  '68'

 L.  30        80  LOAD_CONST               True
               82  STORE_FAST               'in_dict_or_set'
               84  JUMP_FORWARD         96  'to 96'
             86_0  COME_FROM            78  '78'

 L.  32        86  LOAD_FAST                'braces'
               88  LOAD_METHOD              append
               90  LOAD_FAST                'token'
               92  CALL_METHOD_1         1  ''
               94  POP_TOP          
             96_0  COME_FROM            84  '84'
             96_1  COME_FROM            64  '64'

 L.  33        96  LOAD_FAST                'token'
               98  LOAD_ATTR                exact_type
              100  LOAD_GLOBAL              TOKEN
              102  LOAD_ATTR                RBRACE
              104  COMPARE_OP               ==
              106  POP_JUMP_IF_FALSE   128  'to 128'

 L.  34       108  LOAD_FAST                'in_dict_or_set'
              110  POP_JUMP_IF_FALSE   118  'to 118'

 L.  35       112  LOAD_CONST               False
              114  STORE_FAST               'in_dict_or_set'
              116  JUMP_FORWARD        128  'to 128'
            118_0  COME_FROM           110  '110'

 L.  37       118  LOAD_FAST                'braces'
              120  LOAD_METHOD              append
              122  LOAD_FAST                'token'
              124  CALL_METHOD_1         1  ''
              126  POP_TOP          
            128_0  COME_FROM           116  '116'
            128_1  COME_FROM           106  '106'

 L.  38       128  LOAD_FAST                'token'
              130  STORE_FAST               'previous'
              132  JUMP_BACK            50  'to 50'

 L.  40       134  BUILD_LIST_0          0 
              136  STORE_FAST               'contexts'

 L.  43       138  LOAD_FAST                'braces'
              140  GET_ITER         
              142  FOR_ITER            234  'to 234'
              144  STORE_FAST               'token'

 L.  44       146  LOAD_FAST                'token'
              148  LOAD_ATTR                exact_type
              150  LOAD_GLOBAL              TOKEN
              152  LOAD_ATTR                LBRACE
              154  COMPARE_OP               ==
              156  POP_JUMP_IF_FALSE   180  'to 180'

 L.  45       158  LOAD_FAST                'contexts'
              160  LOAD_METHOD              append
              162  LOAD_FAST                'tokens'
              164  LOAD_METHOD              index
              166  LOAD_FAST                'token'
              168  CALL_METHOD_1         1  ''
              170  LOAD_CONST               -1
              172  BUILD_LIST_2          2 
              174  CALL_METHOD_1         1  ''
              176  POP_TOP          
              178  JUMP_BACK           142  'to 142'
            180_0  COME_FROM           156  '156'

 L.  47       180  LOAD_GLOBAL              reversed
              182  LOAD_FAST                'contexts'
              184  CALL_FUNCTION_1       1  ''
              186  GET_ITER         
            188_0  COME_FROM           202  '202'
              188  FOR_ITER            224  'to 224'
              190  STORE_FAST               'context'

 L.  48       192  LOAD_FAST                'context'
              194  LOAD_CONST               1
              196  BINARY_SUBSCR    
              198  LOAD_CONST               -1
              200  COMPARE_OP               ==
              202  POP_JUMP_IF_FALSE   188  'to 188'

 L.  49       204  LOAD_FAST                'tokens'
              206  LOAD_METHOD              index
              208  LOAD_FAST                'token'
              210  CALL_METHOD_1         1  ''
              212  LOAD_FAST                'context'
              214  LOAD_CONST               1
              216  STORE_SUBSCR     

 L.  50       218  POP_TOP          
              220  CONTINUE            142  'to 142'
              222  JUMP_BACK           188  'to 188'

 L.  52       224  LOAD_GLOBAL              SyntaxError
              226  LOAD_STR                 'Unmatched braces found.'
              228  CALL_FUNCTION_1       1  ''
              230  RAISE_VARARGS_1       1  'exception instance'
              232  JUMP_BACK           142  'to 142'

 L.  54       234  LOAD_CONST               0
              236  STORE_FAST               'offset'

 L.  57       238  LOAD_GLOBAL              enumerate
              240  LOAD_FAST                'contexts'
              242  LOAD_CONST               1
              244  CALL_FUNCTION_2       2  ''
              246  GET_ITER         
              248  FOR_ITER            400  'to 400'
              250  UNPACK_SEQUENCE_2     2 
              252  STORE_FAST               'indent'
              254  UNPACK_SEQUENCE_2     2 
              256  STORE_FAST               'start'
              258  STORE_FAST               'end'

 L.  60       260  LOAD_GLOBAL              SmallToken
              262  LOAD_GLOBAL              TOKEN
              264  LOAD_ATTR                COLON
              266  LOAD_STR                 ':'
              268  CALL_FUNCTION_2       2  ''
              270  LOAD_FAST                'result'
              272  LOAD_FAST                'start'
              274  LOAD_FAST                'offset'
              276  BINARY_ADD       
              278  STORE_SUBSCR     

 L.  63       280  LOAD_FAST                'offset'
              282  LOAD_CONST               1
              284  INPLACE_ADD      
              286  STORE_FAST               'offset'

 L.  64       288  LOAD_FAST                'result'
              290  LOAD_FAST                'start'
              292  LOAD_FAST                'offset'
              294  BINARY_ADD       
              296  BINARY_SUBSCR    
              298  LOAD_ATTR                type
              300  LOAD_GLOBAL              NEWLINE
              302  COMPARE_OP               in
          304_306  POP_JUMP_IF_FALSE   318  'to 318'

 L.  65       308  LOAD_FAST                'offset'
              310  LOAD_CONST               1
              312  INPLACE_SUBTRACT 
              314  STORE_FAST               'offset'
              316  JUMP_FORWARD        342  'to 342'
            318_0  COME_FROM           304  '304'

 L.  67       318  LOAD_FAST                'result'
              320  LOAD_METHOD              insert
              322  LOAD_FAST                'start'
              324  LOAD_FAST                'offset'
              326  BINARY_ADD       
              328  LOAD_GLOBAL              SmallToken
              330  LOAD_GLOBAL              TOKEN
              332  LOAD_ATTR                NL
              334  LOAD_STR                 '\n'
              336  CALL_FUNCTION_2       2  ''
              338  CALL_METHOD_2         2  ''
              340  POP_TOP          
            342_0  COME_FROM           316  '316'

 L.  70       342  LOAD_GLOBAL              SmallToken
              344  LOAD_GLOBAL              TOKEN
              346  LOAD_ATTR                DEDENT
              348  LOAD_STR                 ''
              350  CALL_FUNCTION_2       2  ''
              352  LOAD_FAST                'result'
              354  LOAD_FAST                'end'
              356  LOAD_FAST                'offset'
              358  BINARY_ADD       
              360  STORE_SUBSCR     

 L.  73       362  LOAD_FAST                'offset'
              364  LOAD_CONST               1
              366  INPLACE_ADD      
              368  STORE_FAST               'offset'

 L.  74       370  LOAD_FAST                'result'
              372  LOAD_METHOD              insert
              374  LOAD_FAST                'start'
              376  LOAD_FAST                'offset'
              378  BINARY_ADD       
              380  LOAD_GLOBAL              SmallToken
              382  LOAD_GLOBAL              TOKEN
              384  LOAD_ATTR                INDENT
              386  LOAD_GLOBAL              INDENT
              388  LOAD_FAST                'indent'
              390  BINARY_MULTIPLY  
              392  CALL_FUNCTION_2       2  ''
              394  CALL_METHOD_2         2  ''
              396  POP_TOP          
              398  JUMP_BACK           248  'to 248'

 L.  76       400  LOAD_CONST               0
              402  STORE_FAST               'offset'

 L.  78       404  LOAD_GLOBAL              enumerate
              406  LOAD_FAST                'result'
              408  LOAD_METHOD              copy
              410  CALL_METHOD_0         0  ''
              412  CALL_FUNCTION_1       1  ''
              414  GET_ITER         
            416_0  COME_FROM           432  '432'
              416  FOR_ITER            508  'to 508'
              418  UNPACK_SEQUENCE_2     2 
              420  STORE_FAST               'index'
              422  STORE_FAST               'small_token'

 L.  80       424  LOAD_FAST                'small_token'
              426  LOAD_ATTR                string
              428  LOAD_STR                 ';'
              430  COMPARE_OP               ==
          432_434  POP_JUMP_IF_FALSE   416  'to 416'

 L.  81       436  LOAD_FAST                'result'
              438  LOAD_FAST                'index'
              440  LOAD_FAST                'offset'
              442  BINARY_SUBTRACT  
              444  LOAD_CONST               1
              446  BINARY_ADD       
              448  BINARY_SUBSCR    
              450  LOAD_ATTR                type
              452  LOAD_GLOBAL              NEWLINE
              454  COMPARE_OP               in
          456_458  POP_JUMP_IF_FALSE   484  'to 484'

 L.  82       460  LOAD_FAST                'result'
              462  LOAD_METHOD              pop
              464  LOAD_FAST                'index'
              466  LOAD_FAST                'offset'
              468  BINARY_SUBTRACT  
              470  CALL_METHOD_1         1  ''
              472  POP_TOP          

 L.  83       474  LOAD_FAST                'offset'
              476  LOAD_CONST               1
              478  INPLACE_ADD      
              480  STORE_FAST               'offset'
              482  JUMP_BACK           416  'to 416'
            484_0  COME_FROM           456  '456'

 L.  85       484  LOAD_GLOBAL              SmallToken
              486  LOAD_GLOBAL              TOKEN
              488  LOAD_ATTR                NL
              490  LOAD_STR                 '\n'
              492  CALL_FUNCTION_2       2  ''
              494  LOAD_FAST                'result'
              496  LOAD_FAST                'index'
              498  LOAD_FAST                'offset'
              500  BINARY_SUBTRACT  
              502  STORE_SUBSCR     
          504_506  JUMP_BACK           416  'to 416'

 L.  87       508  LOAD_GLOBAL              tokenize
              510  LOAD_METHOD              untokenize
              512  LOAD_FAST                'result'
              514  CALL_METHOD_1         1  ''
              516  STORE_FAST               'final'

 L.  89       518  LOAD_STR                 '\n\n'
              520  LOAD_GLOBAL              black
              522  LOAD_ATTR                format_str
              524  LOAD_FAST                'final'
              526  LOAD_GLOBAL              black
              528  LOAD_ATTR                FileMode
              530  LOAD_CONST               100
              532  LOAD_CONST               ('line_length',)
              534  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              536  LOAD_CONST               ('mode',)
              538  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              540  BINARY_ADD       
              542  STORE_FAST               'final'

 L.  91       544  LOAD_FAST                'final'
              546  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CONTINUE' instruction at offset 220