# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /aedir_cli/passwd.py
# Compiled at: 2020-03-29 11:31:44
# Size of source mod 2**32: 1718 bytes
__doc__ = '\nSets the password of the specified aeUser/aeService or aeHost entry\nreferenced by uid or host attribute\n\nThis script must run locally on a Æ-DIR provider\n'
import sys, getpass
from ldap0 import LDAPError
import aedir

def main--- This code section failed: ---

 L.  21         0  LOAD_GLOBAL              aedir
                2  LOAD_ATTR                init_logger
                4  LOAD_GLOBAL              sys
                6  LOAD_ATTR                argv
                8  LOAD_CONST               0
               10  BINARY_SUBSCR    
               12  LOAD_CONST               ('log_name',)
               14  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               16  STORE_FAST               'logger'

 L.  23        18  SETUP_FINALLY        34  'to 34'

 L.  24        20  LOAD_GLOBAL              sys
               22  LOAD_ATTR                argv
               24  LOAD_CONST               1
               26  BINARY_SUBSCR    
               28  STORE_FAST               'arg_value'
               30  POP_BLOCK        
               32  JUMP_FORWARD         88  'to 88'
             34_0  COME_FROM_FINALLY    18  '18'

 L.  25        34  DUP_TOP          
               36  LOAD_GLOBAL              IndexError
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    86  'to 86'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L.  26        48  LOAD_GLOBAL              sys
               50  LOAD_ATTR                stderr
               52  LOAD_METHOD              write
               54  LOAD_STR                 'Usage: {} <username|hostname>\n'
               56  LOAD_METHOD              format
               58  LOAD_GLOBAL              sys
               60  LOAD_ATTR                argv
               62  LOAD_CONST               0
               64  BINARY_SUBSCR    
               66  CALL_METHOD_1         1  ''
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          

 L.  27        72  LOAD_GLOBAL              sys
               74  LOAD_METHOD              exit
               76  LOAD_CONST               9
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          
               82  POP_EXCEPT       
               84  JUMP_FORWARD         88  'to 88'
             86_0  COME_FROM            40  '40'
               86  END_FINALLY      
             88_0  COME_FROM            84  '84'
             88_1  COME_FROM            32  '32'

 L.  29        88  LOAD_GLOBAL              aedir
               90  LOAD_METHOD              AEDirObject
               92  LOAD_CONST               None
               94  CALL_METHOD_1         1  ''
               96  SETUP_WITH          308  'to 308'
               98  STORE_FAST               'aedir_conn'

 L.  31       100  LOAD_FAST                'logger'
              102  LOAD_METHOD              debug
              104  LOAD_STR                 'successfully connected to %r as %r'
              106  LOAD_FAST                'aedir_conn'
              108  LOAD_ATTR                uri
              110  LOAD_FAST                'aedir_conn'
              112  LOAD_METHOD              whoami_s
              114  CALL_METHOD_0         0  ''
              116  CALL_METHOD_3         3  ''
              118  POP_TOP          

 L.  33       120  LOAD_GLOBAL              getpass
              122  LOAD_METHOD              getpass

 L.  34       124  LOAD_STR                 'Enter new password for {} (empty generates password): '
              126  LOAD_METHOD              format
              128  LOAD_FAST                'arg_value'
              130  CALL_METHOD_1         1  ''

 L.  33       132  CALL_METHOD_1         1  ''
              134  STORE_FAST               'new_password1'

 L.  37       136  LOAD_FAST                'new_password1'
              138  POP_JUMP_IF_FALSE   182  'to 182'

 L.  39       140  LOAD_GLOBAL              getpass
              142  LOAD_METHOD              getpass
              144  LOAD_STR                 'repeat password: '
              146  CALL_METHOD_1         1  ''
              148  STORE_FAST               'new_password2'

 L.  40       150  LOAD_FAST                'new_password1'
              152  LOAD_FAST                'new_password2'
              154  COMPARE_OP               !=
              156  POP_JUMP_IF_FALSE   186  'to 186'

 L.  41       158  LOAD_GLOBAL              sys
              160  LOAD_ATTR                stderr
              162  LOAD_METHOD              write
              164  LOAD_STR                 '2nd input for new password differs!\n'
              166  CALL_METHOD_1         1  ''
              168  POP_TOP          

 L.  42       170  LOAD_GLOBAL              sys
              172  LOAD_METHOD              exit
              174  LOAD_CONST               1
              176  CALL_METHOD_1         1  ''
              178  POP_TOP          
              180  JUMP_FORWARD        186  'to 186'
            182_0  COME_FROM           138  '138'

 L.  45       182  LOAD_CONST               None
              184  STORE_FAST               'new_password2'
            186_0  COME_FROM           180  '180'
            186_1  COME_FROM           156  '156'

 L.  47       186  SETUP_FINALLY       208  'to 208'

 L.  48       188  LOAD_FAST                'aedir_conn'
              190  LOAD_METHOD              set_password
              192  LOAD_FAST                'arg_value'
              194  LOAD_FAST                'new_password2'
              196  CALL_METHOD_2         2  ''
              198  UNPACK_SEQUENCE_2     2 
              200  STORE_FAST               'entry_dn'
              202  STORE_FAST               'new_pw'
              204  POP_BLOCK        
              206  JUMP_FORWARD        266  'to 266'
            208_0  COME_FROM_FINALLY   186  '186'

 L.  49       208  DUP_TOP          
              210  LOAD_GLOBAL              LDAPError
              212  COMPARE_OP               exception-match
          214_216  POP_JUMP_IF_FALSE   264  'to 264'
              218  POP_TOP          
              220  STORE_FAST               'ldap_err'
              222  POP_TOP          
              224  SETUP_FINALLY       252  'to 252'

 L.  50       226  LOAD_FAST                'logger'
              228  LOAD_METHOD              error
              230  LOAD_STR                 'LDAPError setting password: %s'
              232  LOAD_FAST                'ldap_err'
              234  CALL_METHOD_2         2  ''
              236  POP_TOP          

 L.  51       238  LOAD_GLOBAL              sys
              240  LOAD_METHOD              exit
              242  LOAD_CONST               1
              244  CALL_METHOD_1         1  ''
              246  POP_TOP          
              248  POP_BLOCK        
              250  BEGIN_FINALLY    
            252_0  COME_FROM_FINALLY   224  '224'
              252  LOAD_CONST               None
              254  STORE_FAST               'ldap_err'
              256  DELETE_FAST              'ldap_err'
              258  END_FINALLY      
              260  POP_EXCEPT       
              262  JUMP_FORWARD        304  'to 304'
            264_0  COME_FROM           214  '214'
              264  END_FINALLY      
            266_0  COME_FROM           206  '206'

 L.  53       266  LOAD_FAST                'new_password2'
              268  LOAD_CONST               None
              270  COMPARE_OP               is
          272_274  POP_JUMP_IF_FALSE   292  'to 292'

 L.  54       276  LOAD_GLOBAL              sys
              278  LOAD_ATTR                stdout
              280  LOAD_METHOD              write
              282  LOAD_STR                 'Generated password: %s\n'
              284  LOAD_FAST                'new_pw'
              286  BINARY_MODULO    
              288  CALL_METHOD_1         1  ''
              290  POP_TOP          
            292_0  COME_FROM           272  '272'

 L.  55       292  LOAD_FAST                'logger'
              294  LOAD_METHOD              info
              296  LOAD_STR                 'Successfully set password of entry %r'
              298  LOAD_FAST                'entry_dn'
              300  CALL_METHOD_2         2  ''
              302  POP_TOP          
            304_0  COME_FROM           262  '262'
              304  POP_BLOCK        
              306  BEGIN_FINALLY    
            308_0  COME_FROM_WITH       96  '96'
              308  WITH_CLEANUP_START
              310  WITH_CLEANUP_FINISH
              312  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 306


if __name__ == '__main__':
    main()