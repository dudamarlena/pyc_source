# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /aedir_cli/reportuser.py
# Compiled at: 2020-03-29 12:38:38
# Size of source mod 2**32: 2001 bytes
__doc__ = '\nGenerates a report of active aeUser entries and their aePerson attributes\n'
import sys, csv, ldap0, aedir
from .reportperson import AEPERSON_ATTRS
AEUSER_ATTRS = [
 'aePerson',
 'uid',
 'uidNumber',
 'entryUUID',
 'aeTicketId',
 'description',
 'memberOf',
 'aeNotBefore',
 'aeNotAfter',
 'pwdChangedTime',
 'createTimestamp',
 'modifyTimestamp']
VIRTUAL_ATTRS = [
 'aeZoneName']

def main--- This code section failed: ---

 L.  37         0  LOAD_GLOBAL              aedir
                2  LOAD_ATTR                AEDirObject
                4  LOAD_CONST               None
                6  LOAD_CONST               1800.0
                8  LOAD_CONST               ('cache_ttl',)
               10  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               12  SETUP_WITH          218  'to 218'
               14  STORE_FAST               'ldap_conn'

 L.  39        16  LOAD_FAST                'ldap_conn'
               18  LOAD_ATTR                search_base
               20  STORE_FAST               'aedir_search_base'

 L.  41        22  LOAD_FAST                'ldap_conn'
               24  LOAD_ATTR                search

 L.  42        26  LOAD_FAST                'aedir_search_base'

 L.  43        28  LOAD_GLOBAL              ldap0
               30  LOAD_ATTR                SCOPE_SUBTREE

 L.  44        32  LOAD_STR                 '(&(objectClass=aeUser)(aeStatus=0))'

 L.  45        34  LOAD_GLOBAL              AEUSER_ATTRS

 L.  41        36  LOAD_CONST               ('attrlist',)
               38  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               40  STORE_FAST               'msg_id'

 L.  48        42  LOAD_GLOBAL              AEUSER_ATTRS
               44  LOAD_GLOBAL              AEPERSON_ATTRS
               46  BINARY_ADD       
               48  LOAD_GLOBAL              VIRTUAL_ATTRS
               50  BINARY_ADD       
               52  STORE_FAST               'column_attrs'

 L.  50        54  LOAD_GLOBAL              csv
               56  LOAD_ATTR                DictWriter
               58  LOAD_GLOBAL              sys
               60  LOAD_ATTR                stdout
               62  LOAD_FAST                'column_attrs'
               64  LOAD_STR                 'excel'
               66  LOAD_CONST               ('dialect',)
               68  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               70  STORE_FAST               'csv_writer'

 L.  53        72  LOAD_FAST                'csv_writer'
               74  LOAD_METHOD              writerow
               76  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               78  LOAD_STR                 'main.<locals>.<dictcomp>'
               80  MAKE_FUNCTION_0          ''

 L.  55        82  LOAD_FAST                'column_attrs'

 L.  53        84  GET_ITER         
               86  CALL_FUNCTION_1       1  ''
               88  CALL_METHOD_1         1  ''
               90  POP_TOP          

 L.  58        92  LOAD_FAST                'ldap_conn'
               94  LOAD_METHOD              results
               96  LOAD_FAST                'msg_id'
               98  CALL_METHOD_1         1  ''
              100  GET_ITER         
              102  FOR_ITER            214  'to 214'
              104  STORE_FAST               'res'

 L.  59       106  LOAD_FAST                'res'
              108  LOAD_ATTR                rdata
              110  GET_ITER         
              112  FOR_ITER            212  'to 212'
              114  STORE_FAST               'result'

 L.  60       116  LOAD_FAST                'result'
              118  LOAD_ATTR                dn_s
              120  STORE_FAST               'user_dn'

 L.  61       122  LOAD_FAST                'result'
              124  LOAD_ATTR                entry_s
              126  STORE_FAST               'user_entry'

 L.  63       128  LOAD_GLOBAL              aedir
              130  LOAD_ATTR                extract_zone
              132  LOAD_FAST                'user_dn'
              134  LOAD_FAST                'aedir_search_base'
              136  LOAD_CONST               ('aeroot_dn',)
              138  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L.  62       140  BUILD_LIST_1          1 
              142  LOAD_FAST                'user_entry'
              144  LOAD_STR                 'aeZoneName'
              146  STORE_SUBSCR     

 L.  66       148  LOAD_FAST                'ldap_conn'
              150  LOAD_ATTR                read_s
              152  LOAD_FAST                'user_entry'
              154  LOAD_STR                 'aePerson'
              156  BINARY_SUBSCR    
              158  LOAD_CONST               0
              160  BINARY_SUBSCR    
              162  LOAD_GLOBAL              AEPERSON_ATTRS
              164  LOAD_CONST               ('attrlist',)
              166  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              168  STORE_FAST               'person_result'

 L.  67       170  LOAD_FAST                'user_entry'
              172  LOAD_METHOD              update
              174  LOAD_FAST                'person_result'
              176  LOAD_ATTR                entry_s
              178  CALL_METHOD_1         1  ''
              180  POP_TOP          

 L.  69       182  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              184  LOAD_STR                 'main.<locals>.<dictcomp>'
              186  MAKE_FUNCTION_0          ''

 L.  71       188  LOAD_FAST                'user_entry'
              190  LOAD_METHOD              items
              192  CALL_METHOD_0         0  ''

 L.  69       194  GET_ITER         
              196  CALL_FUNCTION_1       1  ''
              198  STORE_FAST               'user_dict'

 L.  74       200  LOAD_FAST                'csv_writer'
              202  LOAD_METHOD              writerow
              204  LOAD_FAST                'user_dict'
              206  CALL_METHOD_1         1  ''
              208  POP_TOP          
              210  JUMP_BACK           112  'to 112'
              212  JUMP_BACK           102  'to 102'
              214  POP_BLOCK        
              216  BEGIN_FINALLY    
            218_0  COME_FROM_WITH       12  '12'
              218  WITH_CLEANUP_START
              220  WITH_CLEANUP_FINISH
              222  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 216


if __name__ == '__main__':
    main()