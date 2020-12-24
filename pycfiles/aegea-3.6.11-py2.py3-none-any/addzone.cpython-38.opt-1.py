# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /aedir_cli/addzone.py
# Compiled at: 2020-03-29 11:31:44
# Size of source mod 2**32: 997 bytes
__doc__ = '\naedir.cli.addzone - Add a zone with two role groups for zone admins / auditors and an init tag\n'
import sys, locale
from ldap0.base import decode_list
import aedir

def main--- This code section failed: ---

 L.  18         0  LOAD_GLOBAL              aedir
                2  LOAD_ATTR                init_logger
                4  LOAD_GLOBAL              sys
                6  LOAD_ATTR                argv
                8  LOAD_CONST               0
               10  BINARY_SUBSCR    
               12  LOAD_CONST               ('log_name',)
               14  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               16  STORE_FAST               'logger'

 L.  19        18  SETUP_FINALLY        60  'to 60'

 L.  20        20  LOAD_GLOBAL              decode_list

 L.  21        22  LOAD_GLOBAL              sys
               24  LOAD_ATTR                argv
               26  LOAD_CONST               1
               28  LOAD_CONST               None
               30  BUILD_SLICE_2         2 
               32  BINARY_SUBSCR    

 L.  22        34  LOAD_GLOBAL              locale
               36  LOAD_METHOD              getdefaultlocale
               38  CALL_METHOD_0         0  ''
               40  LOAD_CONST               1
               42  BINARY_SUBSCR    

 L.  20        44  LOAD_CONST               ('encoding',)
               46  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               48  UNPACK_SEQUENCE_3     3 
               50  STORE_FAST               'zone_cn'
               52  STORE_FAST               'ticket_id'
               54  STORE_FAST               'zone_desc'
               56  POP_BLOCK        
               58  JUMP_FORWARD        130  'to 130'
             60_0  COME_FROM_FINALLY    18  '18'

 L.  24        60  DUP_TOP          
               62  LOAD_GLOBAL              IndexError
               64  LOAD_GLOBAL              ValueError
               66  LOAD_GLOBAL              UnicodeError
               68  BUILD_TUPLE_3         3 
               70  COMPARE_OP               exception-match
               72  POP_JUMP_IF_FALSE   128  'to 128'
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          

 L.  25        80  LOAD_FAST                'logger'
               82  LOAD_METHOD              error
               84  LOAD_STR                 'Missing or wrong command-line args'
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          

 L.  26        90  LOAD_GLOBAL              sys
               92  LOAD_ATTR                stderr
               94  LOAD_METHOD              write

 L.  27        96  LOAD_STR                 '\n\nUsage: {} <zone name> <ticket ID> <description>\n'
               98  LOAD_METHOD              format

 L.  28       100  LOAD_GLOBAL              sys
              102  LOAD_ATTR                argv
              104  LOAD_CONST               0
              106  BINARY_SUBSCR    

 L.  27       108  CALL_METHOD_1         1  ''

 L.  26       110  CALL_METHOD_1         1  ''
              112  POP_TOP          

 L.  31       114  LOAD_GLOBAL              sys
              116  LOAD_METHOD              exit
              118  LOAD_CONST               9
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          
              124  POP_EXCEPT       
              126  JUMP_FORWARD        130  'to 130'
            128_0  COME_FROM            72  '72'
              128  END_FINALLY      
            130_0  COME_FROM           126  '126'
            130_1  COME_FROM            58  '58'

 L.  32       130  LOAD_GLOBAL              aedir
              132  LOAD_METHOD              AEDirObject
              134  LOAD_CONST               None
              136  CALL_METHOD_1         1  ''
              138  SETUP_WITH          160  'to 160'
              140  STORE_FAST               'aedir_conn'

 L.  33       142  LOAD_FAST                'aedir_conn'
              144  LOAD_METHOD              add_aezone
              146  LOAD_FAST                'zone_cn'
              148  LOAD_FAST                'ticket_id'
              150  LOAD_FAST                'zone_desc'
              152  CALL_METHOD_3         3  ''
              154  STORE_FAST               'zone_dn'
              156  POP_BLOCK        
              158  BEGIN_FINALLY    
            160_0  COME_FROM_WITH      138  '138'
              160  WITH_CLEANUP_START
              162  WITH_CLEANUP_FINISH
              164  END_FINALLY      

 L.  34       166  LOAD_FAST                'logger'
              168  LOAD_METHOD              info
              170  LOAD_STR                 'Added zone entry %r'
              172  LOAD_FAST                'zone_dn'
              174  CALL_METHOD_2         2  ''
              176  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 158


if __name__ == '__main__':
    main()