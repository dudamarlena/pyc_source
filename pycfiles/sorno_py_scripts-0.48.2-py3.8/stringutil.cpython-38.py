# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sorno/stringutil.py
# Compiled at: 2020-03-16 00:44:32
# Size of source mod 2**32: 1435 bytes
"""
Utility functions for dealing with strings
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import re

def oneline(s):
    """
    Compact all space characters to a single space. Leading and trailing
    spaces are stripped.
    """
    return re.sub('\\s+', ' ', s).strip()


def u(s):
    """
    Converts s to unicode with utf-8 encoding if it is not already a unicode.
    Leave it as is otherwise.
    """
    if type(s) == unicode:
        return s
    return s.decode('utf8')


def format_with_default_value--- This code section failed: ---

 L.  46         0  LOAD_GLOBAL              dict
                2  BUILD_TUPLE_0         0 
                4  LOAD_FAST                'd'
                6  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
                8  STORE_FAST               'copy'

 L.  48        10  SETUP_FINALLY        26  'to 26'

 L.  49        12  LOAD_FAST                's'
               14  LOAD_ATTR                format
               16  BUILD_TUPLE_0         0 
               18  LOAD_FAST                'copy'
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY    10  '10'

 L.  50        26  DUP_TOP          
               28  LOAD_GLOBAL              KeyError
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    80  'to 80'
               34  POP_TOP          
               36  STORE_FAST               'ex'
               38  POP_TOP          
               40  SETUP_FINALLY        68  'to 68'

 L.  51        42  LOAD_FAST                'ex'
               44  LOAD_ATTR                args
               46  LOAD_CONST               0
               48  BINARY_SUBSCR    
               50  STORE_FAST               'key'

 L.  52        52  LOAD_FAST                'handle_missing_key'
               54  LOAD_FAST                'key'
               56  CALL_FUNCTION_1       1  ''
               58  LOAD_FAST                'copy'
               60  LOAD_FAST                'key'
               62  STORE_SUBSCR     
               64  POP_BLOCK        
               66  BEGIN_FINALLY    
             68_0  COME_FROM_FINALLY    40  '40'
               68  LOAD_CONST               None
               70  STORE_FAST               'ex'
               72  DELETE_FAST              'ex'
               74  END_FINALLY      
               76  POP_EXCEPT       
               78  JUMP_BACK            10  'to 10'
             80_0  COME_FROM            32  '32'
               80  END_FINALLY      
               82  JUMP_BACK            10  'to 10'

Parse error at or near `JUMP_BACK' instruction at offset 78