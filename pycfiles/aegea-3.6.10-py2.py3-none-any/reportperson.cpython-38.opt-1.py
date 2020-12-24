# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /aedir_cli/reportperson.py
# Compiled at: 2020-03-29 12:22:56
# Size of source mod 2**32: 1892 bytes
__doc__ = '\nGenerates a report of aePerson entries referenced by active aeUser entries\n'
import sys, csv, ldap0
from ldap0.controls.deref import DereferenceControl
import aedir
USER_ATTRS = [
 '1.1']
AEPERSON_ATTRS = [
 'sn',
 'givenName',
 'cn',
 'mail',
 'employeeNumber',
 'employeeType',
 'telephoneNumber',
 'mobile',
 'homePhone',
 'aeDept',
 'ou',
 'departmentNumber',
 'o',
 'street',
 'l',
 'c']
DEREF_CONTROL = DereferenceControl(True, {'aePerson': AEPERSON_ATTRS})

def main--- This code section failed: ---

 L.  41         0  BUILD_MAP_0           0 
                2  STORE_FAST               'person_dict'

 L.  43         4  LOAD_GLOBAL              aedir
                6  LOAD_ATTR                AEDirObject
                8  LOAD_CONST               None
               10  LOAD_CONST               1800.0
               12  LOAD_CONST               ('cache_ttl',)
               14  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               16  SETUP_WITH          166  'to 166'
               18  STORE_FAST               'ldap_conn'

 L.  45        20  LOAD_FAST                'ldap_conn'
               22  LOAD_ATTR                search

 L.  46        24  LOAD_FAST                'ldap_conn'
               26  LOAD_ATTR                search_base

 L.  47        28  LOAD_GLOBAL              ldap0
               30  LOAD_ATTR                SCOPE_SUBTREE

 L.  48        32  LOAD_STR                 '(&(objectClass=aeUser)(aeStatus=0))'

 L.  49        34  LOAD_GLOBAL              USER_ATTRS

 L.  50        36  LOAD_GLOBAL              DEREF_CONTROL
               38  BUILD_LIST_1          1 

 L.  45        40  LOAD_CONST               ('attrlist', 'req_ctrls')
               42  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               44  STORE_FAST               'msg_id'

 L.  53        46  LOAD_FAST                'ldap_conn'
               48  LOAD_METHOD              results
               50  LOAD_FAST                'msg_id'
               52  CALL_METHOD_1         1  ''
               54  GET_ITER         
               56  FOR_ITER            162  'to 162'
               58  STORE_FAST               'res'

 L.  54        60  LOAD_FAST                'res'
               62  LOAD_ATTR                rdata
               64  GET_ITER         
             66_0  COME_FROM            92  '92'
             66_1  COME_FROM            74  '74'
               66  FOR_ITER            160  'to 160'
               68  STORE_FAST               'result'

 L.  56        70  LOAD_FAST                'result'
               72  LOAD_ATTR                ctrls
               74  POP_JUMP_IF_FALSE    66  'to 66'
               76  LOAD_FAST                'result'
               78  LOAD_ATTR                ctrls
               80  LOAD_CONST               0
               82  BINARY_SUBSCR    
               84  LOAD_ATTR                controlType
               86  LOAD_GLOBAL              DereferenceControl
               88  LOAD_ATTR                controlType
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_FALSE    66  'to 66'

 L.  57        94  LOAD_FAST                'result'
               96  LOAD_ATTR                ctrls
               98  LOAD_CONST               0
              100  BINARY_SUBSCR    
              102  STORE_FAST               'deref_control'

 L.  58       104  LOAD_GLOBAL              dict
              106  LOAD_LISTCOMP            '<code_object <listcomp>>'
              108  LOAD_STR                 'main.<locals>.<listcomp>'
              110  MAKE_FUNCTION_0          ''

 L.  60       112  LOAD_FAST                'deref_control'
              114  LOAD_ATTR                derefRes
              116  LOAD_STR                 'aePerson'
              118  BINARY_SUBSCR    
              120  LOAD_CONST               0
              122  BINARY_SUBSCR    
              124  LOAD_ATTR                entry_s
              126  LOAD_METHOD              items
              128  CALL_METHOD_0         0  ''

 L.  58       130  GET_ITER         
              132  CALL_FUNCTION_1       1  ''
              134  CALL_FUNCTION_1       1  ''
              136  LOAD_FAST                'person_dict'
              138  LOAD_FAST                'deref_control'
              140  LOAD_ATTR                derefRes
              142  LOAD_STR                 'aePerson'
              144  BINARY_SUBSCR    
              146  LOAD_CONST               0
              148  BINARY_SUBSCR    
              150  LOAD_ATTR                dn_s
              152  LOAD_METHOD              lower
              154  CALL_METHOD_0         0  ''
              156  STORE_SUBSCR     
              158  JUMP_BACK            66  'to 66'
              160  JUMP_BACK            56  'to 56'
              162  POP_BLOCK        
              164  BEGIN_FINALLY    
            166_0  COME_FROM_WITH       16  '16'
              166  WITH_CLEANUP_START
              168  WITH_CLEANUP_FINISH
              170  END_FINALLY      

 L.  64       172  LOAD_GLOBAL              csv
              174  LOAD_ATTR                DictWriter

 L.  65       176  LOAD_GLOBAL              sys
              178  LOAD_ATTR                stdout

 L.  66       180  LOAD_GLOBAL              AEPERSON_ATTRS

 L.  67       182  LOAD_STR                 'excel'

 L.  64       184  LOAD_CONST               ('dialect',)
              186  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              188  STORE_FAST               'csv_writer'

 L.  69       190  LOAD_FAST                'csv_writer'
              192  LOAD_METHOD              writerow

 L.  70       194  LOAD_GLOBAL              dict
              196  LOAD_LISTCOMP            '<code_object <listcomp>>'
              198  LOAD_STR                 'main.<locals>.<listcomp>'
              200  MAKE_FUNCTION_0          ''

 L.  72       202  LOAD_GLOBAL              AEPERSON_ATTRS

 L.  70       204  GET_ITER         
              206  CALL_FUNCTION_1       1  ''
              208  CALL_FUNCTION_1       1  ''

 L.  69       210  CALL_METHOD_1         1  ''
              212  POP_TOP          

 L.  75       214  LOAD_FAST                'csv_writer'
              216  LOAD_METHOD              writerows
              218  LOAD_FAST                'person_dict'
              220  LOAD_METHOD              values
              222  CALL_METHOD_0         0  ''
              224  CALL_METHOD_1         1  ''
              226  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 164


if __name__ == '__main__':
    main()