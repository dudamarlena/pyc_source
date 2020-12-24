# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /aedir_cli/nextgid.py
# Compiled at: 2020-03-29 11:31:44
# Size of source mod 2**32: 2940 bytes
__doc__ = '\nSets next GID number to highest GID found + 1\n\nThis script must run locally on a Æ-DIR provider\n'
import sys, ldap0, aedir
GID_ATTR = 'gidNumber'
UID_ATTR = 'uidNumber'
UID_GID_ALIGN = True

def main--- This code section failed: ---

 L.  26         0  LOAD_GLOBAL              aedir
                2  LOAD_ATTR                init_logger
                4  LOAD_GLOBAL              sys
                6  LOAD_ATTR                argv
                8  LOAD_CONST               0
               10  BINARY_SUBSCR    
               12  LOAD_CONST               ('log_name',)
               14  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               16  STORE_FAST               'logger'

 L.  28        18  LOAD_GLOBAL              aedir
               20  LOAD_METHOD              AEDirObject
               22  LOAD_CONST               None
               24  CALL_METHOD_1         1  ''
            26_28  SETUP_WITH          492  'to 492'
               30  STORE_FAST               'aedir_conn'

 L.  30        32  LOAD_FAST                'aedir_conn'
               34  LOAD_ATTR                find_highest_id

 L.  31        36  LOAD_FAST                'aedir_conn'
               38  LOAD_ATTR                search_base

 L.  32        40  LOAD_GLOBAL              GID_ATTR

 L.  30        42  LOAD_CONST               ('id_pool_dn', 'id_pool_attr')
               44  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               46  STORE_FAST               'highest_gid_number'

 L.  34        48  LOAD_FAST                'aedir_conn'
               50  LOAD_ATTR                read_s

 L.  35        52  LOAD_FAST                'aedir_conn'
               54  LOAD_ATTR                search_base

 L.  36        56  LOAD_GLOBAL              GID_ATTR
               58  LOAD_GLOBAL              UID_ATTR
               60  BUILD_LIST_2          2 

 L.  34        62  LOAD_CONST               ('attrlist',)
               64  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               66  LOAD_ATTR                entry_s
               68  STORE_FAST               'aeroot_entry'

 L.  39        70  SETUP_FINALLY        92  'to 92'

 L.  40        72  LOAD_GLOBAL              int
               74  LOAD_FAST                'aeroot_entry'
               76  LOAD_GLOBAL              GID_ATTR
               78  BINARY_SUBSCR    
               80  LOAD_CONST               0
               82  BINARY_SUBSCR    
               84  CALL_FUNCTION_1       1  ''
               86  STORE_FAST               'current_next_gid'
               88  POP_BLOCK        
               90  JUMP_FORWARD        116  'to 116'
             92_0  COME_FROM_FINALLY    70  '70'

 L.  41        92  DUP_TOP          
               94  LOAD_GLOBAL              KeyError
               96  COMPARE_OP               exception-match
               98  POP_JUMP_IF_FALSE   114  'to 114'
              100  POP_TOP          
              102  POP_TOP          
              104  POP_TOP          

 L.  42       106  LOAD_CONST               None
              108  STORE_FAST               'current_next_gid'
              110  POP_EXCEPT       
              112  JUMP_FORWARD        116  'to 116'
            114_0  COME_FROM            98  '98'
              114  END_FINALLY      
            116_0  COME_FROM           112  '112'
            116_1  COME_FROM            90  '90'

 L.  43       116  LOAD_FAST                'logger'
              118  LOAD_METHOD              debug
              120  LOAD_STR                 'Current %r value: %s'
              122  LOAD_GLOBAL              GID_ATTR
              124  LOAD_FAST                'current_next_gid'
              126  CALL_METHOD_3         3  ''
              128  POP_TOP          

 L.  44       130  SETUP_FINALLY       152  'to 152'

 L.  45       132  LOAD_GLOBAL              int
              134  LOAD_FAST                'aeroot_entry'
              136  LOAD_GLOBAL              UID_ATTR
              138  BINARY_SUBSCR    
              140  LOAD_CONST               0
              142  BINARY_SUBSCR    
              144  CALL_FUNCTION_1       1  ''
              146  STORE_FAST               'current_next_uid'
              148  POP_BLOCK        
              150  JUMP_FORWARD        176  'to 176'
            152_0  COME_FROM_FINALLY   130  '130'

 L.  46       152  DUP_TOP          
              154  LOAD_GLOBAL              KeyError
              156  COMPARE_OP               exception-match
              158  POP_JUMP_IF_FALSE   174  'to 174'
              160  POP_TOP          
              162  POP_TOP          
              164  POP_TOP          

 L.  47       166  LOAD_CONST               None
              168  STORE_FAST               'current_next_uid'
              170  POP_EXCEPT       
              172  JUMP_FORWARD        176  'to 176'
            174_0  COME_FROM           158  '158'
              174  END_FINALLY      
            176_0  COME_FROM           172  '172'
            176_1  COME_FROM           150  '150'

 L.  48       176  LOAD_FAST                'logger'
              178  LOAD_METHOD              debug
              180  LOAD_STR                 'Current %r value: %s'
              182  LOAD_GLOBAL              UID_ATTR
              184  LOAD_FAST                'current_next_uid'
              186  CALL_METHOD_3         3  ''
              188  POP_TOP          

 L.  50       190  BUILD_LIST_0          0 
              192  STORE_FAST               'modlist'

 L.  53       194  LOAD_FAST                'current_next_gid'
              196  LOAD_FAST                'highest_gid_number'
              198  LOAD_CONST               1
              200  BINARY_ADD       
              202  COMPARE_OP               !=
          204_206  POP_JUMP_IF_FALSE   296  'to 296'

 L.  54       208  LOAD_FAST                'modlist'
              210  LOAD_METHOD              append

 L.  55       212  LOAD_GLOBAL              ldap0
              214  LOAD_ATTR                MOD_ADD
              216  LOAD_GLOBAL              GID_ATTR
              218  LOAD_METHOD              encode
              220  LOAD_STR                 'ascii'
              222  CALL_METHOD_1         1  ''
              224  LOAD_GLOBAL              str
              226  LOAD_FAST                'highest_gid_number'
              228  LOAD_CONST               1
              230  BINARY_ADD       
              232  CALL_FUNCTION_1       1  ''
              234  LOAD_METHOD              encode
              236  LOAD_STR                 'ascii'
              238  CALL_METHOD_1         1  ''
              240  BUILD_LIST_1          1 
              242  BUILD_TUPLE_3         3 

 L.  54       244  CALL_METHOD_1         1  ''
              246  POP_TOP          

 L.  57       248  LOAD_FAST                'current_next_gid'
              250  LOAD_CONST               None
              252  COMPARE_OP               is-not
          254_256  POP_JUMP_IF_FALSE   310  'to 310'

 L.  58       258  LOAD_FAST                'modlist'
              260  LOAD_METHOD              append

 L.  59       262  LOAD_GLOBAL              ldap0
              264  LOAD_ATTR                MOD_DELETE
              266  LOAD_GLOBAL              GID_ATTR
              268  LOAD_METHOD              encode
              270  LOAD_STR                 'ascii'
              272  CALL_METHOD_1         1  ''
              274  LOAD_GLOBAL              str
              276  LOAD_FAST                'current_next_gid'
              278  CALL_FUNCTION_1       1  ''
              280  LOAD_METHOD              encode
              282  LOAD_STR                 'ascii'
              284  CALL_METHOD_1         1  ''
              286  BUILD_LIST_1          1 
              288  BUILD_TUPLE_3         3 

 L.  58       290  CALL_METHOD_1         1  ''
              292  POP_TOP          
              294  JUMP_FORWARD        310  'to 310'
            296_0  COME_FROM           204  '204'

 L.  62       296  LOAD_FAST                'logger'
              298  LOAD_METHOD              debug
              300  LOAD_STR                 'Current %r value %d seems ok => no change.'
              302  LOAD_GLOBAL              GID_ATTR
              304  LOAD_FAST                'current_next_gid'
              306  CALL_METHOD_3         3  ''
              308  POP_TOP          
            310_0  COME_FROM           294  '294'
            310_1  COME_FROM           254  '254'

 L.  65       310  LOAD_FAST                'current_next_uid'
              312  LOAD_CONST               None
              314  COMPARE_OP               is-not
          316_318  POP_JUMP_IF_FALSE   440  'to 440'

 L.  67       320  LOAD_GLOBAL              UID_GID_ALIGN
          322_324  POP_JUMP_IF_FALSE   332  'to 332'

 L.  68       326  LOAD_FAST                'highest_gid_number'
              328  STORE_FAST               'highest_uid_number'
              330  JUMP_FORWARD        348  'to 348'
            332_0  COME_FROM           322  '322'

 L.  70       332  LOAD_FAST                'aedir_conn'
              334  LOAD_ATTR                find_highest_id

 L.  71       336  LOAD_FAST                'aedir_conn'
              338  LOAD_ATTR                search_base

 L.  72       340  LOAD_GLOBAL              UID_ATTR

 L.  70       342  LOAD_CONST               ('id_pool_dn', 'id_pool_attr')
              344  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              346  STORE_FAST               'highest_uid_number'
            348_0  COME_FROM           330  '330'

 L.  75       348  LOAD_FAST                'current_next_uid'
              350  LOAD_FAST                'highest_uid_number'
              352  LOAD_CONST               1
              354  BINARY_ADD       
              356  COMPARE_OP               !=
          358_360  POP_JUMP_IF_FALSE   426  'to 426'

 L.  76       362  LOAD_FAST                'modlist'
              364  LOAD_METHOD              append

 L.  77       366  LOAD_GLOBAL              ldap0
              368  LOAD_ATTR                MOD_ADD
              370  LOAD_GLOBAL              UID_ATTR
              372  LOAD_GLOBAL              str
              374  LOAD_FAST                'highest_uid_number'
              376  LOAD_CONST               1
              378  BINARY_ADD       
              380  CALL_FUNCTION_1       1  ''
              382  BUILD_LIST_1          1 
              384  BUILD_TUPLE_3         3 

 L.  76       386  CALL_METHOD_1         1  ''
              388  POP_TOP          

 L.  79       390  LOAD_FAST                'current_next_uid'
              392  LOAD_CONST               None
              394  COMPARE_OP               is-not
          396_398  POP_JUMP_IF_FALSE   440  'to 440'

 L.  80       400  LOAD_FAST                'modlist'
              402  LOAD_METHOD              append

 L.  81       404  LOAD_GLOBAL              ldap0
              406  LOAD_ATTR                MOD_DELETE
              408  LOAD_GLOBAL              UID_ATTR
              410  LOAD_GLOBAL              str
              412  LOAD_FAST                'current_next_uid'
              414  CALL_FUNCTION_1       1  ''
              416  BUILD_LIST_1          1 
              418  BUILD_TUPLE_3         3 

 L.  80       420  CALL_METHOD_1         1  ''
              422  POP_TOP          
              424  JUMP_FORWARD        440  'to 440'
            426_0  COME_FROM           358  '358'

 L.  84       426  LOAD_FAST                'logger'
              428  LOAD_METHOD              debug

 L.  85       430  LOAD_STR                 'Current %r value %d seems ok => no change.'

 L.  86       432  LOAD_GLOBAL              UID_ATTR

 L.  87       434  LOAD_FAST                'current_next_uid'

 L.  84       436  CALL_METHOD_3         3  ''
              438  POP_TOP          
            440_0  COME_FROM           424  '424'
            440_1  COME_FROM           396  '396'
            440_2  COME_FROM           316  '316'

 L.  90       440  LOAD_FAST                'modlist'
          442_444  POP_JUMP_IF_FALSE   478  'to 478'

 L.  91       446  LOAD_FAST                'aedir_conn'
              448  LOAD_METHOD              modify_s
              450  LOAD_FAST                'aedir_conn'
              452  LOAD_ATTR                search_base
              454  LOAD_FAST                'modlist'
              456  CALL_METHOD_2         2  ''
              458  POP_TOP          

 L.  92       460  LOAD_FAST                'logger'
              462  LOAD_METHOD              info

 L.  93       464  LOAD_STR                 'Updated entry %r with %r'

 L.  94       466  LOAD_FAST                'aedir_conn'
              468  LOAD_ATTR                search_base

 L.  95       470  LOAD_FAST                'modlist'

 L.  92       472  CALL_METHOD_3         3  ''
              474  POP_TOP          
              476  JUMP_FORWARD        488  'to 488'
            478_0  COME_FROM           442  '442'

 L.  98       478  LOAD_FAST                'logger'
              480  LOAD_METHOD              info
              482  LOAD_STR                 'no modifications'
              484  CALL_METHOD_1         1  ''
              486  POP_TOP          
            488_0  COME_FROM           476  '476'
              488  POP_BLOCK        
              490  BEGIN_FINALLY    
            492_0  COME_FROM_WITH       26  '26'
              492  WITH_CLEANUP_START
              494  WITH_CLEANUP_FINISH
              496  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 490


if __name__ == '__main__':
    main()