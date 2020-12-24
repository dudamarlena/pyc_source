# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /aedir_pproc/status.py
# Compiled at: 2020-02-05 10:31:34
# Size of source mod 2**32: 3530 bytes
__doc__ = '\naedir_pproc.status - updates aeStatus of expired AE-DIR entries (aeObject)\n'
import time, ldap0, aedir, aedir.process
from .__about__ import __version__, __author__, __license__

class AEStatusUpdater(aedir.process.AEProcess):
    """AEStatusUpdater"""
    script_version = __version__

    def __init__(self):
        aedir.process.AEProcess.__init__(self)
        self.aeobject_counter = 0
        self.modify_counter = 0
        self.error_counter = 0

    def exit(self):
        """
        Log a summary of actions and errors, mainly counters
        """
        self.logger.debug('Found %d auto-expiry AE-DIR entries', self.aeobject_counter)
        if self.modify_counter:
            self.logger.info('Modifed %d auto-expiry AE-DIR entries.', self.modify_counter)
        if self.error_counter:
            self.logger.error('%d errors.', self.error_counter)

    def run_worker--- This code section failed: ---

 L.  48         0  LOAD_GLOBAL              ldap0
                2  LOAD_ATTR                functions
                4  LOAD_METHOD              strf_secs
                6  LOAD_GLOBAL              time
                8  LOAD_METHOD              time
               10  CALL_METHOD_0         0  ''
               12  CALL_METHOD_1         1  ''
               14  STORE_FAST               'current_time_str'

 L.  49        16  LOAD_FAST                'self'
               18  LOAD_ATTR                logger
               20  LOAD_METHOD              debug
               22  LOAD_STR                 'current_time_str = %r'
               24  LOAD_FAST                'current_time_str'
               26  CALL_METHOD_2         2  ''
               28  POP_TOP          

 L.  51        30  LOAD_STR                 '(&(objectClass=aeObject)(aeNotAfter<={0})(|(&(aeStatus<=0)(aeExpiryStatus>=1))(&(aeStatus<=1)(aeExpiryStatus>=2))))'

 L.  50        32  LOAD_METHOD              format

 L.  59        34  LOAD_FAST                'current_time_str'

 L.  50        36  CALL_METHOD_1         1  ''
               38  STORE_FAST               'expiry_filter'

 L.  60        40  LOAD_FAST                'self'
               42  LOAD_ATTR                logger
               44  LOAD_METHOD              debug
               46  LOAD_STR                 'expiry_filter = %r'
               48  LOAD_FAST                'expiry_filter'
               50  CALL_METHOD_2         2  ''
               52  POP_TOP          

 L.  61        54  SETUP_FINALLY        90  'to 90'

 L.  62        56  LOAD_FAST                'self'
               58  LOAD_ATTR                ldap_conn
               60  LOAD_ATTR                search

 L.  63        62  LOAD_FAST                'self'
               64  LOAD_ATTR                ldap_conn
               66  LOAD_ATTR                search_base

 L.  64        68  LOAD_GLOBAL              ldap0
               70  LOAD_ATTR                SCOPE_SUBTREE

 L.  65        72  LOAD_FAST                'expiry_filter'

 L.  66        74  LOAD_STR                 'aeStatus'
               76  LOAD_STR                 'aeExpiryStatus'
               78  BUILD_LIST_2          2 

 L.  62        80  LOAD_CONST               ('attrlist',)
               82  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               84  STORE_FAST               'msg_id'
               86  POP_BLOCK        
               88  JUMP_FORWARD        148  'to 148'
             90_0  COME_FROM_FINALLY    54  '54'

 L.  68        90  DUP_TOP          
               92  LOAD_GLOBAL              ldap0
               94  LOAD_ATTR                LDAPError
               96  COMPARE_OP               exception-match
               98  POP_JUMP_IF_FALSE   146  'to 146'
              100  POP_TOP          
              102  STORE_FAST               'ldap_error'
              104  POP_TOP          
              106  SETUP_FINALLY       134  'to 134'

 L.  69       108  LOAD_FAST                'self'
              110  LOAD_ATTR                logger
              112  LOAD_METHOD              warning
              114  LOAD_STR                 'LDAPError searching %r: %s'
              116  LOAD_FAST                'expiry_filter'
              118  LOAD_FAST                'ldap_error'
              120  CALL_METHOD_3         3  ''
              122  POP_TOP          

 L.  70       124  POP_BLOCK        
              126  POP_EXCEPT       
              128  CALL_FINALLY        134  'to 134'
              130  LOAD_CONST               None
              132  RETURN_VALUE     
            134_0  COME_FROM           128  '128'
            134_1  COME_FROM_FINALLY   106  '106'
              134  LOAD_CONST               None
              136  STORE_FAST               'ldap_error'
              138  DELETE_FAST              'ldap_error'
              140  END_FINALLY      
              142  POP_EXCEPT       
              144  JUMP_FORWARD        148  'to 148'
            146_0  COME_FROM            98  '98'
              146  END_FINALLY      
            148_0  COME_FROM           144  '144'
            148_1  COME_FROM            88  '88'

 L.  72       148  LOAD_FAST                'self'
              150  LOAD_ATTR                ldap_conn
              152  LOAD_METHOD              results
              154  LOAD_FAST                'msg_id'
              156  CALL_METHOD_1         1  ''
              158  GET_ITER         
              160  FOR_ITER            384  'to 384'
              162  STORE_FAST               'ldap_res'

 L.  73       164  LOAD_FAST                'ldap_res'
              166  LOAD_ATTR                rdata
              168  GET_ITER         
              170  FOR_ITER            382  'to 382'
              172  STORE_FAST               'aeobj'

 L.  74       174  LOAD_FAST                'self'
              176  DUP_TOP          
              178  LOAD_ATTR                aeobject_counter
              180  LOAD_CONST               1
              182  INPLACE_ADD      
              184  ROT_TWO          
              186  STORE_ATTR               aeobject_counter

 L.  76       188  LOAD_GLOBAL              ldap0
              190  LOAD_ATTR                MOD_DELETE
              192  LOAD_CONST               b'aeStatus'
              194  LOAD_FAST                'aeobj'
              196  LOAD_ATTR                entry_as
              198  LOAD_STR                 'aeStatus'
              200  BINARY_SUBSCR    
              202  BUILD_TUPLE_3         3 

 L.  77       204  LOAD_GLOBAL              ldap0
              206  LOAD_ATTR                MOD_ADD
              208  LOAD_CONST               b'aeStatus'
              210  LOAD_FAST                'aeobj'
              212  LOAD_ATTR                entry_as
              214  LOAD_STR                 'aeExpiryStatus'
              216  BINARY_SUBSCR    
              218  BUILD_TUPLE_3         3 

 L.  75       220  BUILD_LIST_2          2 
              222  STORE_FAST               'modlist'

 L.  79       224  SETUP_FINALLY       278  'to 278'

 L.  80       226  LOAD_FAST                'self'
              228  LOAD_ATTR                ldap_conn
              230  LOAD_METHOD              modify_s

 L.  81       232  LOAD_FAST                'aeobj'
              234  LOAD_ATTR                dn_s

 L.  83       236  LOAD_GLOBAL              ldap0
              238  LOAD_ATTR                MOD_DELETE
              240  LOAD_CONST               b'aeStatus'
              242  LOAD_FAST                'aeobj'
              244  LOAD_ATTR                entry_as
              246  LOAD_STR                 'aeStatus'
              248  BINARY_SUBSCR    
              250  BUILD_TUPLE_3         3 

 L.  84       252  LOAD_GLOBAL              ldap0
              254  LOAD_ATTR                MOD_ADD
              256  LOAD_CONST               b'aeStatus'
              258  LOAD_FAST                'aeobj'
              260  LOAD_ATTR                entry_as
              262  LOAD_STR                 'aeExpiryStatus'
              264  BINARY_SUBSCR    
              266  BUILD_TUPLE_3         3 

 L.  82       268  BUILD_LIST_2          2 

 L.  80       270  CALL_METHOD_2         2  ''
              272  POP_TOP          
              274  POP_BLOCK        
              276  JUMP_FORWARD        348  'to 348'
            278_0  COME_FROM_FINALLY   224  '224'

 L.  87       278  DUP_TOP          
              280  LOAD_GLOBAL              ldap0
              282  LOAD_ATTR                LDAPError
              284  COMPARE_OP               exception-match
          286_288  POP_JUMP_IF_FALSE   346  'to 346'
              290  POP_TOP          
              292  STORE_FAST               'ldap_error'
              294  POP_TOP          
              296  SETUP_FINALLY       334  'to 334'

 L.  88       298  LOAD_FAST                'self'
              300  LOAD_ATTR                logger
              302  LOAD_METHOD              warning
              304  LOAD_STR                 'LDAPError modifying %r: %s'
              306  LOAD_FAST                'aeobj'
              308  LOAD_ATTR                dn_s
              310  LOAD_FAST                'ldap_error'
              312  CALL_METHOD_3         3  ''
              314  POP_TOP          

 L.  89       316  LOAD_FAST                'self'
              318  DUP_TOP          
              320  LOAD_ATTR                error_counter
              322  LOAD_CONST               1
              324  INPLACE_ADD      
              326  ROT_TWO          
              328  STORE_ATTR               error_counter
              330  POP_BLOCK        
              332  BEGIN_FINALLY    
            334_0  COME_FROM_FINALLY   296  '296'
              334  LOAD_CONST               None
              336  STORE_FAST               'ldap_error'
              338  DELETE_FAST              'ldap_error'
              340  END_FINALLY      
              342  POP_EXCEPT       
              344  JUMP_BACK           170  'to 170'
            346_0  COME_FROM           286  '286'
              346  END_FINALLY      
            348_0  COME_FROM           276  '276'

 L.  91       348  LOAD_FAST                'self'
              350  LOAD_ATTR                logger
              352  LOAD_METHOD              info
              354  LOAD_STR                 'Updated aeStatus in %r: %s'
              356  LOAD_FAST                'aeobj'
              358  LOAD_ATTR                dn_s
              360  LOAD_FAST                'modlist'
              362  CALL_METHOD_3         3  ''
              364  POP_TOP          

 L.  92       366  LOAD_FAST                'self'
              368  DUP_TOP          
              370  LOAD_ATTR                modify_counter
              372  LOAD_CONST               1
              374  INPLACE_ADD      
              376  ROT_TWO          
              378  STORE_ATTR               modify_counter
              380  JUMP_BACK           170  'to 170'
              382  JUMP_BACK           160  'to 160'

Parse error at or near `CALL_FINALLY' instruction at offset 128


def main--- This code section failed: ---

 L. 100         0  LOAD_GLOBAL              AEStatusUpdater
                2  CALL_FUNCTION_0       0  ''
                4  SETUP_WITH           24  'to 24'
                6  STORE_FAST               'ae_process'

 L. 101         8  LOAD_FAST                'ae_process'
               10  LOAD_ATTR                run
               12  LOAD_CONST               1
               14  LOAD_CONST               ('max_runs',)
               16  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               18  POP_TOP          
               20  POP_BLOCK        
               22  BEGIN_FINALLY    
             24_0  COME_FROM_WITH        4  '4'
               24  WITH_CLEANUP_START
               26  WITH_CLEANUP_FINISH
               28  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 22


if __name__ == '__main__':
    main()