# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/r/repo/aibolit/patterns/classic_setter/classic_setter.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 1422 bytes
from typing import List
import javalang
from aibolit.types_decl import LineNumber
from aibolit.utils.ast import AST

class ClassicSetter:

    def __init__(self):
        pass

    def value--- This code section failed: ---

 L.  15         0  BUILD_LIST_0          0 
                2  STORE_FAST               'lst'

 L.  16         4  LOAD_GLOBAL              AST
                6  LOAD_FAST                'filename'
                8  CALL_FUNCTION_1       1  ''
               10  LOAD_ATTR                value
               12  CALL_FUNCTION_0       0  ''
               14  LOAD_ATTR                filter
               16  LOAD_GLOBAL              javalang
               18  LOAD_ATTR                tree
               20  LOAD_ATTR                MethodDeclaration
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'tree'

 L.  17        26  SETUP_LOOP          238  'to 238'
               28  LOAD_FAST                'tree'
               30  GET_ITER         
               32  FOR_ITER            236  'to 236'
               34  UNPACK_SEQUENCE_2     2 
               36  STORE_FAST               'path'
               38  STORE_FAST               'node'

 L.  18        40  LOAD_FAST                'node'
               42  LOAD_ATTR                return_type
               44  LOAD_CONST               None
               46  COMPARE_OP               is
               48  POP_JUMP_IF_FALSE    32  'to 32'
               50  LOAD_STR                 'set'
               52  LOAD_FAST                'node'
               54  LOAD_ATTR                name
               56  LOAD_CONST               None
               58  LOAD_CONST               3
               60  BUILD_SLICE_2         2 
               62  BINARY_SUBSCR    
               64  COMPARE_OP               in
               66  POP_JUMP_IF_FALSE    32  'to 32'

 L.  19        68  LOAD_GLOBAL              isinstance
               70  LOAD_FAST                'node'
               72  LOAD_ATTR                body
               74  LOAD_GLOBAL              list
               76  CALL_FUNCTION_2       2  ''
               78  POP_JUMP_IF_FALSE    32  'to 32'
               80  LOAD_GLOBAL              len
               82  LOAD_FAST                'node'
               84  LOAD_ATTR                body
               86  CALL_FUNCTION_1       1  ''
               88  LOAD_CONST               2
               90  COMPARE_OP               <
               92  POP_JUMP_IF_FALSE    32  'to 32'

 L.  20        94  SETUP_LOOP          234  'to 234'
               96  LOAD_FAST                'node'
               98  LOAD_ATTR                body
              100  GET_ITER         
              102  FOR_ITER            232  'to 232'
              104  STORE_FAST               'statement'

 L.  21       106  LOAD_GLOBAL              isinstance
              108  LOAD_FAST                'statement'
              110  LOAD_GLOBAL              javalang
              112  LOAD_ATTR                tree
              114  LOAD_ATTR                StatementExpression
              116  CALL_FUNCTION_2       2  ''
              118  POP_JUMP_IF_FALSE   102  'to 102'

 L.  22       120  LOAD_GLOBAL              isinstance
              122  LOAD_FAST                'statement'
              124  LOAD_ATTR                expression
              126  LOAD_GLOBAL              javalang
              128  LOAD_ATTR                tree
              130  LOAD_ATTR                Assignment
              132  CALL_FUNCTION_2       2  ''
              134  POP_JUMP_IF_FALSE   228  'to 228'

 L.  23       136  LOAD_FAST                'statement'
              138  LOAD_ATTR                expression
              140  LOAD_ATTR                expressionl
              142  STORE_FAST               'expression'

 L.  24       144  LOAD_GLOBAL              isinstance
              146  LOAD_FAST                'expression'
              148  LOAD_GLOBAL              javalang
              150  LOAD_ATTR                tree
              152  LOAD_ATTR                This
              154  CALL_FUNCTION_2       2  ''
              156  POP_JUMP_IF_FALSE   224  'to 224'

 L.  25       158  LOAD_FAST                'statement'
              160  LOAD_ATTR                expression
              162  LOAD_ATTR                type
              164  LOAD_STR                 '='
              166  COMPARE_OP               ==
              168  POP_JUMP_IF_FALSE   220  'to 220'

 L.  26       170  LOAD_FAST                'expression'
              172  LOAD_ATTR                selectors
              174  LOAD_CONST               0
              176  BINARY_SUBSCR    
              178  LOAD_ATTR                member
              180  LOAD_ATTR                lower
              182  CALL_FUNCTION_0       0  ''
              184  LOAD_FAST                'node'
              186  LOAD_ATTR                name
              188  LOAD_ATTR                lower
              190  CALL_FUNCTION_0       0  ''
              192  LOAD_CONST               3
              194  LOAD_CONST               None
              196  BUILD_SLICE_2         2 
              198  BINARY_SUBSCR    
              200  COMPARE_OP               ==
              202  POP_JUMP_IF_FALSE   222  'to 222'

 L.  27       204  LOAD_FAST                'lst'
              206  LOAD_ATTR                append
              208  LOAD_FAST                'node'
              210  LOAD_ATTR                _position
              212  LOAD_ATTR                line
              214  CALL_FUNCTION_1       1  ''
              216  POP_TOP          
              218  JUMP_ABSOLUTE       226  'to 226'
              220  ELSE                     '222'

 L.  29       220  BREAK_LOOP       
            222_0  COME_FROM           202  '202'
              222  JUMP_ABSOLUTE       230  'to 230'
              224  ELSE                     '226'

 L.  31       224  BREAK_LOOP       
              226  JUMP_BACK           102  'to 102'
              228  ELSE                     '230'

 L.  33       228  BREAK_LOOP       
            230_0  COME_FROM           118  '118'
              230  JUMP_BACK           102  'to 102'
              232  POP_BLOCK        
            234_0  COME_FROM_LOOP       94  '94'
              234  JUMP_BACK            32  'to 32'
              236  POP_BLOCK        
            238_0  COME_FROM_LOOP       26  '26'

 L.  34       238  LOAD_FAST                'lst'
              240  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 222