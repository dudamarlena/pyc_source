# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /aedir_pproc/pwd/expwarn.py
# Compiled at: 2020-02-21 06:24:25
# Size of source mod 2**32: 8915 bytes
"""
aedir_pproc.pwd.expwarn - send password expiry warnings via e-mail
"""
import os, smtplib, time, email.utils, aedir.process, ldap0, ldap0.functions
from aedirpwd_cnf import APP_PATH_PREFIX, SMTP_DEBUGLEVEL, SMTP_FROM, SMTP_LOCALHOSTNAME, SMTP_TLS_CACERTS, SMTP_URL, TEMPLATES_DIRNAME, USER_MAIL_ENABLED, WEB_CTX_HOST
from ..__about__ import __version__, __author__, __license__
PWDPOLICY_FILTER = '(&(objectClass=pwdPolicy)(&(pwdMaxAge=*)(!(pwdMaxAge=0)))(pwdExpireWarning=*)(!(pwdAllowUserChange=FALSE)))'
PWD_EXPIRYWARN_FILTER_TMPL = '(&(objectClass=aeUser)(aeStatus=0)(uid=*)(displayName=*)(mail=*)(pwdPolicySubentry={pwdpolicy})(pwdChangedTime>={pwdchangedtime_ge})(pwdChangedTime<={pwdchangedtime_le}))'
FILTERSTR_USER = '(&(objectClass=aeUser)(aeStatus=0)(displayName=*)(mail=*))'
NOTIFY_OLDEST_TIMESPAN = 151200.0
PWD_EXPIRYWARN_MAIL_SUBJECT = 'Password of Æ-DIR account "{user_uid}" will expire soon!'
PWD_EXPIRYWARN_MAIL_TEMPLATE = os.path.join(TEMPLATES_DIRNAME, 'pwd_expiry_warning.txt')

class AEDIRPwdJob(aedir.process.AEProcess):
    __doc__ = '\n    Job instance\n    '
    script_version = __version__
    notify_oldest_timespan = NOTIFY_OLDEST_TIMESPAN
    user_attrs = [
     'objectClass',
     'uid',
     'cn',
     'displayName',
     'description',
     'mail',
     'creatorsName',
     'modifiersName']

    def __init__(self):
        aedir.process.AEProcess.__init__(self)
        self.notification_counter = 0
        self._smtp_conn = None

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

    def run_worker(self, state):
        """
        Run the job
        """
        last_run_timestr, current_run_timestr = self._get_time_strings()
        self._send_password_expiry_notifications(last_run_timestr, current_run_timestr)
        return current_run_timestr

    def _get_pwd_policy_entries(self):
        """
        Search all pwdPolicy entries with expiring passwords (pwdMaxAge set)
        """
        ldap_pwdpolicy_results = self.ldap_conn.search_s((self.ldap_conn.search_base),
          (ldap0.SCOPE_SUBTREE),
          filterstr=PWDPOLICY_FILTER,
          attrlist=[
         'cn',
         'pwdMaxAge',
         'pwdExpireWarning'])
        if not ldap_pwdpolicy_results:
            self.logger.error('No pwdPolicy entries found => nothing to do => abort')
        pwd_policy_list = [(res.dn_s, int(res.entry_s['pwdMaxAge'][0]), int(res.entry_s['pwdExpireWarning'][0])) for res in ldap_pwdpolicy_results]
        self.logger.debug('Found %d pwdPolicy entries: %s', len(pwd_policy_list), pwd_policy_list)
        return pwd_policy_list

    def _send_password_expiry_notifications--- This code section failed: ---

 L. 147         0  LOAD_GLOBAL              ldap0
                2  LOAD_ATTR                functions
                4  LOAD_METHOD              strp_secs
                6  LOAD_FAST                'current_run_timestr'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'current_time'

 L. 149        12  LOAD_FAST                'self'
               14  LOAD_METHOD              _get_pwd_policy_entries
               16  CALL_METHOD_0         0  ''
               18  STORE_FAST               'pwd_policy_list'

 L. 150        20  BUILD_LIST_0          0 
               22  STORE_FAST               'pwd_expire_warning_list'

 L. 152        24  LOAD_FAST                'pwd_policy_list'
               26  GET_ITER         
               28  FOR_ITER            280  'to 280'
               30  UNPACK_SEQUENCE_3     3 
               32  STORE_FAST               'pwd_policy'
               34  STORE_FAST               'pwd_max_age'
               36  STORE_FAST               'pwd_expire_warning'

 L. 154        38  LOAD_FAST                'pwd_policy'

 L. 155        40  LOAD_GLOBAL              ldap0
               42  LOAD_ATTR                functions
               44  LOAD_METHOD              strf_secs
               46  LOAD_FAST                'current_time'
               48  LOAD_FAST                'pwd_max_age'
               50  BINARY_SUBTRACT  
               52  CALL_METHOD_1         1  ''

 L. 156        54  LOAD_GLOBAL              ldap0
               56  LOAD_ATTR                functions
               58  LOAD_METHOD              strf_secs
               60  LOAD_FAST                'current_time'
               62  LOAD_FAST                'pwd_max_age'
               64  LOAD_FAST                'pwd_expire_warning'
               66  BINARY_SUBTRACT  
               68  BINARY_SUBTRACT  
               70  CALL_METHOD_1         1  ''

 L. 153        72  LOAD_CONST               ('pwdpolicy', 'pwdchangedtime_ge', 'pwdchangedtime_le')
               74  BUILD_CONST_KEY_MAP_3     3 
               76  STORE_FAST               'filterstr_inputs_dict'

 L. 158        78  LOAD_FAST                'self'
               80  LOAD_ATTR                logger
               82  LOAD_METHOD              debug
               84  LOAD_STR                 'filterstr_inputs_dict = %s'
               86  LOAD_FAST                'filterstr_inputs_dict'
               88  CALL_METHOD_2         2  ''
               90  POP_TOP          

 L. 160        92  LOAD_GLOBAL              PWD_EXPIRYWARN_FILTER_TMPL
               94  LOAD_ATTR                format
               96  BUILD_TUPLE_0         0 
               98  LOAD_FAST                'filterstr_inputs_dict'
              100  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              102  STORE_FAST               'pwd_expirywarn_filter'

 L. 162       104  LOAD_FAST                'self'
              106  LOAD_ATTR                logger
              108  LOAD_METHOD              debug

 L. 163       110  LOAD_STR                 'Search users for password expiry warning with %r'

 L. 164       112  LOAD_FAST                'pwd_expirywarn_filter'

 L. 162       114  CALL_METHOD_2         2  ''
              116  POP_TOP          

 L. 166       118  LOAD_FAST                'self'
              120  LOAD_ATTR                ldap_conn
              122  LOAD_ATTR                search_s

 L. 167       124  LOAD_FAST                'self'
              126  LOAD_ATTR                ldap_conn
              128  LOAD_ATTR                search_base

 L. 168       130  LOAD_GLOBAL              ldap0
              132  LOAD_ATTR                SCOPE_SUBTREE

 L. 169       134  LOAD_FAST                'pwd_expirywarn_filter'

 L. 170       136  LOAD_FAST                'self'
              138  LOAD_ATTR                user_attrs

 L. 166       140  LOAD_CONST               ('filterstr', 'attrlist')
              142  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              144  STORE_FAST               'ldap_results'

 L. 173       146  LOAD_FAST                'ldap_results'
              148  GET_ITER         
              150  FOR_ITER            278  'to 278'
              152  STORE_FAST               'res'

 L. 174       154  LOAD_FAST                'res'
              156  LOAD_ATTR                entry_s
              158  LOAD_STR                 'mail'
              160  BINARY_SUBSCR    
              162  LOAD_CONST               0
              164  BINARY_SUBSCR    
              166  STORE_FAST               'to_addr'

 L. 175       168  LOAD_FAST                'self'
              170  LOAD_ATTR                logger
              172  LOAD_METHOD              debug
              174  LOAD_STR                 'Prepare password expiry notification for %r sent to %r'
              176  LOAD_FAST                'res'
              178  LOAD_ATTR                dn_s
              180  LOAD_FAST                'to_addr'
              182  CALL_METHOD_3         3  ''
              184  POP_TOP          

 L. 176       186  LOAD_FAST                'pwd_expire_warning_list'
              188  LOAD_METHOD              append

 L. 177       190  LOAD_FAST                'res'
              192  LOAD_ATTR                entry_s
              194  LOAD_STR                 'uid'
              196  BINARY_SUBSCR    
              198  LOAD_CONST               0
              200  BINARY_SUBSCR    

 L. 178       202  LOAD_FAST                'res'
              204  LOAD_ATTR                entry_s
              206  LOAD_METHOD              get
              208  LOAD_STR                 'cn'
              210  LOAD_STR                 ''
              212  BUILD_LIST_1          1 
              214  CALL_METHOD_2         2  ''
              216  LOAD_CONST               0
              218  BINARY_SUBSCR    

 L. 179       220  LOAD_FAST                'res'
              222  LOAD_ATTR                entry_s
              224  LOAD_METHOD              get
              226  LOAD_STR                 'displayName'
              228  LOAD_STR                 ''
              230  BUILD_LIST_1          1 
              232  CALL_METHOD_2         2  ''
              234  LOAD_CONST               0
              236  BINARY_SUBSCR    

 L. 180       238  LOAD_FAST                'res'
              240  LOAD_ATTR                entry_s
              242  LOAD_METHOD              get
              244  LOAD_STR                 'description'
              246  LOAD_STR                 ''
              248  BUILD_LIST_1          1 
              250  CALL_METHOD_2         2  ''
              252  LOAD_CONST               0
              254  BINARY_SUBSCR    

 L. 181       256  LOAD_FAST                'to_addr'

 L. 182       258  LOAD_GLOBAL              SMTP_FROM

 L. 183       260  LOAD_FAST                'res'
              262  LOAD_ATTR                dn_s

 L. 184       264  LOAD_GLOBAL              WEB_CTX_HOST

 L. 185       266  LOAD_GLOBAL              APP_PATH_PREFIX

 L. 176       268  LOAD_CONST               ('user_uid', 'user_cn', 'user_displayname', 'user_description', 'emailaddr', 'fromaddr', 'user_dn', 'web_ctx_host', 'app_path_prefix')
              270  BUILD_CONST_KEY_MAP_9     9 
              272  CALL_METHOD_1         1  ''
              274  POP_TOP          
              276  JUMP_BACK           150  'to 150'
              278  JUMP_BACK            28  'to 28'

 L. 188       280  LOAD_FAST                'self'
              282  LOAD_ATTR                logger
              284  LOAD_METHOD              debug
              286  LOAD_STR                 'pwd_expire_warning_list = %s'
              288  LOAD_FAST                'pwd_expire_warning_list'
              290  CALL_METHOD_2         2  ''
              292  POP_TOP          

 L. 190       294  LOAD_FAST                'pwd_expire_warning_list'
          296_298  POP_JUMP_IF_TRUE    316  'to 316'

 L. 191       300  LOAD_FAST                'self'
              302  LOAD_ATTR                logger
              304  LOAD_METHOD              info
              306  LOAD_STR                 'No results => no password expiry notifications'
              308  CALL_METHOD_1         1  ''
              310  POP_TOP          
          312_314  JUMP_FORWARD        674  'to 674'
            316_0  COME_FROM           296  '296'

 L. 192       316  LOAD_GLOBAL              USER_MAIL_ENABLED
              318  LOAD_CONST               True
              320  COMPARE_OP               is-not
          322_324  POP_JUMP_IF_FALSE   366  'to 366'

 L. 193       326  LOAD_FAST                'self'
              328  LOAD_ATTR                logger
              330  LOAD_METHOD              info

 L. 194       332  LOAD_STR                 'Sending e-mails is disabled => Supressed %d password expiry notifications to %s'

 L. 195       334  LOAD_GLOBAL              len
              336  LOAD_FAST                'pwd_expire_warning_list'
              338  CALL_FUNCTION_1       1  ''

 L. 196       340  LOAD_STR                 ', '
              342  LOAD_METHOD              join
              344  LOAD_LISTCOMP            '<code_object <listcomp>>'
              346  LOAD_STR                 'AEDIRPwdJob._send_password_expiry_notifications.<locals>.<listcomp>'
              348  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              350  LOAD_FAST                'pwd_expire_warning_list'
              352  GET_ITER         
              354  CALL_FUNCTION_1       1  ''
              356  CALL_METHOD_1         1  ''

 L. 193       358  CALL_METHOD_3         3  ''
              360  POP_TOP          
          362_364  JUMP_FORWARD        674  'to 674'
            366_0  COME_FROM           322  '322'

 L. 200       366  LOAD_GLOBAL              open
              368  LOAD_GLOBAL              PWD_EXPIRYWARN_MAIL_TEMPLATE
              370  LOAD_STR                 'r'
              372  LOAD_STR                 'utf-8'
              374  LOAD_CONST               ('encoding',)
              376  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              378  SETUP_WITH          394  'to 394'
              380  STORE_FAST               'template_file'

 L. 201       382  LOAD_FAST                'template_file'
              384  LOAD_METHOD              read
              386  CALL_METHOD_0         0  ''
              388  STORE_FAST               'smtp_message_tmpl'
              390  POP_BLOCK        
              392  BEGIN_FINALLY    
            394_0  COME_FROM_WITH      378  '378'
              394  WITH_CLEANUP_START
              396  WITH_CLEANUP_FINISH
              398  END_FINALLY      

 L. 203       400  LOAD_FAST                'self'
              402  LOAD_ATTR                smtp_connection

 L. 204       404  LOAD_GLOBAL              SMTP_URL

 L. 205       406  LOAD_GLOBAL              SMTP_LOCALHOSTNAME

 L. 206       408  LOAD_GLOBAL              SMTP_TLS_CACERTS

 L. 207       410  LOAD_GLOBAL              SMTP_DEBUGLEVEL

 L. 203       412  LOAD_CONST               ('local_hostname', 'ca_certs', 'debug_level')
              414  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              416  SETUP_WITH          668  'to 668'

 L. 208       418  STORE_FAST               'smtp_conn'

 L. 209       420  BUILD_LIST_0          0 
              422  STORE_FAST               'notified_users'

 L. 210       424  LOAD_FAST                'pwd_expire_warning_list'
              426  GET_ITER         
              428  FOR_ITER            638  'to 638'
              430  STORE_FAST               'user_data'

 L. 211       432  LOAD_FAST                'user_data'
              434  LOAD_STR                 'emailaddr'
              436  BINARY_SUBSCR    
              438  STORE_FAST               'to_addr'

 L. 212       440  LOAD_FAST                'smtp_message_tmpl'
              442  LOAD_ATTR                format
              444  BUILD_TUPLE_0         0 
              446  LOAD_FAST                'user_data'
              448  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              450  STORE_FAST               'smtp_message'

 L. 213       452  LOAD_GLOBAL              PWD_EXPIRYWARN_MAIL_SUBJECT
              454  LOAD_ATTR                format
              456  BUILD_TUPLE_0         0 
              458  LOAD_FAST                'user_data'
              460  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              462  STORE_FAST               'smtp_subject'

 L. 214       464  LOAD_FAST                'self'
              466  LOAD_ATTR                logger
              468  LOAD_METHOD              debug
              470  LOAD_STR                 'smtp_subject = %r'
              472  LOAD_FAST                'smtp_subject'
              474  CALL_METHOD_2         2  ''
              476  POP_TOP          

 L. 215       478  LOAD_FAST                'self'
              480  LOAD_ATTR                logger
              482  LOAD_METHOD              debug
              484  LOAD_STR                 'smtp_message = %r'
              486  LOAD_FAST                'smtp_message'
              488  CALL_METHOD_2         2  ''
              490  POP_TOP          

 L. 216       492  SETUP_FINALLY       556  'to 556'

 L. 217       494  LOAD_FAST                'smtp_conn'
              496  LOAD_METHOD              send_simple_message

 L. 218       498  LOAD_GLOBAL              SMTP_FROM

 L. 219       500  LOAD_FAST                'to_addr'
              502  BUILD_LIST_1          1 

 L. 220       504  LOAD_STR                 'utf-8'

 L. 222       506  LOAD_STR                 'From'
              508  LOAD_GLOBAL              SMTP_FROM
              510  BUILD_TUPLE_2         2 

 L. 223       512  LOAD_STR                 'Date'
              514  LOAD_GLOBAL              email
              516  LOAD_ATTR                utils
              518  LOAD_METHOD              formatdate
              520  LOAD_GLOBAL              time
              522  LOAD_METHOD              time
              524  CALL_METHOD_0         0  ''
              526  LOAD_CONST               True
              528  CALL_METHOD_2         2  ''
              530  BUILD_TUPLE_2         2 

 L. 224       532  LOAD_STR                 'Subject'
              534  LOAD_FAST                'smtp_subject'
              536  BUILD_TUPLE_2         2 

 L. 225       538  LOAD_STR                 'To'
              540  LOAD_FAST                'to_addr'
              542  BUILD_TUPLE_2         2 

 L. 221       544  BUILD_TUPLE_4         4 

 L. 227       546  LOAD_FAST                'smtp_message'

 L. 217       548  CALL_METHOD_5         5  ''
              550  POP_TOP          
              552  POP_BLOCK        
              554  JUMP_FORWARD        620  'to 620'
            556_0  COME_FROM_FINALLY   492  '492'

 L. 229       556  DUP_TOP          
              558  LOAD_GLOBAL              smtplib
              560  LOAD_ATTR                SMTPRecipientsRefused
              562  COMPARE_OP               exception-match
          564_566  POP_JUMP_IF_FALSE   618  'to 618'
              568  POP_TOP          
              570  STORE_FAST               'smtp_err'
              572  POP_TOP          
              574  SETUP_FINALLY       606  'to 606'

 L. 230       576  LOAD_FAST                'self'
              578  LOAD_ATTR                logger
              580  LOAD_METHOD              error
              582  LOAD_STR                 'Recipient %r rejected: %s'
              584  LOAD_FAST                'to_addr'
              586  LOAD_FAST                'smtp_err'
              588  CALL_METHOD_3         3  ''
              590  POP_TOP          

 L. 231       592  POP_BLOCK        
              594  POP_EXCEPT       
              596  CALL_FINALLY        606  'to 606'
          598_600  JUMP_BACK           428  'to 428'
              602  POP_BLOCK        
              604  BEGIN_FINALLY    
            606_0  COME_FROM           596  '596'
            606_1  COME_FROM_FINALLY   574  '574'
              606  LOAD_CONST               None
              608  STORE_FAST               'smtp_err'
              610  DELETE_FAST              'smtp_err'
              612  END_FINALLY      
              614  POP_EXCEPT       
              616  JUMP_BACK           428  'to 428'
            618_0  COME_FROM           564  '564'
              618  END_FINALLY      
            620_0  COME_FROM           554  '554'

 L. 233       620  LOAD_FAST                'notified_users'
              622  LOAD_METHOD              append
              624  LOAD_FAST                'user_data'
              626  LOAD_STR                 'user_uid'
              628  BINARY_SUBSCR    
              630  CALL_METHOD_1         1  ''
              632  POP_TOP          
          634_636  JUMP_BACK           428  'to 428'

 L. 234       638  LOAD_FAST                'self'
              640  LOAD_ATTR                logger
              642  LOAD_METHOD              info

 L. 235       644  LOAD_STR                 'Sent %d password expiry notifications: %s'

 L. 236       646  LOAD_GLOBAL              len
              648  LOAD_FAST                'notified_users'
              650  CALL_FUNCTION_1       1  ''

 L. 237       652  LOAD_STR                 ', '
              654  LOAD_METHOD              join
              656  LOAD_FAST                'notified_users'
              658  CALL_METHOD_1         1  ''

 L. 234       660  CALL_METHOD_3         3  ''
              662  POP_TOP          
              664  POP_BLOCK        
              666  BEGIN_FINALLY    
            668_0  COME_FROM_WITH      416  '416'
              668  WITH_CLEANUP_START
              670  WITH_CLEANUP_FINISH
              672  END_FINALLY      
            674_0  COME_FROM           362  '362'
            674_1  COME_FROM           312  '312'

Parse error at or near `CALL_FINALLY' instruction at offset 596


def main():
    """
    run the process
    """
    with AEDIRPwdJob() as (ae_process):
        ae_process.run(max_runs=1)


if __name__ == '__main__':
    main()