# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /aedir_pproc/welcome.py
# Compiled at: 2020-02-05 13:00:28
# Size of source mod 2**32: 8197 bytes
__doc__ = '\naedir_pproc.welcome -- Send welcome e-mail to new users which have not set a password yet\n'
import sys, os, time, smtplib, email.utils
from socket import getfqdn
import mailutil, ldap0, ldap0.functions, mailutil, aedir.process
from .__about__ import __version__, __author__, __license__
from aedirpwd_cnf import APP_PATH_PREFIX, FILTERSTR_NO_WELCOME_YET, FILTERSTR_USER, NOTIFY_EMAIL_SUBJECT, NOTIFY_EMAIL_TEMPLATE, NOTIFY_OLDEST_TIMESPAN, NOTIFY_SUCCESSFUL_MOD, PWD_LDAP_URL, SERVER_ID, SMTP_DEBUGLEVEL, SMTP_FROM, SMTP_LOCALHOSTNAME, SMTP_TLS_CACERTS, SMTP_URL, WEB_CTX_HOST

class AEDIRWelcomeMailJob(aedir.process.AEProcess):
    """AEDIRWelcomeMailJob"""
    script_version = __version__
    ldap_url = PWD_LDAP_URL
    notify_oldest_timespan = NOTIFY_OLDEST_TIMESPAN
    user_attrs = [
     'objectClass',
     'uid',
     'cn',
     'displayName',
     'description',
     'mail',
     'creatorsName']
    admin_attrs = [
     'objectClass',
     'uid',
     'cn',
     'mail']

    def __init__(self, server_id):
        aedir.process.AEProcess.__init__(self)
        self.host_fqdn = getfqdn()
        self.server_id = server_id
        self._smtp_conn = None
        self.logger.debug('running on %r with (serverID %r)', self.host_fqdn, self.server_id)

    def _get_time_strings(self):
        """
        Determine
        1. oldest possible last timestamp (sounds strange, yeah!)
        2. and current time
        """
        current_time = time.time()
        return (
         ldap0.functions.strf_secs(current_time - self.notify_oldest_timespan),
         ldap0.functions.strf_secs(current_time))

    def _send_welcome_message(self, smtp_conn, to_addr, smtp_message_tmpl, msg_attrs):
        """
        Send single welcome message for a user
        """
        self.logger.debug('msg_attrs = %r', msg_attrs)
        smtp_message = (smtp_message_tmpl.format)(**msg_attrs)
        smtp_subject = (NOTIFY_EMAIL_SUBJECT.format)(**msg_attrs)
        self.logger.debug('smtp_subject = %r', smtp_subject)
        self.logger.debug('smtp_message = %r', smtp_message)
        try:
            smtp_conn.send_simple_message(SMTP_FROM, [
             to_addr], 'utf-8', (
             (
              'From', SMTP_FROM),
             (
              'Date', email.utils.formatdate(time.time(), True)),
             (
              'Subject', smtp_subject),
             (
              'To', to_addr)), smtp_message)
        except smtplib.SMTPRecipientsRefused as smtp_error:
            try:
                self.logger.error('Recipient %r rejected: %s', to_addr, smtp_error)
            finally:
                smtp_error = None
                del smtp_error

        else:
            self.logger.info('Sent welcome notification for user %r to %r', msg_attrs['user_displayname'], to_addr)

    def _welcome_notifications--- This code section failed: ---

 L. 135         0  LOAD_GLOBAL              FILTERSTR_NO_WELCOME_YET
                2  LOAD_ATTR                format

 L. 136         4  LOAD_FAST                'current_run_timestr'

 L. 137         6  LOAD_FAST                'last_run_timestr'

 L. 138         8  LOAD_FAST                'self'
               10  LOAD_ATTR                server_id

 L. 135        12  LOAD_CONST               ('currenttime', 'lasttime', 'serverid')
               14  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'

 L. 134        16  STORE_FAST               'nopassword_filterstr'

 L. 141        18  LOAD_FAST                'self'
               20  LOAD_ATTR                logger
               22  LOAD_METHOD              debug

 L. 142        24  LOAD_STR                 'User search filter: %r'

 L. 143        26  LOAD_FAST                'nopassword_filterstr'

 L. 141        28  CALL_METHOD_2         2  ''
               30  POP_TOP          

 L. 145        32  LOAD_FAST                'self'
               34  LOAD_ATTR                ldap_conn
               36  LOAD_ATTR                search_s

 L. 146        38  LOAD_FAST                'self'
               40  LOAD_ATTR                ldap_conn
               42  LOAD_ATTR                search_base

 L. 147        44  LOAD_GLOBAL              ldap0
               46  LOAD_ATTR                SCOPE_SUBTREE

 L. 148        48  LOAD_FAST                'nopassword_filterstr'

 L. 149        50  LOAD_FAST                'self'
               52  LOAD_ATTR                user_attrs

 L. 145        54  LOAD_CONST               ('filterstr', 'attrlist')
               56  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               58  STORE_FAST               'ldap_results'

 L. 151        60  LOAD_FAST                'ldap_results'
               62  POP_JUMP_IF_TRUE     80  'to 80'

 L. 152        64  LOAD_FAST                'self'
               66  LOAD_ATTR                logger
               68  LOAD_METHOD              debug
               70  LOAD_STR                 'No results => no notifications'
               72  CALL_METHOD_1         1  ''
               74  POP_TOP          

 L. 153        76  LOAD_CONST               None
               78  RETURN_VALUE     
             80_0  COME_FROM            62  '62'

 L. 155        80  LOAD_CONST               0
               82  STORE_FAST               'notification_counter'

 L. 157        84  LOAD_GLOBAL              open
               86  LOAD_GLOBAL              NOTIFY_EMAIL_TEMPLATE
               88  LOAD_STR                 'r'
               90  LOAD_STR                 'utf-8'
               92  LOAD_CONST               ('encoding',)
               94  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               96  SETUP_WITH          112  'to 112'
               98  STORE_FAST               'tfile'

 L. 158       100  LOAD_FAST                'tfile'
              102  LOAD_METHOD              read
              104  CALL_METHOD_0         0  ''
              106  STORE_FAST               'smtp_message_tmpl'
              108  POP_BLOCK        
              110  BEGIN_FINALLY    
            112_0  COME_FROM_WITH       96  '96'
              112  WITH_CLEANUP_START
              114  WITH_CLEANUP_FINISH
              116  END_FINALLY      

 L. 160       118  LOAD_FAST                'self'
              120  LOAD_ATTR                smtp_connection

 L. 161       122  LOAD_GLOBAL              SMTP_URL

 L. 162       124  LOAD_GLOBAL              SMTP_LOCALHOSTNAME

 L. 163       126  LOAD_GLOBAL              SMTP_TLS_CACERTS

 L. 164       128  LOAD_GLOBAL              SMTP_DEBUGLEVEL

 L. 160       130  LOAD_CONST               ('local_hostname', 'ca_certs', 'debug_level')
              132  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
          134_136  SETUP_WITH          556  'to 556'

 L. 165       138  STORE_FAST               'smtp_conn'

 L. 167       140  LOAD_FAST                'ldap_results'
              142  GET_ITER         
            144_0  COME_FROM           532  '532'
          144_146  FOR_ITER            552  'to 552'
              148  STORE_FAST               'ldap_res'

 L. 168       150  LOAD_FAST                'ldap_res'
              152  LOAD_ATTR                entry_s
              154  LOAD_STR                 'mail'
              156  BINARY_SUBSCR    
              158  LOAD_CONST               0
              160  BINARY_SUBSCR    
              162  STORE_FAST               'to_addr'

 L. 169       164  LOAD_FAST                'self'
              166  LOAD_ATTR                logger
              168  LOAD_METHOD              debug

 L. 170       170  LOAD_STR                 'Prepare welcome notification for %r sent to %r'

 L. 171       172  LOAD_FAST                'ldap_res'
              174  LOAD_ATTR                dn_s

 L. 172       176  LOAD_FAST                'to_addr'

 L. 169       178  CALL_METHOD_3         3  ''
              180  POP_TOP          

 L. 175       182  LOAD_GLOBAL              str
              184  LOAD_FAST                'self'
              186  LOAD_ATTR                ldap_conn
              188  LOAD_ATTR                ldap_url_obj
              190  LOAD_METHOD              connect_uri
              192  CALL_METHOD_0         0  ''
              194  CALL_FUNCTION_1       1  ''

 L. 176       196  LOAD_FAST                'ldap_res'
              198  LOAD_ATTR                entry_s
              200  LOAD_STR                 'uid'
              202  BINARY_SUBSCR    
              204  LOAD_CONST               0
              206  BINARY_SUBSCR    

 L. 177       208  LOAD_FAST                'ldap_res'
              210  LOAD_ATTR                entry_s
              212  LOAD_METHOD              get
              214  LOAD_STR                 'cn'
              216  LOAD_STR                 ''
              218  BUILD_LIST_1          1 
              220  CALL_METHOD_2         2  ''
              222  LOAD_CONST               0
              224  BINARY_SUBSCR    

 L. 178       226  LOAD_FAST                'ldap_res'
              228  LOAD_ATTR                entry_s
              230  LOAD_METHOD              get
              232  LOAD_STR                 'displayName'
              234  LOAD_STR                 ''
              236  BUILD_LIST_1          1 
              238  CALL_METHOD_2         2  ''
              240  LOAD_CONST               0
              242  BINARY_SUBSCR    

 L. 179       244  LOAD_FAST                'ldap_res'
              246  LOAD_ATTR                entry_s
              248  LOAD_METHOD              get
              250  LOAD_STR                 'description'
              252  LOAD_STR                 ''
              254  BUILD_LIST_1          1 
              256  CALL_METHOD_2         2  ''
              258  LOAD_CONST               0
              260  BINARY_SUBSCR    

 L. 180       262  LOAD_FAST                'to_addr'

 L. 181       264  LOAD_GLOBAL              SMTP_FROM

 L. 182       266  LOAD_FAST                'ldap_res'
              268  LOAD_ATTR                dn_s

 L. 183       270  LOAD_GLOBAL              WEB_CTX_HOST
          272_274  JUMP_IF_TRUE_OR_POP   280  'to 280'
              276  LOAD_FAST                'self'
              278  LOAD_ATTR                host_fqdn
            280_0  COME_FROM           272  '272'

 L. 184       280  LOAD_GLOBAL              APP_PATH_PREFIX

 L. 185       282  LOAD_STR                 'unknown'

 L. 186       284  LOAD_STR                 'unknown'

 L. 174       286  LOAD_CONST               ('ldap_uri', 'user_uid', 'user_cn', 'user_displayname', 'user_description', 'emailadr', 'fromaddr', 'user_dn', 'web_ctx_host', 'app_path_prefix', 'admin_cn', 'admin_mail')
              288  BUILD_CONST_KEY_MAP_12    12 
              290  STORE_FAST               'msg_attrs'

 L. 188       292  LOAD_FAST                'ldap_res'
              294  LOAD_ATTR                entry_s
              296  LOAD_STR                 'creatorsName'
              298  BINARY_SUBSCR    
              300  LOAD_CONST               0
              302  BINARY_SUBSCR    
              304  STORE_FAST               'admin_dn'

 L. 189       306  SETUP_FINALLY       332  'to 332'

 L. 190       308  LOAD_FAST                'self'
              310  LOAD_ATTR                ldap_conn
              312  LOAD_ATTR                read_s

 L. 191       314  LOAD_FAST                'admin_dn'

 L. 192       316  LOAD_GLOBAL              FILTERSTR_USER

 L. 193       318  LOAD_FAST                'self'
              320  LOAD_ATTR                admin_attrs

 L. 190       322  LOAD_CONST               ('filterstr', 'attrlist')
              324  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              326  STORE_FAST               'admin_res'
              328  POP_BLOCK        
              330  JUMP_FORWARD        400  'to 400'
            332_0  COME_FROM_FINALLY   306  '306'

 L. 195       332  DUP_TOP          
              334  LOAD_GLOBAL              ldap0
              336  LOAD_ATTR                NO_SUCH_OBJECT
              338  LOAD_GLOBAL              ldap0
              340  LOAD_ATTR                INSUFFICIENT_ACCESS
              342  BUILD_TUPLE_2         2 
              344  COMPARE_OP               exception-match
          346_348  POP_JUMP_IF_FALSE   398  'to 398'
              350  POP_TOP          
              352  STORE_FAST               'ldap_err'
              354  POP_TOP          
              356  SETUP_FINALLY       386  'to 386'

 L. 196       358  LOAD_FAST                'self'
              360  LOAD_ATTR                logger
              362  LOAD_METHOD              warning

 L. 197       364  LOAD_STR                 'Error reading admin entry %r referenced by %r: %s'

 L. 198       366  LOAD_FAST                'admin_dn'

 L. 199       368  LOAD_FAST                'ldap_res'
              370  LOAD_ATTR                dn_s

 L. 200       372  LOAD_FAST                'ldap_err'

 L. 196       374  CALL_METHOD_4         4  ''
              376  POP_TOP          

 L. 202       378  BUILD_MAP_0           0 
              380  STORE_FAST               'admin_entry'
              382  POP_BLOCK        
              384  BEGIN_FINALLY    
            386_0  COME_FROM_FINALLY   356  '356'
              386  LOAD_CONST               None
              388  STORE_FAST               'ldap_err'
              390  DELETE_FAST              'ldap_err'
              392  END_FINALLY      
              394  POP_EXCEPT       
              396  JUMP_FORWARD        506  'to 506'
            398_0  COME_FROM           346  '346'
              398  END_FINALLY      
            400_0  COME_FROM           330  '330'

 L. 204       400  LOAD_FAST                'admin_res'
              402  LOAD_CONST               None
              404  COMPARE_OP               is
          406_408  POP_JUMP_IF_FALSE   430  'to 430'

 L. 205       410  LOAD_FAST                'self'
              412  LOAD_ATTR                logger
              414  LOAD_METHOD              warning

 L. 206       416  LOAD_STR                 'Empty result reading admin entry %r referenced by %r'

 L. 207       418  LOAD_FAST                'admin_dn'

 L. 208       420  LOAD_FAST                'ldap_res'
              422  LOAD_ATTR                dn_s

 L. 205       424  CALL_METHOD_3         3  ''
              426  POP_TOP          
              428  JUMP_FORWARD        506  'to 506'
            430_0  COME_FROM           406  '406'

 L. 211       430  LOAD_FAST                'self'
              432  LOAD_ATTR                logger
              434  LOAD_METHOD              debug

 L. 212       436  LOAD_STR                 'Read admin entry %r: %r'

 L. 213       438  LOAD_FAST                'admin_dn'

 L. 214       440  LOAD_FAST                'admin_res'
              442  LOAD_ATTR                entry_s

 L. 211       444  CALL_METHOD_3         3  ''
              446  POP_TOP          

 L. 216       448  LOAD_FAST                'admin_res'
              450  LOAD_CONST               None
              452  COMPARE_OP               is-not
          454_456  POP_JUMP_IF_FALSE   506  'to 506'

 L. 217       458  LOAD_FAST                'admin_res'
              460  LOAD_ATTR                entry_s
              462  LOAD_METHOD              get
              464  LOAD_STR                 'cn'
              466  LOAD_STR                 'unknown'
              468  BUILD_LIST_1          1 
              470  CALL_METHOD_2         2  ''
              472  LOAD_CONST               0
              474  BINARY_SUBSCR    
              476  LOAD_FAST                'msg_attrs'
              478  LOAD_STR                 'admin_cn'
              480  STORE_SUBSCR     

 L. 218       482  LOAD_FAST                'admin_res'
              484  LOAD_ATTR                entry_s
              486  LOAD_METHOD              get
              488  LOAD_STR                 'mail'
              490  LOAD_STR                 'unknown'
              492  BUILD_LIST_1          1 
              494  CALL_METHOD_2         2  ''
              496  LOAD_CONST               0
              498  BINARY_SUBSCR    
              500  LOAD_FAST                'msg_attrs'
              502  LOAD_STR                 'admin_mail'
              504  STORE_SUBSCR     
            506_0  COME_FROM           454  '454'
            506_1  COME_FROM           428  '428'
            506_2  COME_FROM           396  '396'

 L. 219       506  LOAD_FAST                'self'
              508  LOAD_METHOD              _send_welcome_message
              510  LOAD_FAST                'smtp_conn'
              512  LOAD_FAST                'to_addr'
              514  LOAD_FAST                'smtp_message_tmpl'
              516  LOAD_FAST                'msg_attrs'
              518  CALL_METHOD_4         4  ''
              520  POP_TOP          

 L. 220       522  LOAD_FAST                'notification_counter'
              524  LOAD_CONST               1
              526  INPLACE_ADD      
              528  STORE_FAST               'notification_counter'

 L. 221       530  LOAD_GLOBAL              NOTIFY_SUCCESSFUL_MOD
              532  POP_JUMP_IF_FALSE   144  'to 144'

 L. 222       534  LOAD_FAST                'self'
              536  LOAD_ATTR                ldap_conn
              538  LOAD_METHOD              modify_s
              540  LOAD_FAST                'ldap_res'
              542  LOAD_ATTR                dn_s
              544  LOAD_GLOBAL              NOTIFY_SUCCESSFUL_MOD
              546  CALL_METHOD_2         2  ''
              548  POP_TOP          
              550  JUMP_BACK           144  'to 144'
              552  POP_BLOCK        
              554  BEGIN_FINALLY    
            556_0  COME_FROM_WITH      134  '134'
              556  WITH_CLEANUP_START
              558  WITH_CLEANUP_FINISH
              560  END_FINALLY      

 L. 224       562  LOAD_FAST                'notification_counter'
          564_566  POP_JUMP_IF_FALSE   582  'to 582'

 L. 225       568  LOAD_FAST                'self'
              570  LOAD_ATTR                logger
              572  LOAD_METHOD              info
              574  LOAD_STR                 'Sent %d welcome notifications'
              576  LOAD_FAST                'notification_counter'
              578  CALL_METHOD_2         2  ''
              580  POP_TOP          
            582_0  COME_FROM           564  '564'

Parse error at or near `BEGIN_FINALLY' instruction at offset 110

    def run_worker(self, state):
        """
        Run the job
        """
        last_run_timestr, current_run_timestr = self._get_time_strings()
        self._welcome_notifications(last_run_timestr, current_run_timestr)
        return current_run_timestr


def main--- This code section failed: ---

 L. 242         0  LOAD_GLOBAL              AEDIRWelcomeMailJob
                2  LOAD_GLOBAL              SERVER_ID
                4  CALL_FUNCTION_1       1  ''
                6  SETUP_WITH           26  'to 26'
                8  STORE_FAST               'ae_process'

 L. 243        10  LOAD_FAST                'ae_process'
               12  LOAD_ATTR                run
               14  LOAD_CONST               1
               16  LOAD_CONST               ('max_runs',)
               18  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               20  POP_TOP          
               22  POP_BLOCK        
               24  BEGIN_FINALLY    
             26_0  COME_FROM_WITH        6  '6'
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 24


if __name__ == '__main__':
    main()