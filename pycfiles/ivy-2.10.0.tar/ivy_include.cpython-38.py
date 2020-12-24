# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmulholl/dev/src/ivy/ivy/extensions/ivy_include.py
# Compiled at: 2020-04-04 05:06:35
# Size of source mod 2**32: 1044 bytes
import shortcodes, ivy, os

@shortcodes.register('include')
def handler--- This code section failed: ---

 L.  22         0  LOAD_FAST                'pargs'
                2  POP_JUMP_IF_FALSE    68  'to 68'

 L.  23         4  LOAD_GLOBAL              ivy
                6  LOAD_ATTR                site
                8  LOAD_METHOD              inc
               10  LOAD_FAST                'pargs'
               12  LOAD_CONST               0
               14  BINARY_SUBSCR    
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'path'

 L.  24        20  LOAD_GLOBAL              os
               22  LOAD_ATTR                path
               24  LOAD_METHOD              exists
               26  LOAD_FAST                'path'
               28  CALL_METHOD_1         1  ''
               30  POP_JUMP_IF_FALSE    68  'to 68'

 L.  25        32  LOAD_GLOBAL              open
               34  LOAD_FAST                'path'
               36  CALL_FUNCTION_1       1  ''
               38  SETUP_WITH           62  'to 62'
               40  STORE_FAST               'file'

 L.  26        42  LOAD_FAST                'file'
               44  LOAD_METHOD              read
               46  CALL_METHOD_0         0  ''
               48  POP_BLOCK        
               50  ROT_TWO          
               52  BEGIN_FINALLY    
               54  WITH_CLEANUP_START
               56  WITH_CLEANUP_FINISH
               58  POP_FINALLY           0  ''
               60  RETURN_VALUE     
             62_0  COME_FROM_WITH       38  '38'
               62  WITH_CLEANUP_START
               64  WITH_CLEANUP_FINISH
               66  END_FINALLY      
             68_0  COME_FROM            30  '30'
             68_1  COME_FROM             2  '2'

 L.  27        68  LOAD_STR                 ''
               70  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_TWO' instruction at offset 50