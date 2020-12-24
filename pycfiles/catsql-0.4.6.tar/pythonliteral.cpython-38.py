# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__QTYPES__/pythonliteral/pythonliteral.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 1350 bytes
import ast
tutor.qtype_inherit('pythonic')
base, _ = tutor.question('pythonic')

def handle_submission--- This code section failed: ---

 L.  24         0  LOAD_FAST                'submissions'
                2  LOAD_FAST                'info'
                4  LOAD_STR                 'csq_name'
                6  BINARY_SUBSCR    
                8  BINARY_SUBSCR    
               10  LOAD_METHOD              strip
               12  CALL_METHOD_0         0  ''
               14  STORE_FAST               'sub'

 L.  26        16  LOAD_FAST                'info'
               18  LOAD_STR                 'csq_input_check'
               20  BINARY_SUBSCR    
               22  LOAD_FAST                'sub'
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'inp'

 L.  27        28  LOAD_FAST                'inp'
               30  LOAD_CONST               None
               32  COMPARE_OP               is-not
               34  POP_JUMP_IF_FALSE    50  'to 50'

 L.  28        36  LOAD_CONST               0.0
               38  LOAD_STR                 '<font color="red">%s</font>'
               40  LOAD_FAST                'inp'
               42  BINARY_MODULO    
               44  LOAD_CONST               ('score', 'msg')
               46  BUILD_CONST_KEY_MAP_2     2 
               48  RETURN_VALUE     
             50_0  COME_FROM            34  '34'

 L.  30        50  SETUP_FINALLY       100  'to 100'

 L.  31        52  LOAD_GLOBAL              ast
               54  LOAD_METHOD              parse
               56  LOAD_FAST                'sub'
               58  CALL_METHOD_1         1  ''
               60  LOAD_ATTR                body
               62  LOAD_CONST               0
               64  BINARY_SUBSCR    
               66  LOAD_ATTR                value
               68  STORE_FAST               'x'

 L.  32        70  LOAD_GLOBAL              isinstance
               72  LOAD_FAST                'x'
               74  LOAD_GLOBAL              ast
               76  LOAD_ATTR                BinOp
               78  CALL_FUNCTION_2       2  ''
               80  POP_JUMP_IF_FALSE    86  'to 86'
               82  LOAD_GLOBAL              AssertionError
               84  RAISE_VARARGS_1       1  ''
             86_0  COME_FROM            80  '80'

 L.  33        86  LOAD_GLOBAL              ast
               88  LOAD_METHOD              literal_eval
               90  LOAD_FAST                'x'
               92  CALL_METHOD_1         1  ''
               94  POP_TOP          
               96  POP_BLOCK        
               98  JUMP_FORWARD        122  'to 122'
            100_0  COME_FROM_FINALLY    50  '50'

 L.  34       100  POP_TOP          
              102  POP_TOP          
              104  POP_TOP          

 L.  35       106  LOAD_CONST               0.0
              108  LOAD_STR                 'Value must be a valid Python literal.'
              110  LOAD_CONST               ('score', 'msg')
              112  BUILD_CONST_KEY_MAP_2     2 
              114  ROT_FOUR         
              116  POP_EXCEPT       
              118  RETURN_VALUE     
              120  END_FINALLY      
            122_0  COME_FROM            98  '98'

 L.  37       122  LOAD_GLOBAL              base
              124  LOAD_STR                 'handle_submission'
              126  BINARY_SUBSCR    
              128  LOAD_FAST                'submissions'
              130  BUILD_TUPLE_1         1 
              132  LOAD_FAST                'info'
              134  CALL_FUNCTION_EX_KW     1  'keyword args'
              136  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_FOUR' instruction at offset 114