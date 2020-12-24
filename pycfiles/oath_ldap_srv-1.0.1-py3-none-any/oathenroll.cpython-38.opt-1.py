# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /oathldap_srv/web/oathenroll.py
# Compiled at: 2020-02-22 18:17:18
# Size of source mod 2**32: 20793 bytes
"""
Web-interface for OATH-LDAP token enrollment

Author: Michael Ströder <michael@stroeder.com>
"""
import os, time, socket, smtplib, hashlib, logging
import urllib.parse as url_quote_plus
import email.utils, web, ldap0, ldap0.filter, ldap0.err
from ldap0 import LDAPError
from ldap0.ldapobject import ReconnectLDAPObject
from ldap0.controls.sessiontrack import SessionTrackingControl, SESSION_TRACKING_FORMAT_OID_USERNAME
from ldap0.ldapurl import LDAPUrl
from ldap0.pw import random_string
import mailutil
from oathenroll_cnf import APP_PATH_PREFIX, ATTR_OWNER_DN, EMAIL_SUBJECT, EMAIL_TEMPLATE, FILTERSTR_ADMIN_LOGIN, FILTERSTR_OWNER_READ, FILTERSTR_TOKEN_SEARCH, LDAPI_AUTHZ_ID, LDAP_URL, PWD_ADMIN_LEN, PWD_LENGTH, PWD_TMP_CHARS, LDAP0_TRACE_LEVEL, SMTP_DEBUGLEVEL, SMTP_FROM, SMTP_LOCALHOSTNAME, SMTP_TLS_CACERTS, SMTP_URL, LAYOUT, TEMPLATES_DIRNAME, WEB_CONFIG_DEBUG, WEB_ERROR
URL2CLASS_MAPPING = ('/', 'Default', '/reset', 'ResetToken', '/init', 'InitToken')

def init_logger():
    """
    Create logger instance
    """
    if 'LOG_CONFIG' in os.environ:
        from logging.config import fileConfig
        fileConfig(os.environ['LOG_CONFIG'])
    else:
        logging.basicConfig(level=(os.environ.get('LOG_LEVEL', '').upper() or logging.INFO),
          format='%(asctime)s %(name)s %(levelname)s: %(message)s',
          datefmt='%Y-%m-%d %H:%M:%S')
    _logger = logging.getLogger(os.environ.get('LOG_QUALNAME', None))
    _logger.name = 'oathenroll'
    return _logger


APP_LOGGER = init_logger()

class ExtLDAPUrl(LDAPUrl):
    __doc__ = '\n    Special class for handling additional LDAP URL extensions\n    '
    attr2extype = {'who':'bindname', 
     'cred':'X-BINDPW', 
     'start_tls':'startTLS', 
     'trace_level':'trace'}


class RequestLogAdaptor(logging.LoggerAdapter):
    __doc__ = '\n    wrapper for adding more request-specific information to log messages\n    '

    def process(self, msg, kwargs):
        return (
         'IP=%s CLASS=%s REQID=%d - %s' % (
          self.extra['remote_ip'],
          self.extra['req_class'],
          self.extra['req_id'],
          msg),
         kwargs)


if PWD_TMP_CHARS != url_quote_plus(PWD_TMP_CHARS):
    raise ValueError('URL special chars in PWD_TMP_CHARS: %r' % (PWD_TMP_CHARS,))
if WEB_CONFIG_DEBUG is False:
    web.config.debug = False
RENDER = web.template.render(TEMPLATES_DIRNAME, base=LAYOUT)
ADMIN_FIELD = web.form.Textbox('admin',
  (web.form.notnull),
  (web.form.regexp('^[a-zA-Z]+$', 'Invalid 2FA admin user name.')),
  description='2FA admin user name')
PASSWORD_FIELD = web.form.Password('password',
  (web.form.notnull),
  (web.form.regexp('^.+$', 'Invalid password')),
  description='2FA admin password')
SERIAL_FIELD = web.form.Textbox('serial',
  (web.form.notnull),
  (web.form.regexp('^[0-9]+$', 'Invalid token serial number')),
  description='E-mail address')
CONFIRM_FIELD = web.form.Textbox('confirm',
  (web.form.regexp('^[0-9a-fA-F]*$', 'Invalid confirmation hash')),
  description='Confirmation hash')

class Default:
    __doc__ = '\n    Handle requests to base URL\n    '
    ldap_url = ExtLDAPUrl(LDAP_URL)

    def __init__(self):
        self.remote_ip = web.ctx.env.get('FORWARDED_FOR', web.ctx.env.get('HTTP_X_FORWARDED_FOR', web.ctx.ip))
        self.logger = RequestLogAdaptor(APP_LOGGER, {'remote_ip':self.remote_ip, 
         'req_class':'.'.join((self.__class__.__module__, self.__class__.__name__)), 
         'req_id':id(self)})
        self.logger.debug('%s request from %s (via %s)', web.ctx.env['REQUEST_METHOD'], self.remote_ip, web.ctx.ip)
        self._add_headers()
        self.ldap_conn = None
        self.user_ldap_conn = None

    @staticmethod
    def _add_headers():
        """
        Add more HTTP headers to response
        """
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

    def GET(self, message=''):
        """
        Simply display the entry landing page
        """
        return RENDER.default()


class BaseApp(Default):
    __doc__ = '\n    Request handler base class which is not used directly\n    '
    post_form = None

    def _sess_track_ctrl(self):
        """
        return LDAPv3 session tracking control representing current user
        """
        return SessionTrackingControl(self.remote_ip, web.ctx.homedomain, SESSION_TRACKING_FORMAT_OID_USERNAME, str(id(self)))

    def ldap_connect(self, authz_id=None):
        """
        Connect and bind to the LDAP directory as local system account
        """
        self.ldap_conn = ReconnectLDAPObject((self.ldap_url.connect_uri()),
          trace_level=LDAP0_TRACE_LEVEL)
        self.ldap_conn.sasl_non_interactive_bind_s('EXTERNAL', authz_id=authz_id)

    def open_user_conn(self, username, password):
        """
        Search a user entry specified by :username: and check
        :password: with LDAP simple bind.
        """
        self.user_ldap_conn = None
        user = self.ldap_conn.find_unique_entry((self.ldap_url.dn),
          scope=(self.ldap_url.scope),
          filterstr=FILTERSTR_ADMIN_LOGIN.format(uid=username),
          attrlist=[
         '1.1'])
        self.user_ldap_conn = ReconnectLDAPObject((self.ldap_url.connect_uri()),
          trace_level=LDAP0_TRACE_LEVEL)
        self.user_ldap_conn.simple_bind_s(user.dn_s, password.encode('utf-8'))

    def search_token(self, token_serial):
        """
        Search a token entry specified by serial number
        """
        token = self.user_ldap_conn.find_unique_entry((self.ldap_url.dn),
          scope=(self.ldap_url.scope),
          filterstr=FILTERSTR_TOKEN_SEARCH.format(owner_attr=ATTR_OWNER_DN,
          serial=token_serial),
          attrlist=[
         'createTimestamp',
         'displayName',
         'oathFailureCount',
         'oathHOTPCounter',
         'oathHOTPParams',
         'oathLastFailure',
         'oathLastLogin',
         'oathSecretTime',
         'oathTokenIdentifier',
         'oathTokenSerialNumber',
         ATTR_OWNER_DN],
          req_ctrls=[
         self._sess_track_ctrl()])
        return (
         token.entry_s['displayName'][0], token.dn_s, token.entry_s)

    def do_the_work(self):
        """
        this method contains the real work and is implemented by derived classes
        """
        pass

    def clean_up(self):
        """
        Clean up initialized stuff
        """
        for conn in (
         self.ldap_conn, self.user_ldap_conn):
            if conn:
                try:
                    self.ldap_conn.unbind_s()
                except (AttributeError, LDAPError):
                    pass

    def POST--- This code section failed: ---

 L. 334         0  LOAD_FAST                'self'
                2  LOAD_METHOD              post_form
                4  CALL_METHOD_0         0  ''
                6  LOAD_FAST                'self'
                8  STORE_ATTR               form

 L. 335        10  LOAD_FAST                'self'
               12  LOAD_ATTR                form
               14  LOAD_METHOD              validates
               16  CALL_METHOD_0         0  ''
               18  POP_JUMP_IF_TRUE     32  'to 32'

 L. 336        20  LOAD_FAST                'self'
               22  LOAD_ATTR                GET
               24  LOAD_STR                 'Incomplete or invalid input!'
               26  LOAD_CONST               ('message',)
               28  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               30  RETURN_VALUE     
             32_0  COME_FROM            18  '18'

 L. 338        32  SETUP_FINALLY        50  'to 50'

 L. 339        34  LOAD_FAST                'self'
               36  LOAD_ATTR                ldap_connect
               38  LOAD_GLOBAL              LDAPI_AUTHZ_ID
               40  LOAD_CONST               ('authz_id',)
               42  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               44  POP_TOP          
               46  POP_BLOCK        
               48  JUMP_FORWARD        194  'to 194'
             50_0  COME_FROM_FINALLY    32  '32'

 L. 340        50  DUP_TOP          
               52  LOAD_GLOBAL              ldap0
               54  LOAD_ATTR                SERVER_DOWN
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE   122  'to 122'
               60  POP_TOP          
               62  STORE_FAST               'ldap_err'
               64  POP_TOP          
               66  SETUP_FINALLY       110  'to 110'

 L. 341        68  LOAD_FAST                'self'
               70  LOAD_ATTR                logger
               72  LOAD_METHOD              error
               74  LOAD_STR                 'Error connectiong to %r: %s'
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                ldap_url
               80  LOAD_METHOD              connect_uri
               82  CALL_METHOD_0         0  ''
               84  LOAD_FAST                'ldap_err'
               86  CALL_METHOD_3         3  ''
               88  POP_TOP          

 L. 342        90  LOAD_FAST                'self'
               92  LOAD_ATTR                GET
               94  LOAD_STR                 'LDAP server not reachable!'
               96  LOAD_CONST               ('message',)
               98  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              100  ROT_FOUR         
              102  POP_BLOCK        
              104  POP_EXCEPT       
              106  CALL_FINALLY        110  'to 110'
              108  RETURN_VALUE     
            110_0  COME_FROM           106  '106'
            110_1  COME_FROM_FINALLY    66  '66'
              110  LOAD_CONST               None
              112  STORE_FAST               'ldap_err'
              114  DELETE_FAST              'ldap_err'
              116  END_FINALLY      
              118  POP_EXCEPT       
              120  JUMP_FORWARD        194  'to 194'
            122_0  COME_FROM            58  '58'

 L. 343       122  DUP_TOP          
              124  LOAD_GLOBAL              LDAPError
              126  COMPARE_OP               exception-match
              128  POP_JUMP_IF_FALSE   192  'to 192'
              130  POP_TOP          
              132  STORE_FAST               'ldap_err'
              134  POP_TOP          
              136  SETUP_FINALLY       180  'to 180'

 L. 344       138  LOAD_FAST                'self'
              140  LOAD_ATTR                logger
              142  LOAD_METHOD              error
              144  LOAD_STR                 'Other LDAPError connecting to %r: %s'
              146  LOAD_FAST                'self'
              148  LOAD_ATTR                ldap_url
              150  LOAD_METHOD              connect_uri
              152  CALL_METHOD_0         0  ''
              154  LOAD_FAST                'ldap_err'
              156  CALL_METHOD_3         3  ''
              158  POP_TOP          

 L. 345       160  LOAD_FAST                'self'
              162  LOAD_ATTR                GET
              164  LOAD_STR                 'Internal LDAP error!'
              166  LOAD_CONST               ('message',)
              168  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              170  ROT_FOUR         
              172  POP_BLOCK        
              174  POP_EXCEPT       
              176  CALL_FINALLY        180  'to 180'
              178  RETURN_VALUE     
            180_0  COME_FROM           176  '176'
            180_1  COME_FROM_FINALLY   136  '136'
              180  LOAD_CONST               None
              182  STORE_FAST               'ldap_err'
              184  DELETE_FAST              'ldap_err'
              186  END_FINALLY      
              188  POP_EXCEPT       
              190  JUMP_FORWARD        194  'to 194'
            192_0  COME_FROM           128  '128'
              192  END_FINALLY      
            194_0  COME_FROM           190  '190'
            194_1  COME_FROM           120  '120'
            194_2  COME_FROM            48  '48'

 L. 347       194  SETUP_FINALLY       208  'to 208'

 L. 348       196  LOAD_FAST                'self'
              198  LOAD_METHOD              do_the_work
              200  CALL_METHOD_0         0  ''
              202  STORE_FAST               'res'
              204  POP_BLOCK        
              206  JUMP_FORWARD        274  'to 274'
            208_0  COME_FROM_FINALLY   194  '194'

 L. 349       208  DUP_TOP          
              210  LOAD_GLOBAL              Exception
              212  COMPARE_OP               exception-match
          214_216  POP_JUMP_IF_FALSE   272  'to 272'
              218  POP_TOP          
              220  STORE_FAST               'err'
              222  POP_TOP          
              224  SETUP_FINALLY       260  'to 260'

 L. 350       226  LOAD_FAST                'self'
              228  LOAD_ATTR                logger
              230  LOAD_ATTR                error
              232  LOAD_STR                 'Unhandled exception: %s'
              234  LOAD_FAST                'err'
              236  LOAD_CONST               True
              238  LOAD_CONST               ('exc_info',)
              240  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              242  POP_TOP          

 L. 351       244  LOAD_FAST                'self'
              246  LOAD_ATTR                GET
              248  LOAD_STR                 'Internal error!'
              250  LOAD_CONST               ('message',)
              252  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              254  STORE_FAST               'res'
              256  POP_BLOCK        
              258  BEGIN_FINALLY    
            260_0  COME_FROM_FINALLY   224  '224'
              260  LOAD_CONST               None
              262  STORE_FAST               'err'
              264  DELETE_FAST              'err'
              266  END_FINALLY      
              268  POP_EXCEPT       
              270  JUMP_FORWARD        274  'to 274'
            272_0  COME_FROM           214  '214'
              272  END_FINALLY      
            274_0  COME_FROM           270  '270'
            274_1  COME_FROM           206  '206'

 L. 352       274  LOAD_FAST                'self'
              276  LOAD_METHOD              clean_up
              278  CALL_METHOD_0         0  ''
              280  POP_TOP          

 L. 353       282  LOAD_FAST                'res'
              284  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 102


class ResetToken(BaseApp):
    __doc__ = '\n    Resets token to unusable state but with temporary enrollment password.\n\n    LDAP operations are authenticated with LDAPI/SASL/EXTERNAL\n    '
    post_form = web.form.Form(ADMIN_FIELD, PASSWORD_FIELD, SERIAL_FIELD, CONFIRM_FIELD, web.form.Button('submit',
      type='submit',
      description='Reset token'))

    def GET(self, message=''):
        """
        Process the GET request mainly for displaying input form
        """
        try:
            get_input = web.input(serial='',
              admin='',
              password='')
        except UnicodeError:
            return RENDER.reset_form('Invalid Unicode input')
        else:
            if not get_input.serial:
                message = 'Enter a serial number of token to be (re-)initialized.'
            else:
                if not get_input.admin:
                    message = 'Login with your 2FA admin account.'
            return RENDER.reset_form(message,
              admin=(get_input.admin),
              serial=(get_input.serial))

    def _send_pw(self, token_serial, owner_entry, enroll_pw1):
        """
        Send 2nd part of temporary password to token owner
        """
        smtp_conn = mailutil.smtp_connection(SMTP_URL,
          local_hostname=SMTP_LOCALHOSTNAME,
          ca_certs=SMTP_TLS_CACERTS,
          debug_level=SMTP_DEBUGLEVEL)
        smtp_message_tmpl = open(EMAIL_TEMPLATE, 'rb').read().decode('utf-8')
        to_addr = owner_entry['mail'][0]
        default_headers = (
         (
          'From', SMTP_FROM),
         (
          'Date', email.utils.formatdate(time.time(), True)))
        owner_data = {'serial':token_serial, 
         'admin':self.form.d.admin, 
         'enrollpw1':enroll_pw1, 
         'remote_ip':self.remote_ip, 
         'fromaddr':SMTP_FROM, 
         'web_ctx_host':web.ctx.host, 
         'app_path_prefix':APP_PATH_PREFIX}
        smtp_message = smtp_message_tmpl % owner_data
        smtp_subject = EMAIL_SUBJECT % owner_data
        smtp_conn.send_simple_message(SMTP_FROM, [
         to_addr], 'utf-8', default_headers + (
         (
          'Subject', smtp_subject),
         (
          'To', to_addr)), smtp_message)
        smtp_conn.quit()
        self.logger.info('Sent reset password to %r.', to_addr)

    def search_accounts(self, token_dn):
        """
        Search all accounts using the token
        """
        ldap_result = self.user_ldap_conn.search_s((self.ldap_url.dn),
          (ldap0.SCOPE_SUBTREE),
          filterstr='(&(objectClass=oathUser)(oathToken={dn}))'.format(dn=(ldap0.filter.escape_str(token_dn))),
          attrlist=[
         'uid', 'description'])
        if not ldap_result:
            return
        return [(res.entry_s['uid'][0],
         res.entry_s.get('description', [''])[0]) for res in ldap_result]

    def read_owner(self, owner_dn):
        """
        Read a token owner entry
        """
        ldap_result = self.user_ldap_conn.read_s(owner_dn,
          filterstr=FILTERSTR_OWNER_READ,
          attrlist=[
         'displayName',
         'mail',
         'telePhoneNumber',
         'mobile',
         'l'])
        if ldap_result:
            result = ldap_result.entry_s
        else:
            raise ldap0.NO_SUCH_OBJECT('No result with %r' % (FILTERSTR_OWNER_READ,))
        return result

    def update_token(self, token_dn, token_entry, token_password):
        """
        Resets token to unusable state by
        - overwriting 'oathSecret'
        - removing 'oathLastLogin'
        - removing 'oathHOTPCounter'
        - removing failure attributes 'oathFailureCount' and 'oathLastFailure'
        - setting temporary enrollment password in 'userPassword'
        - resetting 'oathSecretTime' to current time
        """
        session_tracking_ctrl = self._sess_track_ctrl()
        token_mods = [
         (
          ldap0.MOD_REPLACE,
          b'oathSecretTime',
          [
           time.strftime('%Y%m%d%H%M%SZ', time.gmtime(time.time())).encode('ascii')])]
        for del_attr in ('oathHOTPCounter', 'oathLastLogin', 'oathFailureCount', 'oathLastFailure'):
            if del_attr in token_entry:
                token_mods.append((
                 ldap0.MOD_DELETE, del_attr.encode('ascii'), None))
        else:
            self.user_ldap_conn.modify_s(token_dn,
              token_mods,
              req_ctrls=[
             session_tracking_ctrl])
            try:
                self.user_ldap_conn.modify_s(token_dn,
                  [
                 (
                  ldap0.MOD_DELETE, b'oathSecret', None)],
                  req_ctrls=[
                 session_tracking_ctrl])
            except ldap0.NO_SUCH_ATTRIBUTE:
                pass
            else:
                self.ldap_conn.passwd_s(token_dn,
                  None,
                  token_password, req_ctrls=[
                 session_tracking_ctrl])

    def do_the_work--- This code section failed: ---

 L. 554         0  SETUP_FINALLY        30  'to 30'

 L. 555         2  LOAD_FAST                'self'
                4  LOAD_METHOD              open_user_conn
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                form
               10  LOAD_ATTR                d
               12  LOAD_ATTR                admin
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                form
               18  LOAD_ATTR                d
               20  LOAD_ATTR                password
               22  CALL_METHOD_2         2  ''
               24  POP_TOP          
               26  POP_BLOCK        
               28  JUMP_FORWARD        108  'to 108'
             30_0  COME_FROM_FINALLY     0  '0'

 L. 556        30  DUP_TOP          
               32  LOAD_GLOBAL              LDAPError
               34  COMPARE_OP               exception-match
               36  POP_JUMP_IF_FALSE   106  'to 106'
               38  POP_TOP          
               40  STORE_FAST               'ldap_err'
               42  POP_TOP          
               44  SETUP_FINALLY        94  'to 94'

 L. 557        46  LOAD_FAST                'self'
               48  LOAD_ATTR                logger
               50  LOAD_METHOD              error

 L. 558        52  LOAD_STR                 'Error opening user connection to %r as user %r: %s'

 L. 559        54  LOAD_FAST                'self'
               56  LOAD_ATTR                ldap_url
               58  LOAD_METHOD              connect_uri
               60  CALL_METHOD_0         0  ''

 L. 560        62  LOAD_FAST                'self'
               64  LOAD_ATTR                form
               66  LOAD_ATTR                d
               68  LOAD_ATTR                admin

 L. 557        70  CALL_METHOD_3         3  ''
               72  POP_TOP          

 L. 562        74  LOAD_FAST                'self'
               76  LOAD_ATTR                GET
               78  LOAD_STR                 'Admin login failed!'
               80  LOAD_CONST               ('message',)
               82  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               84  ROT_FOUR         
               86  POP_BLOCK        
               88  POP_EXCEPT       
               90  CALL_FINALLY         94  'to 94'
               92  RETURN_VALUE     
             94_0  COME_FROM            90  '90'
             94_1  COME_FROM_FINALLY    44  '44'
               94  LOAD_CONST               None
               96  STORE_FAST               'ldap_err'
               98  DELETE_FAST              'ldap_err'
              100  END_FINALLY      
              102  POP_EXCEPT       
              104  JUMP_FORWARD        108  'to 108'
            106_0  COME_FROM            36  '36'
              106  END_FINALLY      
            108_0  COME_FROM           104  '104'
            108_1  COME_FROM            28  '28'

 L. 563       108  LOAD_FAST                'self'
              110  LOAD_ATTR                form
              112  LOAD_ATTR                d
              114  LOAD_ATTR                serial
              116  STORE_FAST               'token_serial'

 L. 564       118  SETUP_FINALLY       346  'to 346'

 L. 565       120  LOAD_FAST                'self'
              122  LOAD_METHOD              search_token

 L. 566       124  LOAD_FAST                'token_serial'

 L. 565       126  CALL_METHOD_1         1  ''
              128  UNPACK_SEQUENCE_3     3 
              130  STORE_FAST               'token_displayname'
              132  STORE_FAST               'token_dn'
              134  STORE_FAST               'token_entry'

 L. 568       136  LOAD_FAST                'token_entry'
              138  LOAD_GLOBAL              ATTR_OWNER_DN
              140  BINARY_SUBSCR    
              142  LOAD_CONST               0
              144  BINARY_SUBSCR    
              146  STORE_FAST               'owner_dn'

 L. 569       148  LOAD_FAST                'self'
              150  LOAD_METHOD              read_owner
              152  LOAD_FAST                'owner_dn'
              154  CALL_METHOD_1         1  ''
              156  STORE_FAST               'owner_entry'

 L. 570       158  LOAD_FAST                'self'
              160  LOAD_METHOD              search_accounts
              162  LOAD_FAST                'token_dn'
              164  CALL_METHOD_1         1  ''
              166  STORE_FAST               'accounts'

 L. 571       168  LOAD_GLOBAL              hashlib
              170  LOAD_METHOD              sha256

 L. 572       172  LOAD_STR                 ' || '
              174  LOAD_METHOD              join

 L. 573       176  LOAD_GLOBAL              repr
              178  LOAD_FAST                'token_serial'
              180  CALL_FUNCTION_1       1  ''

 L. 574       182  LOAD_GLOBAL              repr
              184  LOAD_FAST                'owner_dn'
              186  CALL_FUNCTION_1       1  ''

 L. 575       188  LOAD_GLOBAL              repr
              190  LOAD_GLOBAL              sorted
              192  LOAD_FAST                'accounts'
              194  JUMP_IF_TRUE_OR_POP   198  'to 198'
              196  BUILD_LIST_0          0 
            198_0  COME_FROM           194  '194'
              198  CALL_FUNCTION_1       1  ''
              200  CALL_FUNCTION_1       1  ''

 L. 572       202  BUILD_TUPLE_3         3 
              204  CALL_METHOD_1         1  ''
              206  LOAD_METHOD              encode

 L. 576       208  LOAD_STR                 'ascii'

 L. 572       210  CALL_METHOD_1         1  ''

 L. 571       212  CALL_METHOD_1         1  ''
              214  LOAD_METHOD              hexdigest
              216  CALL_METHOD_0         0  ''
              218  STORE_FAST               'confirm_hash'

 L. 578       220  LOAD_FAST                'self'
              222  LOAD_ATTR                form
              224  LOAD_ATTR                d
              226  LOAD_ATTR                confirm
              228  LOAD_FAST                'confirm_hash'
              230  COMPARE_OP               !=
          232_234  POP_JUMP_IF_FALSE   292  'to 292'

 L. 579       236  LOAD_GLOBAL              RENDER
              238  LOAD_ATTR                reset_form

 L. 580       240  LOAD_STR                 'Please confirm token reset. Examine this information carefully!'

 L. 581       242  LOAD_FAST                'self'
              244  LOAD_ATTR                form
              246  LOAD_ATTR                d
              248  LOAD_ATTR                admin

 L. 582       250  LOAD_FAST                'self'
              252  LOAD_ATTR                form
              254  LOAD_ATTR                d
              256  LOAD_ATTR                serial

 L. 583       258  LOAD_FAST                'token_displayname'

 L. 584       260  LOAD_FAST                'owner_entry'
              262  LOAD_STR                 'displayName'
              264  BINARY_SUBSCR    
              266  LOAD_CONST               0
              268  BINARY_SUBSCR    

 L. 585       270  LOAD_FAST                'owner_entry'
              272  LOAD_STR                 'mail'
              274  BINARY_SUBSCR    
              276  LOAD_CONST               0
              278  BINARY_SUBSCR    

 L. 586       280  LOAD_FAST                'accounts'

 L. 587       282  LOAD_FAST                'confirm_hash'

 L. 579       284  LOAD_CONST               ('admin', 'serial', 'token', 'owner', 'email', 'accounts', 'confirm')
              286  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
              288  POP_BLOCK        
              290  RETURN_VALUE     
            292_0  COME_FROM           232  '232'

 L. 589       292  LOAD_GLOBAL              random_string
              294  LOAD_GLOBAL              PWD_TMP_CHARS
              296  LOAD_GLOBAL              PWD_LENGTH
              298  LOAD_GLOBAL              PWD_ADMIN_LEN
              300  BINARY_SUBTRACT  
              302  LOAD_CONST               ('alphabet', 'length')
              304  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              306  STORE_FAST               'enroll_pw1'

 L. 590       308  LOAD_GLOBAL              random_string
              310  LOAD_GLOBAL              PWD_TMP_CHARS
              312  LOAD_GLOBAL              PWD_ADMIN_LEN
              314  LOAD_CONST               ('alphabet', 'length')
              316  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              318  STORE_FAST               'enroll_pw2'

 L. 591       320  LOAD_FAST                'enroll_pw1'
              322  LOAD_FAST                'enroll_pw2'
              324  BINARY_ADD       
              326  STORE_FAST               'enroll_pw'

 L. 592       328  LOAD_FAST                'self'
              330  LOAD_METHOD              update_token
              332  LOAD_FAST                'token_dn'
              334  LOAD_FAST                'token_entry'
              336  LOAD_FAST                'enroll_pw'
              338  CALL_METHOD_3         3  ''
              340  POP_TOP          
              342  POP_BLOCK        
              344  JUMP_FORWARD        542  'to 542'
            346_0  COME_FROM_FINALLY   118  '118'

 L. 593       346  DUP_TOP          
              348  LOAD_GLOBAL              ldap0
              350  LOAD_ATTR                err
              352  LOAD_ATTR                NoUniqueEntry
              354  COMPARE_OP               exception-match
          356_358  POP_JUMP_IF_FALSE   412  'to 412'
              360  POP_TOP          
              362  STORE_FAST               'ldap_err'
              364  POP_TOP          
              366  SETUP_FINALLY       398  'to 398'

 L. 594       368  LOAD_FAST                'self'
              370  LOAD_ATTR                logger
              372  LOAD_METHOD              warning
              374  LOAD_STR                 'LDAPError: %s'
              376  LOAD_FAST                'ldap_err'
              378  CALL_METHOD_2         2  ''
              380  POP_TOP          

 L. 595       382  LOAD_FAST                'self'
              384  LOAD_ATTR                GET
              386  LOAD_STR                 'Serial no. not found!'
              388  LOAD_CONST               ('message',)
              390  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              392  STORE_FAST               'res'
              394  POP_BLOCK        
              396  BEGIN_FINALLY    
            398_0  COME_FROM_FINALLY   366  '366'
              398  LOAD_CONST               None
              400  STORE_FAST               'ldap_err'
              402  DELETE_FAST              'ldap_err'
              404  END_FINALLY      
              406  POP_EXCEPT       
          408_410  JUMP_FORWARD        706  'to 706'
            412_0  COME_FROM           356  '356'

 L. 596       412  DUP_TOP          
              414  LOAD_GLOBAL              LDAPError
              416  COMPARE_OP               exception-match
          418_420  POP_JUMP_IF_FALSE   476  'to 476'
              422  POP_TOP          
              424  STORE_FAST               'ldap_err'
              426  POP_TOP          
              428  SETUP_FINALLY       464  'to 464'

 L. 597       430  LOAD_FAST                'self'
              432  LOAD_ATTR                logger
              434  LOAD_ATTR                error
              436  LOAD_STR                 'LDAPError: %s'
              438  LOAD_FAST                'ldap_err'
              440  LOAD_CONST               True
              442  LOAD_CONST               ('exc_info',)
              444  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              446  POP_TOP          

 L. 598       448  LOAD_FAST                'self'
              450  LOAD_ATTR                GET
              452  LOAD_STR                 'Internal LDAP error!'
              454  LOAD_CONST               ('message',)
              456  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              458  STORE_FAST               'res'
              460  POP_BLOCK        
              462  BEGIN_FINALLY    
            464_0  COME_FROM_FINALLY   428  '428'
              464  LOAD_CONST               None
              466  STORE_FAST               'ldap_err'
              468  DELETE_FAST              'ldap_err'
              470  END_FINALLY      
              472  POP_EXCEPT       
              474  JUMP_FORWARD        706  'to 706'
            476_0  COME_FROM           418  '418'

 L. 599       476  DUP_TOP          
              478  LOAD_GLOBAL              Exception
              480  COMPARE_OP               exception-match
          482_484  POP_JUMP_IF_FALSE   540  'to 540'
              486  POP_TOP          
              488  STORE_FAST               'err'
              490  POP_TOP          
              492  SETUP_FINALLY       528  'to 528'

 L. 600       494  LOAD_FAST                'self'
              496  LOAD_ATTR                logger
              498  LOAD_ATTR                error
              500  LOAD_STR                 'Unhandled exception: %s'
              502  LOAD_FAST                'err'
              504  LOAD_CONST               True
              506  LOAD_CONST               ('exc_info',)
              508  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              510  POP_TOP          

 L. 601       512  LOAD_FAST                'self'
              514  LOAD_ATTR                GET
              516  LOAD_STR                 'Internal error!'
              518  LOAD_CONST               ('message',)
              520  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              522  STORE_FAST               'res'
              524  POP_BLOCK        
              526  BEGIN_FINALLY    
            528_0  COME_FROM_FINALLY   492  '492'
              528  LOAD_CONST               None
              530  STORE_FAST               'err'
              532  DELETE_FAST              'err'
              534  END_FINALLY      
              536  POP_EXCEPT       
              538  JUMP_FORWARD        706  'to 706'
            540_0  COME_FROM           482  '482'
              540  END_FINALLY      
            542_0  COME_FROM           344  '344'

 L. 604       542  SETUP_FINALLY       568  'to 568'

 L. 605       544  LOAD_FAST                'self'
              546  LOAD_METHOD              _send_pw
              548  LOAD_FAST                'self'
              550  LOAD_ATTR                form
              552  LOAD_ATTR                d
              554  LOAD_ATTR                serial
              556  LOAD_FAST                'owner_entry'
              558  LOAD_FAST                'enroll_pw1'
              560  CALL_METHOD_3         3  ''
              562  POP_TOP          
              564  POP_BLOCK        
              566  JUMP_FORWARD        646  'to 646'
            568_0  COME_FROM_FINALLY   542  '542'

 L. 606       568  DUP_TOP          
              570  LOAD_GLOBAL              socket
              572  LOAD_ATTR                error
              574  LOAD_GLOBAL              socket
              576  LOAD_ATTR                gaierror
              578  LOAD_GLOBAL              smtplib
              580  LOAD_ATTR                SMTPException
              582  BUILD_TUPLE_3         3 
              584  COMPARE_OP               exception-match
          586_588  POP_JUMP_IF_FALSE   644  'to 644'
              590  POP_TOP          
              592  STORE_FAST               'mail_error'
              594  POP_TOP          
              596  SETUP_FINALLY       632  'to 632'

 L. 607       598  LOAD_FAST                'self'
              600  LOAD_ATTR                logger
              602  LOAD_ATTR                error
              604  LOAD_STR                 'Error sending e-mail: %s'
              606  LOAD_FAST                'mail_error'
              608  LOAD_CONST               True
              610  LOAD_CONST               ('exc_info',)
              612  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              614  POP_TOP          

 L. 608       616  LOAD_FAST                'self'
              618  LOAD_ATTR                GET
              620  LOAD_STR                 'Error sending e-mail via SMTP!'
              622  LOAD_CONST               ('message',)
              624  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              626  STORE_FAST               'res'
              628  POP_BLOCK        
              630  BEGIN_FINALLY    
            632_0  COME_FROM_FINALLY   596  '596'
              632  LOAD_CONST               None
              634  STORE_FAST               'mail_error'
              636  DELETE_FAST              'mail_error'
              638  END_FINALLY      
              640  POP_EXCEPT       
              642  JUMP_FORWARD        706  'to 706'
            644_0  COME_FROM           586  '586'
              644  END_FINALLY      
            646_0  COME_FROM           566  '566'

 L. 610       646  LOAD_FAST                'self'
              648  LOAD_ATTR                logger
              650  LOAD_METHOD              info
              652  LOAD_STR                 'Finished resetting token %r.'
              654  LOAD_FAST                'token_dn'
              656  CALL_METHOD_2         2  ''
              658  POP_TOP          

 L. 611       660  LOAD_GLOBAL              RENDER
              662  LOAD_ATTR                reset_action

 L. 612       664  LOAD_STR                 'Token was reset'

 L. 613       666  LOAD_FAST                'token_serial'

 L. 614       668  LOAD_FAST                'token_entry'
              670  LOAD_STR                 'displayName'
              672  BINARY_SUBSCR    
              674  LOAD_CONST               0
              676  BINARY_SUBSCR    

 L. 615       678  LOAD_FAST                'owner_entry'
              680  LOAD_STR                 'displayName'
              682  BINARY_SUBSCR    
              684  LOAD_CONST               0
              686  BINARY_SUBSCR    

 L. 616       688  LOAD_FAST                'owner_entry'
              690  LOAD_STR                 'mail'
              692  BINARY_SUBSCR    
              694  LOAD_CONST               0
              696  BINARY_SUBSCR    

 L. 617       698  LOAD_FAST                'enroll_pw2'

 L. 611       700  LOAD_CONST               ('serial', 'token', 'owner', 'email', 'enrollpw2')
              702  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              704  STORE_FAST               'res'
            706_0  COME_FROM           642  '642'
            706_1  COME_FROM           538  '538'
            706_2  COME_FROM           474  '474'
            706_3  COME_FROM           408  '408'

 L. 619       706  LOAD_FAST                'res'
              708  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 86


application = web.application(URL2CLASS_MAPPING, (globals()), autoreload=(bool(WEB_ERROR))).wsgifunc()