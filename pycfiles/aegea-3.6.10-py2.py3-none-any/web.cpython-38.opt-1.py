# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /aedir_pproc/pwd/web.py
# Compiled at: 2020-02-05 09:17:24
# Size of source mod 2**32: 33996 bytes
__doc__ = '\naedir_pproc.pwd.web - AE-DIR password self-service web application\n'
import re, sys, os, time, socket, smtplib, hashlib, logging
import urllib.parse as url_quote_plus
import email.utils, web, ldap0, ldap0.functions, ldap0.filter
from ldap0.err import PasswordPolicyException, PasswordPolicyExpirationWarning
from ldap0.controls.ppolicy import PasswordPolicyControl
from ldap0.controls.sessiontrack import SessionTrackingControl
from ldap0.controls.sessiontrack import SESSION_TRACKING_FORMAT_OID_USERNAME
from ldap0.controls.deref import DereferenceControl
from ldap0.pw import random_string
import mailutil, aedir
from aedirpwd_cnf import PWD_LDAP_URL, WEB_CONFIG_DEBUG, WEB_ERROR, APP_PATH_PREFIX, LAYOUT, TEMPLATES_DIRNAME, EMAIL_SUBJECT_ADMIN, EMAIL_SUBJECT_PERSONAL, EMAIL_TEMPLATE_ADMIN, EMAIL_TEMPLATE_PERSONAL, TIME_DISPLAY_FORMAT, FILTERSTR_CHANGEPW, FILTERSTR_REQUESTPW, FILTERSTR_RESETPW, PWD_ADMIN_LEN, PWD_ADMIN_MAILTO, PWD_EXPIRETIMESPAN, PWD_LENGTH, PWD_RESET_ENABLED, PWD_TMP_CHARS, PWD_TMP_HASH_ALGO, SMTP_DEBUGLEVEL, SMTP_FROM, SMTP_LOCALHOSTNAME, SMTP_TLS_CACERTS, SMTP_URL
from ..__about__ import __version__
USER_ATTRS = [
 'objectClass',
 'uid',
 'cn',
 'mail',
 'displayName',
 'pwdChangedTime',
 'pwdPolicySubentry']
PWDPOLICY_EXPIRY_ATTRS = [
 'pwdMaxAge',
 'pwdExpireWarning']
MSPWDRESETPOLICY_ATTRS = [
 'msPwdResetAdminPwLen',
 'msPwdResetEnabled',
 'msPwdResetHashAlgorithm',
 'msPwdResetMaxAge',
 'msPwdResetPwLen']
PWDPOLICY_DEREF_CONTROL = DereferenceControl(True, {'pwdPolicySubentry': [
                       'pwdAllowUserChange',
                       'pwdAttribute',
                       'pwdMinAge',
                       'pwdMinLength'] + PWDPOLICY_EXPIRY_ATTRS + MSPWDRESETPOLICY_ATTRS})
APP_LOGGER = aedir.init_logger(log_name='ae-dir-pwd')
URL2CLASS_MAPPING = ('/', 'Default', '/checkpw', 'CheckPassword', '/changepw', 'ChangePassword',
                     '/requestpw', 'RequestPasswordReset', '/resetpw', 'FinishPasswordReset')
HASH_OID2NAME = {'1.2.840.113549.2.5':'md5', 
 '1.3.14.3.2.26':'sha1', 
 '2.16.840.1.101.3.4.2.4':'sha224', 
 '2.16.840.1.101.3.4.2.1':'sha256', 
 '2.16.840.1.101.3.4.2.2':'sha384', 
 '2.16.840.1.101.3.4.2.3':'sha512'}

def pwd_hash(pw_clear, hash_algo_oid):
    """
    Generate un-salted hash as hex-digest
    """
    return hashlib.new(HASH_OID2NAME[hash_algo_oid], pw_clear.encode('utf-8')).hexdigest()


def read_template_file--- This code section failed: ---

 L. 126         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'filename'
                4  LOAD_STR                 'rb'
                6  CALL_FUNCTION_2       2  ''
                8  SETUP_WITH           30  'to 30'
               10  STORE_FAST               'file_obj'

 L. 127        12  LOAD_FAST                'file_obj'
               14  LOAD_METHOD              read
               16  CALL_METHOD_0         0  ''
               18  LOAD_METHOD              decode
               20  LOAD_STR                 'utf-8'
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'file_content'
               26  POP_BLOCK        
               28  BEGIN_FINALLY    
             30_0  COME_FROM_WITH        8  '8'
               30  WITH_CLEANUP_START
               32  WITH_CLEANUP_FINISH
               34  END_FINALLY      

 L. 128        36  LOAD_FAST                'file_content'
               38  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `BEGIN_FINALLY' instruction at offset 28


RENDER = web.template.render(TEMPLATES_DIRNAME, base=LAYOUT)
if PWD_TMP_CHARS != url_quote_plus(PWD_TMP_CHARS):
    raise ValueError('URL special chars in PWD_TMP_CHARS: %r' % PWD_TMP_CHARS)
if not WEB_CONFIG_DEBUG:
    web.config.debug = False
USERNAME_FIELD = web.form.Textbox('username',
  (web.form.notnull),
  (web.form.regexp('^[a-zA-Z0-9._-]+$', 'Invalid user name.')),
  description='User name:')
EMAIL_FIELD = web.form.Textbox('email',
  (web.form.notnull),
  (web.form.regexp('^[a-zA-Z0-9@.+=/_ -]+@[a-zA-Z0-9-]+(\\.[a-zA-Z0-9-]+)*$', 'Invalid e-mail address.')),
  description='E-mail address:')
USERPASSWORD_FIELD = web.form.Password('oldpassword',
  (web.form.notnull),
  (web.form.regexp('^.*$', '')),
  description='Old password')
TEMP1PASSWORD_FIELD = web.form.Password('temppassword1',
  (web.form.notnull),
  (web.form.regexp('^[%s]+$' % (re.escape(PWD_TMP_CHARS),), 'Invalid input format.')),
  description='Temporary password part #1')
TEMP2PASSWORD_FIELD = web.form.Password('temppassword2',
  (web.form.regexp('^[%s]*$' % (re.escape(PWD_TMP_CHARS),), 'Invalid input format.')),
  description='Temporary password part #2')
VALID_NEWPASSWORD_REGEXP = web.form.regexp('^.+$', 'Passwort rules violated!')
NEWPASSWORD1_FIELD = web.form.Password('newpassword1',
  (web.form.notnull),
  VALID_NEWPASSWORD_REGEXP,
  description='New password')
NEWPASSWORD2_FIELD = web.form.Password('newpassword2',
  (web.form.notnull),
  VALID_NEWPASSWORD_REGEXP,
  description='New password (repeat)')

class RequestLogAdaptor(logging.LoggerAdapter):
    """RequestLogAdaptor"""

    def process(self, msg, kwargs):
        return (
         'IP=%s CLASS=%s REQID=%d - %s' % (
          self.extra['remote_ip'],
          self.extra['req_class'],
          self.extra['req_id'],
          msg),
         kwargs)


class Default:
    """Default"""
    ldap_url = aedir.AEDirUrl(PWD_LDAP_URL)

    def __init__(self):
        self.remote_ip = web.ctx.env.get('FORWARDED_FOR', web.ctx.env.get('HTTP_X_FORWARDED_FOR', web.ctx.ip))
        self.logger = RequestLogAdaptor(APP_LOGGER, {'remote_ip':self.remote_ip, 
         'req_class':'.'.join((self.__class__.__module__, self.__class__.__name__)), 
         'req_id':id(self)})
        self.logger.debug('%s request from %s (via %s)', web.ctx.env['REQUEST_METHOD'], self.remote_ip, web.ctx.ip)
        self._add_headers()
        self.ldap_conn = None
        self.form = None

    @staticmethod
    def _add_headers():
        """
        Add more HTTP headers to response
        """
        csp_value = ' '.join(())
        csp_value = ' '.join(("base-uri 'none';", "child-src 'none';", "connect-src 'none';",
                              "default-src 'none';", "font-src 'self';", "form-action 'self';",
                              "frame-ancestors 'none';", "frame-src 'none';", "img-src 'self' data:;",
                              "media-src 'none';", "object-src 'none';", "script-src 'none';",
                              "style-src 'self';"))
        for header, value in (
         ('Cache-Control', 'no-store,no-cache,max-age=0,must-revalidate'),
         ('X-XSS-Protection', '1; mode=block'),
         ('X-DNS-Prefetch-Control', 'off'),
         ('X-Content-Type-Options', 'nosniff'),
         ('X-Frame-Options', 'deny'),
         ('Server', 'unknown'),
         (
          'Content-Security-Policy', csp_value),
         (
          'X-Webkit-CSP', csp_value),
         (
          'X-Content-Security-Policy', csp_value),
         ('Referrer-Policy', 'same-origin')):
            web.header(header, value)

    def GET(self):
        """
        handle GET request by returning default entry page
        """
        return RENDER.default()


class BaseApp(Default):
    """BaseApp"""
    post_form = web.form.Form()
    get_form = web.form.Form(USERNAME_FIELD)
    filterstr_template = '(|)'

    def _sess_track_ctrl(self):
        """
        return LDAPv3 session tracking control representing current user
        """
        return SessionTrackingControl(self.remote_ip, web.ctx.homedomain, SESSION_TRACKING_FORMAT_OID_USERNAME, str(id(self)))

    def search_user_entry(self, inputs):
        """
        Search a user entry for the user specified by username
        """
        filterstr_inputs_dict = {'currenttime': ldap0.filter.escape_str(ldap0.functions.strf_secs(time.time()))}
        for key, value in inputs.items():
            filterstr_inputs_dict[key] = ldap0.filter.escape_str(value)

        filterstr = (self.filterstr_template.format)(**filterstr_inputs_dict)
        self.logger.debug('.search_user_entry() base=%r filterstr=%r', self.ldap_conn.ldap_url_obj.dn, filterstr)
        try:
            user = self.ldap_conn.find_unique_entry((self.ldap_conn.ldap_url_obj.dn),
              (ldap0.SCOPE_SUBTREE),
              filterstr=filterstr,
              attrlist=USER_ATTRS,
              req_ctrls=[
             PWDPOLICY_DEREF_CONTROL])
        except ldap0.LDAPError as ldap_err:
            try:
                self.logger.warning('.search_user_entry() search failed: %s', ldap_err)
                raise
            finally:
                ldap_err = None
                del ldap_err

        else:
            if user.ctrls:
                user.entry_b.update(user.ctrls[0].derefRes['pwdPolicySubentry'][0].entry_b)
            self.logger.debug('.search_user_entry() returns %r', (
             user.dn_s, user.entry_s))
            return (
             user.dn_s, user.entry_s)

    def _open_ldap_conn(self):
        """
        Open LDAP connection
        """
        try:
            self.ldap_conn = aedir.AEDirObject(PWD_LDAP_URL, trace_level=0)
        except ldap0.LDAPError as ldap_err:
            try:
                self.logger.error('Error connecting to %r: %s', PWD_LDAP_URL, ldap_err)
                raise
            finally:
                ldap_err = None
                del ldap_err

        else:
            self.logger.debug('Successfully bound to %r as %r', self.ldap_conn.ldap_url_obj.connect_uri(), self.ldap_conn.whoami_s())

    def _close_ldap_conn(self):
        """
        Close LDAP connection
        """
        self.logger.debug('Unbind from %r', self.ldap_conn.ldap_url_obj.connect_uri())
        try:
            self.ldap_conn.unbind_s()
        except (AttributeError, ldap0.LDAPError) as ldap_err:
            try:
                self.logger.warning('Error during unbinding from %r: %s', self.ldap_conn.ldap_url_obj.connect_uri(), ldap_err)
            finally:
                ldap_err = None
                del ldap_err

    def handle_user_request(self, user_dn, user_entry):
        """
        nothing to be done herein
        """
        raise NotImplementedError

    def POST--- This code section failed: ---

 L. 413         0  LOAD_FAST                'self'
                2  LOAD_METHOD              post_form
                4  CALL_METHOD_0         0  ''
                6  LOAD_FAST                'self'
                8  STORE_ATTR               form

 L. 414        10  LOAD_FAST                'self'
               12  LOAD_ATTR                form
               14  LOAD_METHOD              validates
               16  CALL_METHOD_0         0  ''
               18  POP_JUMP_IF_TRUE     30  'to 30'

 L. 415        20  LOAD_GLOBAL              RENDER
               22  LOAD_METHOD              error
               24  LOAD_STR                 'Invalid input!'
               26  CALL_METHOD_1         1  ''
               28  RETURN_VALUE     
             30_0  COME_FROM            18  '18'

 L. 416        30  SETUP_FINALLY        44  'to 44'

 L. 417        32  LOAD_FAST                'self'
               34  LOAD_METHOD              _open_ldap_conn
               36  CALL_METHOD_0         0  ''
               38  POP_TOP          
               40  POP_BLOCK        
               42  JUMP_FORWARD         76  'to 76'
             44_0  COME_FROM_FINALLY    30  '30'

 L. 418        44  DUP_TOP          
               46  LOAD_GLOBAL              ldap0
               48  LOAD_ATTR                LDAPError
               50  COMPARE_OP               exception-match
               52  POP_JUMP_IF_FALSE    74  'to 74'
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L. 419        60  LOAD_GLOBAL              RENDER
               62  LOAD_METHOD              error
               64  LOAD_STR                 'Internal error!'
               66  CALL_METHOD_1         1  ''
               68  ROT_FOUR         
               70  POP_EXCEPT       
               72  RETURN_VALUE     
             74_0  COME_FROM            52  '52'
               74  END_FINALLY      
             76_0  COME_FROM            42  '42'

 L. 420        76  SETUP_FINALLY       110  'to 110'

 L. 422        78  LOAD_FAST                'self'
               80  LOAD_METHOD              search_user_entry
               82  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               84  LOAD_STR                 'BaseApp.POST.<locals>.<dictcomp>'
               86  MAKE_FUNCTION_0          ''

 L. 424        88  LOAD_FAST                'self'
               90  LOAD_ATTR                form
               92  LOAD_ATTR                inputs

 L. 422        94  GET_ITER         
               96  CALL_FUNCTION_1       1  ''
               98  CALL_METHOD_1         1  ''
              100  UNPACK_SEQUENCE_2     2 
              102  STORE_FAST               'user_dn'
              104  STORE_FAST               'user_entry'
              106  POP_BLOCK        
              108  JUMP_FORWARD        198  'to 198'
            110_0  COME_FROM_FINALLY    76  '76'

 L. 426       110  DUP_TOP          
              112  LOAD_GLOBAL              ValueError
              114  COMPARE_OP               exception-match
              116  POP_JUMP_IF_FALSE   166  'to 166'
              118  POP_TOP          
              120  STORE_FAST               'err'
              122  POP_TOP          
              124  SETUP_FINALLY       154  'to 154'

 L. 427       126  LOAD_FAST                'self'
              128  LOAD_ATTR                logger
              130  LOAD_METHOD              warning
              132  LOAD_STR                 'Invalid input: %s'
              134  LOAD_FAST                'err'
              136  CALL_METHOD_2         2  ''
              138  POP_TOP          

 L. 428       140  LOAD_GLOBAL              RENDER
              142  LOAD_METHOD              error
              144  LOAD_STR                 'Invalid input!'
              146  CALL_METHOD_1         1  ''
              148  STORE_FAST               'res'
              150  POP_BLOCK        
              152  BEGIN_FINALLY    
            154_0  COME_FROM_FINALLY   124  '124'
              154  LOAD_CONST               None
              156  STORE_FAST               'err'
              158  DELETE_FAST              'err'
              160  END_FINALLY      
              162  POP_EXCEPT       
              164  JUMP_FORWARD        210  'to 210'
            166_0  COME_FROM           116  '116'

 L. 429       166  DUP_TOP          
              168  LOAD_GLOBAL              ldap0
              170  LOAD_ATTR                LDAPError
              172  COMPARE_OP               exception-match
              174  POP_JUMP_IF_FALSE   196  'to 196'
              176  POP_TOP          
              178  POP_TOP          
              180  POP_TOP          

 L. 430       182  LOAD_GLOBAL              RENDER
              184  LOAD_METHOD              error
              186  LOAD_STR                 'Searching the user account failed!'
              188  CALL_METHOD_1         1  ''
              190  STORE_FAST               'res'
              192  POP_EXCEPT       
              194  JUMP_FORWARD        210  'to 210'
            196_0  COME_FROM           174  '174'
              196  END_FINALLY      
            198_0  COME_FROM           108  '108'

 L. 433       198  LOAD_FAST                'self'
              200  LOAD_METHOD              handle_user_request
              202  LOAD_FAST                'user_dn'
              204  LOAD_FAST                'user_entry'
              206  CALL_METHOD_2         2  ''
              208  STORE_FAST               'res'
            210_0  COME_FROM           194  '194'
            210_1  COME_FROM           164  '164'

 L. 434       210  LOAD_FAST                'self'
              212  LOAD_METHOD              _close_ldap_conn
              214  CALL_METHOD_0         0  ''
              216  POP_TOP          

 L. 435       218  LOAD_FAST                'res'
              220  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_FOUR' instruction at offset 68


class CheckPassword(BaseApp):
    """CheckPassword"""
    filterstr_template = FILTERSTR_CHANGEPW
    post_form = web.form.Form(USERNAME_FIELD, USERPASSWORD_FIELD, web.form.Button('submit', type='submit', description='Check password'))

    def GET--- This code section failed: ---

 L. 456         0  SETUP_FINALLY        18  'to 18'

 L. 457         2  LOAD_GLOBAL              web
                4  LOAD_ATTR                input
                6  LOAD_STR                 ''
                8  LOAD_CONST               ('username',)
               10  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               12  STORE_FAST               'get_input'
               14  POP_BLOCK        
               16  JUMP_FORWARD         82  'to 82'
             18_0  COME_FROM_FINALLY     0  '0'

 L. 458        18  DUP_TOP          
               20  LOAD_GLOBAL              UnicodeError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    80  'to 80'
               26  POP_TOP          
               28  STORE_FAST               'err'
               30  POP_TOP          
               32  SETUP_FINALLY        68  'to 68'

 L. 459        34  LOAD_FAST                'self'
               36  LOAD_ATTR                logger
               38  LOAD_METHOD              warning
               40  LOAD_STR                 'Invalid input: %s'
               42  LOAD_FAST                'err'
               44  CALL_METHOD_2         2  ''
               46  POP_TOP          

 L. 460        48  LOAD_GLOBAL              RENDER
               50  LOAD_METHOD              checkpw_form
               52  LOAD_STR                 ''
               54  LOAD_STR                 'Invalid input'
               56  CALL_METHOD_2         2  ''
               58  ROT_FOUR         
               60  POP_BLOCK        
               62  POP_EXCEPT       
               64  CALL_FINALLY         68  'to 68'
               66  RETURN_VALUE     
             68_0  COME_FROM            64  '64'
             68_1  COME_FROM_FINALLY    32  '32'
               68  LOAD_CONST               None
               70  STORE_FAST               'err'
               72  DELETE_FAST              'err'
               74  END_FINALLY      
               76  POP_EXCEPT       
               78  JUMP_FORWARD         96  'to 96'
             80_0  COME_FROM            24  '24'
               80  END_FINALLY      
             82_0  COME_FROM            16  '16'

 L. 462        82  LOAD_GLOBAL              RENDER
               84  LOAD_METHOD              checkpw_form
               86  LOAD_FAST                'get_input'
               88  LOAD_ATTR                username
               90  LOAD_STR                 ''
               92  CALL_METHOD_2         2  ''
               94  RETURN_VALUE     
             96_0  COME_FROM            78  '78'

Parse error at or near `ROT_FOUR' instruction at offset 58

    def handle_user_request--- This code section failed: ---

 L. 469         0  LOAD_GLOBAL              time
                2  LOAD_METHOD              time
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'current_time'

 L. 470         8  SETUP_FINALLY        56  'to 56'

 L. 471        10  LOAD_FAST                'self'
               12  LOAD_ATTR                ldap_conn
               14  LOAD_ATTR                simple_bind_s

 L. 472        16  LOAD_FAST                'user_dn'

 L. 473        18  LOAD_FAST                'self'
               20  LOAD_ATTR                form
               22  LOAD_ATTR                d
               24  LOAD_ATTR                oldpassword
               26  LOAD_METHOD              encode
               28  LOAD_STR                 'utf-8'
               30  CALL_METHOD_1         1  ''

 L. 475        32  LOAD_GLOBAL              PasswordPolicyControl
               34  CALL_FUNCTION_0       0  ''

 L. 476        36  LOAD_FAST                'self'
               38  LOAD_METHOD              _sess_track_ctrl
               40  CALL_METHOD_0         0  ''

 L. 474        42  BUILD_LIST_2          2 

 L. 471        44  LOAD_CONST               ('req_ctrls',)
               46  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               48  POP_TOP          
               50  POP_BLOCK        
            52_54  JUMP_FORWARD        374  'to 374'
             56_0  COME_FROM_FINALLY     8  '8'

 L. 479        56  DUP_TOP          
               58  LOAD_GLOBAL              ldap0
               60  LOAD_ATTR                INVALID_CREDENTIALS
               62  COMPARE_OP               exception-match
               64  POP_JUMP_IF_FALSE   130  'to 130'
               66  POP_TOP          
               68  STORE_FAST               'ldap_err'
               70  POP_TOP          
               72  SETUP_FINALLY       116  'to 116'

 L. 480        74  LOAD_FAST                'self'
               76  LOAD_ATTR                logger
               78  LOAD_METHOD              warning

 L. 481        80  LOAD_STR                 'Binding as %r failed: %s'

 L. 482        82  LOAD_FAST                'user_dn'

 L. 483        84  LOAD_FAST                'ldap_err'

 L. 480        86  CALL_METHOD_3         3  ''
               88  POP_TOP          

 L. 485        90  LOAD_GLOBAL              RENDER
               92  LOAD_METHOD              checkpw_form
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                form
               98  LOAD_ATTR                d
              100  LOAD_ATTR                username
              102  LOAD_STR                 'Wrong password!'
              104  CALL_METHOD_2         2  ''
              106  ROT_FOUR         
              108  POP_BLOCK        
              110  POP_EXCEPT       
              112  CALL_FINALLY        116  'to 116'
              114  RETURN_VALUE     
            116_0  COME_FROM           112  '112'
            116_1  COME_FROM_FINALLY    72  '72'
              116  LOAD_CONST               None
              118  STORE_FAST               'ldap_err'
              120  DELETE_FAST              'ldap_err'
              122  END_FINALLY      
              124  POP_EXCEPT       
          126_128  JUMP_FORWARD        374  'to 374'
            130_0  COME_FROM            64  '64'

 L. 486       130  DUP_TOP          
              132  LOAD_GLOBAL              PasswordPolicyExpirationWarning
              134  COMPARE_OP               exception-match
              136  POP_JUMP_IF_FALSE   232  'to 232'
              138  POP_TOP          
              140  STORE_FAST               'ppolicy_error'
              142  POP_TOP          
              144  SETUP_FINALLY       220  'to 220'

 L. 487       146  LOAD_GLOBAL              time
              148  LOAD_METHOD              strftime

 L. 488       150  LOAD_GLOBAL              TIME_DISPLAY_FORMAT

 L. 489       152  LOAD_GLOBAL              time
              154  LOAD_METHOD              localtime
              156  LOAD_FAST                'current_time'
              158  LOAD_FAST                'ppolicy_error'
              160  LOAD_ATTR                timeBeforeExpiration
              162  BINARY_ADD       
              164  CALL_METHOD_1         1  ''

 L. 487       166  CALL_METHOD_2         2  ''
              168  STORE_FAST               'expire_time_str'

 L. 491       170  LOAD_FAST                'self'
              172  LOAD_ATTR                logger
              174  LOAD_METHOD              info

 L. 492       176  LOAD_STR                 'Password of %r will expire soon at %r (%d seconds)'

 L. 493       178  LOAD_FAST                'user_dn'

 L. 494       180  LOAD_FAST                'expire_time_str'

 L. 495       182  LOAD_FAST                'ppolicy_error'
              184  LOAD_ATTR                timeBeforeExpiration

 L. 491       186  CALL_METHOD_4         4  ''
              188  POP_TOP          

 L. 497       190  LOAD_GLOBAL              RENDER
              192  LOAD_METHOD              changepw_form

 L. 498       194  LOAD_FAST                'self'
              196  LOAD_ATTR                form
              198  LOAD_ATTR                d
              200  LOAD_ATTR                username

 L. 499       202  LOAD_STR                 'Password will expire soon at %s. Change it now!'
              204  LOAD_FAST                'expire_time_str'
              206  BINARY_MODULO    

 L. 497       208  CALL_METHOD_2         2  ''
              210  ROT_FOUR         
              212  POP_BLOCK        
              214  POP_EXCEPT       
              216  CALL_FINALLY        220  'to 220'
              218  RETURN_VALUE     
            220_0  COME_FROM           216  '216'
            220_1  COME_FROM_FINALLY   144  '144'
              220  LOAD_CONST               None
              222  STORE_FAST               'ppolicy_error'
              224  DELETE_FAST              'ppolicy_error'
              226  END_FINALLY      
              228  POP_EXCEPT       
              230  JUMP_FORWARD        374  'to 374'
            232_0  COME_FROM           136  '136'

 L. 501       232  DUP_TOP          
              234  LOAD_GLOBAL              PasswordPolicyException
              236  COMPARE_OP               exception-match
          238_240  POP_JUMP_IF_FALSE   306  'to 306'
              242  POP_TOP          
              244  STORE_FAST               'ppolicy_error'
              246  POP_TOP          
              248  SETUP_FINALLY       294  'to 294'

 L. 502       250  LOAD_FAST                'self'
              252  LOAD_ATTR                logger
              254  LOAD_METHOD              warning
              256  LOAD_STR                 'Password policy error: %s'
              258  LOAD_FAST                'ppolicy_error'
              260  CALL_METHOD_2         2  ''
              262  POP_TOP          

 L. 503       264  LOAD_GLOBAL              RENDER
              266  LOAD_METHOD              changepw_form

 L. 504       268  LOAD_FAST                'self'
              270  LOAD_ATTR                form
              272  LOAD_ATTR                d
              274  LOAD_ATTR                username

 L. 505       276  LOAD_GLOBAL              str
              278  LOAD_FAST                'ppolicy_error'
              280  CALL_FUNCTION_1       1  ''

 L. 503       282  CALL_METHOD_2         2  ''
              284  ROT_FOUR         
              286  POP_BLOCK        
              288  POP_EXCEPT       
              290  CALL_FINALLY        294  'to 294'
              292  RETURN_VALUE     
            294_0  COME_FROM           290  '290'
            294_1  COME_FROM_FINALLY   248  '248'
              294  LOAD_CONST               None
              296  STORE_FAST               'ppolicy_error'
              298  DELETE_FAST              'ppolicy_error'
              300  END_FINALLY      
              302  POP_EXCEPT       
              304  JUMP_FORWARD        374  'to 374'
            306_0  COME_FROM           238  '238'

 L. 507       306  DUP_TOP          
              308  LOAD_GLOBAL              ldap0
              310  LOAD_ATTR                LDAPError
              312  COMPARE_OP               exception-match
          314_316  POP_JUMP_IF_FALSE   372  'to 372'
              318  POP_TOP          
              320  STORE_FAST               'ldap_err'
              322  POP_TOP          
              324  SETUP_FINALLY       360  'to 360'

 L. 508       326  LOAD_FAST                'self'
              328  LOAD_ATTR                logger
              330  LOAD_METHOD              warning

 L. 509       332  LOAD_STR                 'LDAP error checking password of %r: %s'

 L. 510       334  LOAD_FAST                'user_dn'

 L. 511       336  LOAD_FAST                'ldap_err'

 L. 508       338  CALL_METHOD_3         3  ''
              340  POP_TOP          

 L. 513       342  LOAD_GLOBAL              RENDER
              344  LOAD_METHOD              error
              346  LOAD_STR                 'Internal error!'
              348  CALL_METHOD_1         1  ''
              350  ROT_FOUR         
              352  POP_BLOCK        
              354  POP_EXCEPT       
              356  CALL_FINALLY        360  'to 360'
              358  RETURN_VALUE     
            360_0  COME_FROM           356  '356'
            360_1  COME_FROM_FINALLY   324  '324'
              360  LOAD_CONST               None
              362  STORE_FAST               'ldap_err'
              364  DELETE_FAST              'ldap_err'
              366  END_FINALLY      
              368  POP_EXCEPT       
              370  JUMP_FORWARD        374  'to 374'
            372_0  COME_FROM           314  '314'
              372  END_FINALLY      
            374_0  COME_FROM           370  '370'
            374_1  COME_FROM           304  '304'
            374_2  COME_FROM           230  '230'
            374_3  COME_FROM           126  '126'
            374_4  COME_FROM            52  '52'

 L. 515       374  SETUP_FINALLY       396  'to 396'

 L. 516       376  LOAD_GLOBAL              int
              378  LOAD_FAST                'user_entry'
              380  LOAD_STR                 'pwdMaxAge'
              382  BINARY_SUBSCR    
              384  LOAD_CONST               0
              386  BINARY_SUBSCR    
              388  CALL_FUNCTION_1       1  ''
              390  STORE_FAST               'pwd_max_age'
              392  POP_BLOCK        
              394  JUMP_FORWARD        426  'to 426'
            396_0  COME_FROM_FINALLY   374  '374'

 L. 517       396  DUP_TOP          
              398  LOAD_GLOBAL              ValueError
              400  LOAD_GLOBAL              KeyError
              402  BUILD_TUPLE_2         2 
              404  COMPARE_OP               exception-match
          406_408  POP_JUMP_IF_FALSE   424  'to 424'
              410  POP_TOP          
              412  POP_TOP          
              414  POP_TOP          

 L. 518       416  LOAD_STR                 'unknown'
              418  STORE_FAST               'valid_until'
              420  POP_EXCEPT       
              422  JUMP_FORWARD        488  'to 488'
            424_0  COME_FROM           406  '406'
              424  END_FINALLY      
            426_0  COME_FROM           394  '394'

 L. 520       426  LOAD_GLOBAL              ldap0
              428  LOAD_ATTR                functions
              430  LOAD_METHOD              strp_secs
              432  LOAD_FAST                'user_entry'
              434  LOAD_STR                 'pwdChangedTime'
              436  BINARY_SUBSCR    
              438  LOAD_CONST               0
              440  BINARY_SUBSCR    
              442  CALL_METHOD_1         1  ''
              444  STORE_FAST               'pwd_changed_timestamp'

 L. 521       446  LOAD_FAST                'pwd_changed_timestamp'
              448  LOAD_FAST                'pwd_max_age'
              450  BINARY_ADD       
              452  STORE_FAST               'expire_timestamp'

 L. 522       454  LOAD_GLOBAL              time
              456  LOAD_METHOD              strftime

 L. 523       458  LOAD_GLOBAL              TIME_DISPLAY_FORMAT

 L. 524       460  LOAD_GLOBAL              time
              462  LOAD_METHOD              localtime
              464  LOAD_FAST                'expire_timestamp'
              466  CALL_METHOD_1         1  ''

 L. 522       468  CALL_METHOD_2         2  ''
              470  STORE_FAST               'valid_until'

 L. 526       472  LOAD_FAST                'self'
              474  LOAD_ATTR                logger
              476  LOAD_METHOD              info

 L. 527       478  LOAD_STR                 'User %r checked own password, valid until %s.'

 L. 528       480  LOAD_FAST                'user_dn'

 L. 529       482  LOAD_FAST                'valid_until'

 L. 526       484  CALL_METHOD_3         3  ''
              486  POP_TOP          
            488_0  COME_FROM           422  '422'

 L. 532       488  LOAD_GLOBAL              RENDER
              490  LOAD_METHOD              checkpw_action

 L. 533       492  LOAD_FAST                'self'
              494  LOAD_ATTR                form
              496  LOAD_ATTR                d
              498  LOAD_ATTR                username

 L. 534       500  LOAD_FAST                'user_dn'

 L. 535       502  LOAD_FAST                'valid_until'

 L. 532       504  CALL_METHOD_3         3  ''
              506  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_FOUR' instruction at offset 106


class ChangePassword(BaseApp):
    """ChangePassword"""
    filterstr_template = FILTERSTR_CHANGEPW
    post_form = web.form.Form(USERNAME_FIELD, USERPASSWORD_FIELD, NEWPASSWORD1_FIELD, NEWPASSWORD2_FIELD, web.form.Button('submit',
      type='submit',
      description='Change password'))

    def GET--- This code section failed: ---

 L. 563         0  SETUP_FINALLY        18  'to 18'

 L. 564         2  LOAD_GLOBAL              web
                4  LOAD_ATTR                input
                6  LOAD_STR                 ''
                8  LOAD_CONST               ('username',)
               10  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               12  STORE_FAST               'get_input'
               14  POP_BLOCK        
               16  JUMP_FORWARD         82  'to 82'
             18_0  COME_FROM_FINALLY     0  '0'

 L. 565        18  DUP_TOP          
               20  LOAD_GLOBAL              UnicodeError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    80  'to 80'
               26  POP_TOP          
               28  STORE_FAST               'err'
               30  POP_TOP          
               32  SETUP_FINALLY        68  'to 68'

 L. 566        34  LOAD_FAST                'self'
               36  LOAD_ATTR                logger
               38  LOAD_METHOD              warning
               40  LOAD_STR                 'Invalid input: %s'
               42  LOAD_FAST                'err'
               44  CALL_METHOD_2         2  ''
               46  POP_TOP          

 L. 567        48  LOAD_GLOBAL              RENDER
               50  LOAD_METHOD              changepw_form
               52  LOAD_STR                 ''
               54  LOAD_STR                 'Invalid input'
               56  CALL_METHOD_2         2  ''
               58  ROT_FOUR         
               60  POP_BLOCK        
               62  POP_EXCEPT       
               64  CALL_FINALLY         68  'to 68'
               66  RETURN_VALUE     
             68_0  COME_FROM            64  '64'
             68_1  COME_FROM_FINALLY    32  '32'
               68  LOAD_CONST               None
               70  STORE_FAST               'err'
               72  DELETE_FAST              'err'
               74  END_FINALLY      
               76  POP_EXCEPT       
               78  JUMP_FORWARD         96  'to 96'
             80_0  COME_FROM            24  '24'
               80  END_FINALLY      
             82_0  COME_FROM            16  '16'

 L. 569        82  LOAD_GLOBAL              RENDER
               84  LOAD_METHOD              changepw_form
               86  LOAD_FAST                'get_input'
               88  LOAD_ATTR                username
               90  LOAD_STR                 ''
               92  CALL_METHOD_2         2  ''
               94  RETURN_VALUE     
             96_0  COME_FROM            78  '78'

Parse error at or near `ROT_FOUR' instruction at offset 58

    def _check_pw_input(self, user_entry):
        if self.form.d.newpassword1 != self.form.d.newpassword2:
            return 'New password values differ!'
            if 'pwdMinLength' in user_entry:
                pwd_min_len = int(user_entry['pwdMinLength'][0])
                if len(self.form.d.newpassword1) < pwd_min_len:
                    self.logger.warning('Password of %r not long enough, only got %d chars.', user_entry['uid'][0], len(self.form.d.newpassword1))
                    return 'New password must be at least %d characters long!' % pwd_min_len
        elif 'pwdChangedTime' in user_entry:
            if 'pwdMinAge' in user_entry:
                pwd_changed_timestamp = ldap0.functions.strp_secs(user_entry['pwdChangedTime'][0])
                pwd_min_age = int(user_entry['pwdMinAge'][0])
                next_pwd_change_timespan = pwd_changed_timestamp + pwd_min_age - time.time()
                if next_pwd_change_timespan > 0:
                    self.logger.warning('Password of %r is too young to change!', user_entry['uid'][0])
                    return 'Password is too young to change! You can try again after %d secs.' % next_pwd_change_timespan

    def handle_user_request(self, user_dn, user_entry):
        """
        set new password
        """
        pw_input_check_msg = self._check_pw_input(user_entry)
        if pw_input_check_msg is not None:
            return RENDER.changepw_form(self.form.d.username, pw_input_check_msg)
        try:
            self.ldap_conn.simple_bind_s(user_dn,
              (self.form.d.oldpassword.encode('utf-8')),
              req_ctrls=[
             self._sess_track_ctrl()])
            self.ldap_conn.passwd_s(user_dn,
              None,
              (self.form.d.newpassword1.encode('utf-8')),
              req_ctrls=[
             self._sess_track_ctrl()])
        except ldap0.INVALID_CREDENTIALS as ldap_err:
            try:
                self.logger.warning('Old password of %r wrong: %s', user_dn, ldap_err)
                res = RENDER.changepw_form(self.form.d.username, 'Old password wrong!')
            finally:
                ldap_err = None
                del ldap_err

        except ldap0.CONSTRAINT_VIOLATION as ldap_err:
            try:
                self.logger.warning('Changing password of %r failed: %s', user_dn, ldap_err)
                res = RENDER.changepw_form(self.form.d.username, 'Password rules violation: {0}'.format(ldap_err.args[0]['info'].decode('utf-8')))
            finally:
                ldap_err = None
                del ldap_err

        except ldap0.LDAPError as ldap_err:
            try:
                self.logger.warning('LDAP error: %s', ldap_err)
                res = RENDER.error('Internal error!')
            finally:
                ldap_err = None
                del ldap_err

        else:
            self.logger.info('User %r changed own password.', user_dn)
            res = RENDER.changepw_action(self.form.d.username, user_dn, self.ldap_conn.ldap_url_obj.connect_uri())
        return res


class RequestPasswordReset(BaseApp):
    """RequestPasswordReset"""
    filterstr_template = FILTERSTR_REQUESTPW
    post_form = web.form.Form(USERNAME_FIELD, EMAIL_FIELD, web.form.Button('submit',
      type='submit',
      description='Set new password'))

    def GET--- This code section failed: ---

 L. 664         0  SETUP_FINALLY        18  'to 18'

 L. 665         2  LOAD_GLOBAL              web
                4  LOAD_ATTR                input
                6  LOAD_STR                 ''
                8  LOAD_CONST               ('username',)
               10  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               12  STORE_FAST               'get_input'
               14  POP_BLOCK        
               16  JUMP_FORWARD         82  'to 82'
             18_0  COME_FROM_FINALLY     0  '0'

 L. 666        18  DUP_TOP          
               20  LOAD_GLOBAL              UnicodeError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    80  'to 80'
               26  POP_TOP          
               28  STORE_FAST               'err'
               30  POP_TOP          
               32  SETUP_FINALLY        68  'to 68'

 L. 667        34  LOAD_FAST                'self'
               36  LOAD_ATTR                logger
               38  LOAD_METHOD              warning
               40  LOAD_STR                 'Invalid input: %s'
               42  LOAD_FAST                'err'
               44  CALL_METHOD_2         2  ''
               46  POP_TOP          

 L. 668        48  LOAD_GLOBAL              RENDER
               50  LOAD_METHOD              requestpw_form
               52  LOAD_STR                 ''
               54  LOAD_STR                 'Invalid input'
               56  CALL_METHOD_2         2  ''
               58  ROT_FOUR         
               60  POP_BLOCK        
               62  POP_EXCEPT       
               64  CALL_FINALLY         68  'to 68'
               66  RETURN_VALUE     
             68_0  COME_FROM            64  '64'
             68_1  COME_FROM_FINALLY    32  '32'
               68  LOAD_CONST               None
               70  STORE_FAST               'err'
               72  DELETE_FAST              'err'
               74  END_FINALLY      
               76  POP_EXCEPT       
               78  JUMP_FORWARD         96  'to 96'
             80_0  COME_FROM            24  '24'
               80  END_FINALLY      
             82_0  COME_FROM            16  '16'

 L. 670        82  LOAD_GLOBAL              RENDER
               84  LOAD_METHOD              requestpw_form
               86  LOAD_FAST                'get_input'
               88  LOAD_ATTR                username
               90  LOAD_STR                 ''
               92  CALL_METHOD_2         2  ''
               94  RETURN_VALUE     
             96_0  COME_FROM            78  '78'

Parse error at or near `ROT_FOUR' instruction at offset 58

    def _get_admin_mailaddrs(self, user_dn):
        try:
            ldap_results = self.ldap_conn.get_zoneadmins(user_dn,
              attrlist=[
             'mail'],
              suppl_filter='(mail=*)')
        except ldap0.LDAPError:
            admin_addrs = None
        else:
            admin_addrs = [res.entry_s['mail'][0] for res in ldap_results or ]
        return sorted(set(admin_addrs or ))

    def _send_pw(self, username, user_dn, user_entry, temp_pwd_clear):
        """
        send e-mails to user and zone-admins
        """
        smtp_conn = mailutil.smtp_connection(SMTP_URL,
          local_hostname=SMTP_LOCALHOSTNAME,
          ca_certs=SMTP_TLS_CACERTS,
          debug_level=SMTP_DEBUGLEVEL)
        to_addr = user_entry['mail'][0]
        default_headers = (
         (
          'From', SMTP_FROM),
         (
          'Date', email.utils.formatdate(time.time(), True)))
        pwd_admin_len = int(user_entry.get('msPwdResetAdminPwLen', [str(PWD_ADMIN_LEN)])[0])
        if pwd_admin_len:
            user_data_admin = {'username':username,  'temppassword2':temp_pwd_clear[len(temp_pwd_clear) - pwd_admin_len:], 
             'remote_ip':self.remote_ip, 
             'fromaddr':SMTP_FROM, 
             'userdn':user_dn, 
             'userdispname':user_entry['displayName'][0], 
             'web_ctx_host':web.ctx.host, 
             'app_path_prefix':APP_PATH_PREFIX, 
             'ldap_uri':self.ldap_conn.ldap_url_obj.connect_uri()}
            smtp_message = (read_template_file(EMAIL_TEMPLATE_ADMIN).format)(**user_data_admin)
            smtp_subject = (EMAIL_SUBJECT_ADMIN.format)(**user_data_admin)
            admin_addrs = self._get_admin_mailaddrs(user_dn)
            admin_to = ','.join(sorted(admin_addrs))
            smtp_conn.send_simple_message(SMTP_FROM, admin_addrs, 'utf-8', default_headers + (
             (
              'Subject', smtp_subject),
             (
              'To', admin_to)), smtp_message)
            self.logger.info('Sent password reset admin notification to %s', admin_to)
        else:
            admin_addrs = []
        user_data_user = {'username':username, 
         'temppassword1':temp_pwd_clear[:len(temp_pwd_clear) - pwd_admin_len], 
         'remote_ip':self.remote_ip, 
         'fromaddr':SMTP_FROM, 
         'userdn':user_dn, 
         'web_ctx_host':web.ctx.host, 
         'app_path_prefix':APP_PATH_PREFIX, 
         'ldap_uri':self.ldap_conn.ldap_url_obj.connect_uri(), 
         'admin_email_addrs':'\n'.join(admin_addrs)}
        smtp_message = (read_template_file(EMAIL_TEMPLATE_PERSONAL).format)(**user_data_user)
        smtp_subject = (EMAIL_SUBJECT_PERSONAL.format)(**user_data_user)
        smtp_conn.send_simple_message(SMTP_FROM, [
         to_addr], 'utf-8', default_headers + (
         (
          'Subject', smtp_subject),
         (
          'To', to_addr)), smtp_message)
        self.logger.info('Sent reset password to %s', to_addr)
        smtp_conn.quit()

    def handle_user_request(self, user_dn, user_entry):
        """
        add password reset object class and attributes
        to user's entry and send e-mails
        """
        current_time = time.time()
        temp_pwd_len = int(user_entry.get('msPwdResetPwLen', [str(PWD_LENGTH)])[0])
        pwd_admin_len = int(user_entry.get('msPwdResetAdminPwLen', [str(PWD_ADMIN_LEN)])[0])
        temp_pwd_clear = random_string(PWD_TMP_CHARS, temp_pwd_len)
        temp_pwd_hash = pwd_hash(temp_pwd_clear, user_entry.get('msPwdResetHashAlgorithm', [
         PWD_TMP_HASH_ALGO])[0])
        pwd_expire_timespan = int(user_entry.get('msPwdResetMaxAge', [
         str(PWD_EXPIRETIMESPAN)])[0])
        ldap_mod_list = [
         (
          ldap0.MOD_REPLACE, b'msPwdResetPasswordHash', [temp_pwd_hash.encode('ascii')]),
         (
          ldap0.MOD_REPLACE,
          b'msPwdResetTimestamp',
          [
           ldap0.functions.strf_secs(current_time).encode('ascii')]),
         (
          ldap0.MOD_REPLACE,
          b'msPwdResetExpirationTime',
          [
           ldap0.functions.strf_secs(current_time + pwd_expire_timespan).encode('ascii')]),
         (
          ldap0.MOD_REPLACE,
          b'msPwdResetEnabled',
          [
           user_entry.get('msPwdResetEnabled', [PWD_RESET_ENABLED])[0].encode('ascii')])]
        old_objectclasses = [oc.lower() for oc in user_entry['objectClass']]
        if 'mspwdresetobject' not in old_objectclasses:
            ldap_mod_list.append((ldap0.MOD_ADD, b'objectClass', [b'msPwdResetObject']))
        if pwd_admin_len:
            ldap_mod_list.append((
             ldap0.MOD_REPLACE,
             b'msPwdResetAdminPw',
             [
              temp_pwd_clear[-pwd_admin_len:].encode('utf-8')]))
        try:
            self.ldap_conn.modify_s(user_dn,
              ldap_mod_list,
              req_ctrls=[
             self._sess_track_ctrl()])
        except ldap0.LDAPError:
            res = RENDER.error('Internal error!')
        else:
            try:
                self._send_pw(self.form.d.username, user_dn, user_entry, temp_pwd_clear)
            except (socket.error, socket.gaierror, smtplib.SMTPException) as mail_error:
                try:
                    self.logger.error('Error sending reset e-mail to user %r: %s', self.form.d.username, mail_error)
                    res = RENDER.requestpw_form(self.form.d.username, 'Error sending e-mail via SMTP!')
                finally:
                    mail_error = None
                    del mail_error

            else:
                res = RENDER.requestpw_action(self.form.d.username, self.form.d.email, user_dn)
            return res


class FinishPasswordReset(ChangePassword):
    """FinishPasswordReset"""
    filterstr_template = '(&(msPwdResetEnabled=TRUE)%s)' % FILTERSTR_RESETPW
    get_form = web.form.Form(USERNAME_FIELD, TEMP1PASSWORD_FIELD)
    post_form = web.form.Form(USERNAME_FIELD, TEMP1PASSWORD_FIELD, TEMP2PASSWORD_FIELD, NEWPASSWORD1_FIELD, NEWPASSWORD2_FIELD, web.form.Button('submit',
      type='submit',
      description='Change password'))

    def GET--- This code section failed: ---

 L. 887         0  LOAD_GLOBAL              web
                2  LOAD_ATTR                input
                4  LOAD_STR                 ''
                6  LOAD_STR                 ''
                8  LOAD_CONST               ('username', 'temppassword1')
               10  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               12  STORE_FAST               'get_input'

 L. 888        14  LOAD_FAST                'get_input'
               16  LOAD_ATTR                username
               18  POP_JUMP_IF_FALSE    26  'to 26'
               20  LOAD_FAST                'get_input'
               22  LOAD_ATTR                temppassword1
               24  POP_JUMP_IF_TRUE     36  'to 36'
             26_0  COME_FROM            18  '18'

 L. 889        26  LOAD_GLOBAL              RENDER
               28  LOAD_METHOD              error
               30  LOAD_STR                 'Invalid input'
               32  CALL_METHOD_1         1  ''
               34  RETURN_VALUE     
             36_0  COME_FROM            24  '24'

 L. 890        36  SETUP_FINALLY        50  'to 50'

 L. 891        38  LOAD_FAST                'self'
               40  LOAD_METHOD              _open_ldap_conn
               42  CALL_METHOD_0         0  ''
               44  POP_TOP          
               46  POP_BLOCK        
               48  JUMP_FORWARD         82  'to 82'
             50_0  COME_FROM_FINALLY    36  '36'

 L. 892        50  DUP_TOP          
               52  LOAD_GLOBAL              ldap0
               54  LOAD_ATTR                LDAPError
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    80  'to 80'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L. 893        66  LOAD_GLOBAL              RENDER
               68  LOAD_METHOD              error
               70  LOAD_STR                 'Internal LDAP error!'
               72  CALL_METHOD_1         1  ''
               74  ROT_FOUR         
               76  POP_EXCEPT       
               78  RETURN_VALUE     
             80_0  COME_FROM            58  '58'
               80  END_FINALLY      
             82_0  COME_FROM            48  '48'

 L. 894        82  SETUP_FINALLY       108  'to 108'

 L. 895        84  LOAD_FAST                'self'
               86  LOAD_METHOD              search_user_entry
               88  LOAD_STR                 'username'
               90  LOAD_FAST                'get_input'
               92  LOAD_ATTR                username
               94  BUILD_MAP_1           1 
               96  CALL_METHOD_1         1  ''
               98  UNPACK_SEQUENCE_2     2 
              100  STORE_FAST               '_'
              102  STORE_FAST               'user_entry'
              104  POP_BLOCK        
              106  JUMP_FORWARD        140  'to 140'
            108_0  COME_FROM_FINALLY    82  '82'

 L. 896       108  DUP_TOP          
              110  LOAD_GLOBAL              ldap0
              112  LOAD_ATTR                LDAPError
              114  COMPARE_OP               exception-match
              116  POP_JUMP_IF_FALSE   138  'to 138'
              118  POP_TOP          
              120  POP_TOP          
              122  POP_TOP          

 L. 897       124  LOAD_GLOBAL              RENDER
              126  LOAD_METHOD              error
              128  LOAD_STR                 'Error searching user!'
              130  CALL_METHOD_1         1  ''
              132  ROT_FOUR         
              134  POP_EXCEPT       
              136  RETURN_VALUE     
            138_0  COME_FROM           116  '116'
              138  END_FINALLY      
            140_0  COME_FROM           106  '106'

 L. 898       140  LOAD_FAST                'self'
              142  LOAD_METHOD              _close_ldap_conn
              144  CALL_METHOD_0         0  ''
              146  POP_TOP          

 L. 899       148  LOAD_GLOBAL              int
              150  LOAD_FAST                'user_entry'
              152  LOAD_METHOD              get
              154  LOAD_STR                 'msPwdResetAdminPwLen'
              156  LOAD_GLOBAL              str
              158  LOAD_GLOBAL              PWD_ADMIN_LEN
              160  CALL_FUNCTION_1       1  ''
              162  BUILD_LIST_1          1 
              164  CALL_METHOD_2         2  ''
              166  LOAD_CONST               0
              168  BINARY_SUBSCR    
              170  CALL_FUNCTION_1       1  ''
              172  STORE_FAST               'pwd_admin_len'

 L. 900       174  LOAD_GLOBAL              RENDER
              176  LOAD_METHOD              resetpw_form

 L. 901       178  LOAD_FAST                'get_input'
              180  LOAD_ATTR                username

 L. 902       182  LOAD_FAST                'pwd_admin_len'

 L. 903       184  LOAD_FAST                'get_input'
              186  LOAD_ATTR                temppassword1

 L. 904       188  LOAD_STR                 ''

 L. 900       190  CALL_METHOD_4         4  ''
              192  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_FOUR' instruction at offset 74

    def _ldap_user_operations(self, user_dn, user_entry, temp_pwd_hash, new_password_ldap):
        pwd_admin_len = int(user_entry.get('msPwdResetAdminPwLen', [str(PWD_ADMIN_LEN)])[0])
        ldap_mod_list = [(
         ldap0.MOD_DELETE, attr_type.encode('ascii'), attr_values) for attr_type, attr_values in (
         (
          'objectClass', [b'msPwdResetObject']),
         (
          'msPwdResetPasswordHash', [temp_pwd_hash.encode('ascii')]),
         ('msPwdResetTimestamp', None),
         ('msPwdResetExpirationTime', None),
         ('msPwdResetEnabled', None))]
        if pwd_admin_len:
            ldap_mod_list.append((
             ldap0.MOD_DELETE, b'msPwdResetAdminPw', None))
        try:
            self.ldap_conn.modify_s(user_dn,
              ldap_mod_list,
              req_ctrls=[
             self._sess_track_ctrl()])
        except ldap0.LDAPError as ldap_err:
            try:
                self.logger.warning('Modifying entry %r failed: %s', user_dn, ldap_err)
                raise
            finally:
                ldap_err = None
                del ldap_err

        try:
            self.ldap_conn.passwd_s(user_dn,
              None,
              new_password_ldap,
              req_ctrls=[
             self._sess_track_ctrl()])
        except ldap0.LDAPError as ldap_err:
            try:
                self.logger.warning('passwd_s() failed for %r: %s', user_dn, ldap_err)
                raise
            finally:
                ldap_err = None
                del ldap_err

    def handle_user_request(self, user_dn, user_entry):
        """
        set new password if temporary reset password matches
        """
        temppassword1 = self.form.d.temppassword1
        temppassword2 = self.form.d.temppassword2
        pwd_admin_len = int(user_entry.get('msPwdResetAdminPwLen', [str(PWD_ADMIN_LEN)])[0])
        temp_pwd_hash = pwd_hash(''.join((temppassword1, temppassword2)), user_entry.get('msPwdResetHashAlgorithm', [PWD_TMP_HASH_ALGO])[0])
        pw_input_check_msg = self._check_pw_input(user_entry)
        if pw_input_check_msg is not None:
            return RENDER.resetpw_form(self.form.d.username, pwd_admin_len, self.form.d.temppassword1, pw_input_check_msg)
        try:
            self._ldap_user_operations(user_dn, user_entry, temp_pwd_hash, self.form.d.newpassword1.encode('utf-8'))
        except ldap0.NO_SUCH_ATTRIBUTE:
            self.logger.warning('Temporary password of %r wrong!', user_dn)
            res = RENDER.resetpw_form(self.form.d.username, pwd_admin_len, self.form.d.temppassword1, 'Temporary password wrong!')
        except ldap0.CONSTRAINT_VIOLATION as ldap_err:
            try:
                self.logger.warning('Password constraints for %r violated: %s', user_dn, ldap_err)
                res = RENDER.requestpw_form(self.form.d.username, 'Constraint violation (password rules): {0} / You have to request password reset again!'.format(ldap_err.args[0]['info'].decode('utf-8')))
            finally:
                ldap_err = None
                del ldap_err

        except ldap0.LDAPError:
            res = RENDER.error('Internal error!')
        else:
            self.logger.info('Password reset completed for %r.', user_dn)
            res = RENDER.resetpw_action(self.form.d.username, user_dn)
        return res


application = web.application(URL2CLASS_MAPPING, (globals()), autoreload=(bool(WEB_ERROR))).wsgifunc()

def main():
    """
    run the web application
    """
    APP_LOGGER.debug('Starting %s %s', sys.argv[0], __version__)
    app = web.application(URL2CLASS_MAPPING, (globals()), autoreload=(bool(WEB_ERROR)))
    APP_LOGGER.debug('chdir to %r', TEMPLATES_DIRNAME)
    os.chdir(TEMPLATES_DIRNAME)
    if not WEB_ERROR:
        APP_LOGGER.debug('switch off debugging')
        app.internalerror = False
    APP_LOGGER.info('Script %r starts %r instance listening on %r', sys.argv[0], app.__class__.__name__, sys.argv[1])
    app.run()


if __name__ == '__main__':
    main()