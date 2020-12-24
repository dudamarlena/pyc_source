# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /aedir_pproc/pwsync.py
# Compiled at: 2020-04-01 11:05:46
# Size of source mod 2**32: 19800 bytes
"""
aedir_pproc.pwsync - slapd-sock listener for password synchronisation

This demon intercepts password changes (Password modify extended operation)
and sends the clear-text password to e.g. MS AD
"""
import logging, os, sys, queue, threading, time
from collections import OrderedDict
import passlib.context
from pyasn1.type.univ import OctetString, Sequence
from pyasn1.type.namedtype import NamedTypes, OptionalNamedType
from pyasn1.type.tag import Tag, tagClassContext, tagFormatSimple
import pyasn1.codec.ber as pyasn1_decoder
from pyasn1.error import PyAsn1Error
import ldap0
from ldap0.res import SearchResultEntry
from ldap0.dn import DNObj
import ldap0.functions as ldap_strf_secs
from ldap0.ldapurl import LDAPUrl
from ldap0.lock import LDAPLock
from ldap0.pw import unicode_pwd
from ldap0.ldapobject import ReconnectLDAPObject
from slapdsock.ldaphelper import LocalLDAPConn
from slapdsock.loghelper import combined_logger
from slapdsock.handler import SlapdSockHandler
from slapdsock.service import SlapdSockThreadingServer
from .__about__ import __version__
ALLOWED_UIDS = [
 0, 'ae-dir-slapd']
ALLOWED_GIDS = [0]
SOCKET_PERMISSIONS = '0666'
LDAP0_TRACE_LEVEL = int(os.environ.get('LDAP0_TRACE_LEVEL', 0))
LDAP_MAXRETRYCOUNT = 10
LDAP_RETRYDELAY = 0.1
LDAP_SASL_AUTHZID = None
LDAP_CACHE_TTL = 5.0
LDAP_LONG_CACHE_TTL = 20 * LDAP_CACHE_TTL
LDAP_TIMEOUT = 3.0
LDAP_USERNAME_ATTR = 'uid'
SOCKET_TIMEOUT = 2 * LDAP_TIMEOUT
SYS_LOG_FORMAT = '%(name)s %(levelname)s %(message)s'
CONSOLE_LOG_FORMAT = '%(name)s %(asctime)s %(levelname)s %(message)s'
AVERAGE_COUNT = 100
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
CACHE_TTL = -1.0
DEBUG_VARS = [
 'user_dn']
DEBUG_VARS.extend([
 'old_passwd',
 'new_passwd'])

class DictQueue(queue.Queue):
    __doc__ = '\n    modified Queue class which internally stores items in a dict\n    '

    def _init(self, maxsize):
        self.queue = OrderedDict()

    def _put(self, item):
        key, value = item
        self.queue[key] = value

    def _get(self):
        key, value = self.queue.popitem()
        return (key, value)


class PWSyncWorker(threading.Thread, LocalLDAPConn):
    __doc__ = '\n    Thread class for the password synchronization worker\n    '
    passwd_update_delay = 1.0
    source_id_attr = 'uid'
    target_filter_format = '({0}={1})'
    target_id_attr = 'uid'
    target_password_attr = 'userPassword'
    target_password_encoding = 'utf-8'

    def __init__(self, target_ldap_url, que):
        self._target_ldap_url = target_ldap_url
        if target_ldap_url.attrs is not None:
            if len(target_ldap_url.attrs) == 2:
                self.target_id_attr, self.target_password_attr = target_ldap_url.attrs
        self.logger = combined_logger((self.__class__.__name__),
          LOG_LEVEL,
          sys_log_format=SYS_LOG_FORMAT,
          console_log_format=CONSOLE_LOG_FORMAT)
        self._queue = que
        threading.Thread.__init__(self, name=(self.__class__.__module__ + self.__class__.__name__))
        LocalLDAPConn.__init__(self, self.logger)
        self._target_conn = None
        self._target_conn_lock = LDAPLock(desc=('target_conn() in %s' % repr(self.__class__)))

    def target_conn(self):
        """
        open and cache target connection
        """
        if isinstance(self._target_conn, ReconnectLDAPObject):
            self.logger.debug('Existing LDAP connection to %s (%s)', repr(self._target_conn.uri), repr(self._target_conn))
            return self._target_conn
        try:
            self.logger.debug('Open connection to %r as %r', self._target_ldap_url.connect_uri(), self._target_ldap_url.who)
            self._target_conn_lock.acquire()
            try:
                self._target_conn = ReconnectLDAPObject((self._target_ldap_url.connect_uri()),
                  trace_level=LDAP0_TRACE_LEVEL,
                  cache_ttl=LDAP_CACHE_TTL,
                  retry_max=LDAP_MAXRETRYCOUNT,
                  retry_delay=LDAP_RETRYDELAY)
                self._target_conn.simple_bind_s(self._target_ldap_url.who or '', (self._target_ldap_url.cred or '').encode('utf-8'))
            except ldap0.LDAPError as ldap_error:
                try:
                    self._target_conn = None
                    self.logger.error('LDAPError during connecting to %r: %s', self.ldapi_uri, ldap_error)
                    raise ldap_error
                finally:
                    ldap_error = None
                    del ldap_error

            else:
                self._target_conn.authz_id = self._target_conn.whoami_s()
                self.logger.info('Successfully bound to %s as %s', self._target_conn.uri, self._target_conn.authz_id)
        finally:
            self._target_conn_lock.release()

        return self._target_conn

    def _check_password--- This code section failed: ---

 L. 224         0  LOAD_FAST                'self'
                2  LOAD_ATTR                logger
                4  LOAD_METHOD              debug
                6  LOAD_STR                 'Check password of %r'
                8  LOAD_FAST                'user_dn'
               10  CALL_METHOD_2         2  ''
               12  POP_TOP          

 L. 225        14  LOAD_FAST                'self'
               16  LOAD_METHOD              get_ldapi_conn
               18  CALL_METHOD_0         0  ''
               20  STORE_FAST               'ldapi_conn'

 L. 226        22  SETUP_FINALLY        44  'to 44'

 L. 227        24  LOAD_FAST                'ldapi_conn'
               26  LOAD_ATTR                read_s

 L. 228        28  LOAD_FAST                'user_dn'

 L. 229        30  LOAD_STR                 'userPassword'
               32  BUILD_LIST_1          1 

 L. 227        34  LOAD_CONST               ('attrlist',)
               36  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               38  STORE_FAST               'user_entry'
               40  POP_BLOCK        
               42  JUMP_FORWARD        102  'to 102'
             44_0  COME_FROM_FINALLY    22  '22'

 L. 231        44  DUP_TOP          
               46  LOAD_GLOBAL              ldap0
               48  LOAD_ATTR                LDAPError
               50  COMPARE_OP               exception-match
               52  POP_JUMP_IF_FALSE   100  'to 100'
               54  POP_TOP          
               56  STORE_FAST               'ldap_error'
               58  POP_TOP          
               60  SETUP_FINALLY        88  'to 88'

 L. 232        62  LOAD_FAST                'self'
               64  LOAD_ATTR                logger
               66  LOAD_METHOD              warning
               68  LOAD_STR                 'LDAPError checking password of %r: %s'
               70  LOAD_FAST                'user_dn'
               72  LOAD_FAST                'ldap_error'
               74  CALL_METHOD_3         3  ''
               76  POP_TOP          

 L. 233        78  POP_BLOCK        
               80  POP_EXCEPT       
               82  CALL_FINALLY         88  'to 88'
               84  LOAD_CONST               False
               86  RETURN_VALUE     
             88_0  COME_FROM            82  '82'
             88_1  COME_FROM_FINALLY    60  '60'
               88  LOAD_CONST               None
               90  STORE_FAST               'ldap_error'
               92  DELETE_FAST              'ldap_error'
               94  END_FINALLY      
               96  POP_EXCEPT       
               98  JUMP_FORWARD        102  'to 102'
            100_0  COME_FROM            52  '52'
              100  END_FINALLY      
            102_0  COME_FROM            98  '98'
            102_1  COME_FROM            42  '42'

 L. 234       102  LOAD_FAST                'user_entry'
              104  POP_JUMP_IF_TRUE    124  'to 124'

 L. 235       106  LOAD_FAST                'self'
              108  LOAD_ATTR                logger
              110  LOAD_METHOD              warning
              112  LOAD_STR                 'No search result reading %r'
              114  LOAD_FAST                'user_dn'
              116  CALL_METHOD_2         2  ''
              118  POP_TOP          

 L. 236       120  LOAD_CONST               False
              122  RETURN_VALUE     
            124_0  COME_FROM           104  '104'

 L. 237       124  SETUP_FINALLY       160  'to 160'

 L. 238       126  LOAD_GLOBAL              ldap0
              128  LOAD_ATTR                cidict
              130  LOAD_METHOD              CIDict
              132  LOAD_FAST                'user_entry'
              134  LOAD_ATTR                entry_as
              136  CALL_METHOD_1         1  ''
              138  LOAD_STR                 'userPassword'
              140  BINARY_SUBSCR    
              142  LOAD_CONST               0
              144  BINARY_SUBSCR    
              146  LOAD_CONST               7
              148  LOAD_CONST               None
              150  BUILD_SLICE_2         2 
              152  BINARY_SUBSCR    
              154  STORE_FAST               'user_password_hash'
              156  POP_BLOCK        
              158  JUMP_FORWARD        200  'to 200'
            160_0  COME_FROM_FINALLY   124  '124'

 L. 239       160  DUP_TOP          
              162  LOAD_GLOBAL              KeyError
              164  LOAD_GLOBAL              IndexError
              166  BUILD_TUPLE_2         2 
              168  COMPARE_OP               exception-match
              170  POP_JUMP_IF_FALSE   198  'to 198'
              172  POP_TOP          
              174  POP_TOP          
              176  POP_TOP          

 L. 240       178  LOAD_FAST                'self'
              180  LOAD_ATTR                logger
              182  LOAD_METHOD              warning
              184  LOAD_STR                 'No userPassword in %r'
              186  LOAD_FAST                'user_dn'
              188  CALL_METHOD_2         2  ''
              190  POP_TOP          

 L. 241       192  POP_EXCEPT       
              194  LOAD_CONST               False
              196  RETURN_VALUE     
            198_0  COME_FROM           170  '170'
              198  END_FINALLY      
            200_0  COME_FROM           158  '158'

 L. 243       200  LOAD_FAST                'self'
              202  LOAD_ATTR                logger
              204  LOAD_METHOD              debug
              206  LOAD_STR                 'user_password_hash = %r'
              208  LOAD_FAST                'user_password_hash'
              210  CALL_METHOD_2         2  ''
              212  POP_TOP          

 L. 245       214  LOAD_GLOBAL              passlib
              216  LOAD_ATTR                context
              218  LOAD_ATTR                CryptContext
              220  LOAD_STR                 'sha512_crypt'
              222  BUILD_LIST_1          1 
              224  LOAD_CONST               ('schemes',)
              226  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              228  STORE_FAST               'pw_context'

 L. 246       230  LOAD_FAST                'pw_context'
              232  LOAD_METHOD              verify
              234  LOAD_FAST                'new_passwd'
              236  LOAD_FAST                'user_password_hash'
              238  CALL_METHOD_2         2  ''
              240  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 82

    def get_target_id(self, source_dn):
        """
        determine target identifier based on user's source DN
        """
        self.logger.debug('Determine target ID for %r', source_dn)
        rdn_attr_type, uid = list(DNObj.from_str(source_dn).rdn_attrs().items())[0]
        if rdn_attr_type.lower() != self.source_id_attr:
            self.logger.warning('RDN attribute %r is not %r => ignore password change of %r', rdn_attr_type, self.source_id_attr, source_dn)
            return None
        self.logger.debug('Extracted %s=%r from source_dn=%r', self.source_id_attr, uid, source_dn)
        target_filter = self.target_filter_format.format(self.target_id_attr, uid)
        self.logger.debug('Searching target entry with %r', target_filter)
        target_conn = self.target_conn()
        ldap_result = target_conn.search_s((self._target_ldap_url.dn),
          (self._target_ldap_url.scope or ldap0.SCOPE_SUBTREE),
          target_filter,
          attrlist=[
         '1.1'],
          sizelimit=8)
        ldap_result = [res for res in ldap_result if isinstance(res, SearchResultEntry)]
        self.logger.debug('ldap_result=%r', ldap_result)
        if len(ldap_result) != 1:
            return
        return ldap_result[0].dn_s

    def _encode_target_password(self, password):
        """
        encode argument password for target system
        """
        if self.target_password_attr.lower() == 'unicodepwd':
            return unicode_pwd(password.encode('utf-8'))
        return password.encode(self.target_password_encoding)

    def _update_target_password(self, target_id, old_passwd, new_passwd, req_time):
        """
        write new password to target
        """
        target_conn = self.target_conn()
        target_conn.modify_s(target_id, [
         (
          ldap0.MOD_REPLACE,
          self.target_password_attr.encode('ascii'),
          [
           self._encode_target_password(new_passwd)])])

    def run--- This code section failed: ---

 L. 315         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _queue
                4  LOAD_METHOD              get
                6  CALL_METHOD_0         0  ''
                8  UNPACK_SEQUENCE_2     2 
               10  STORE_FAST               'user_dn'
               12  STORE_FAST               'val'

 L. 316        14  LOAD_FAST                'val'
               16  UNPACK_SEQUENCE_3     3 
               18  STORE_FAST               'old_passwd'
               20  STORE_FAST               'new_passwd'
               22  STORE_FAST               'req_time'

 L. 317        24  LOAD_FAST                'self'
               26  LOAD_ATTR                logger
               28  LOAD_METHOD              debug

 L. 318        30  LOAD_STR                 'Received password change for %r (at %s)'

 L. 319        32  LOAD_FAST                'user_dn'

 L. 320        34  LOAD_GLOBAL              ldap_strf_secs
               36  LOAD_FAST                'req_time'
               38  CALL_FUNCTION_1       1  ''

 L. 317        40  CALL_METHOD_3         3  ''
               42  POP_TOP          

 L. 322        44  SETUP_FINALLY       198  'to 198'

 L. 323        46  LOAD_GLOBAL              max

 L. 324        48  LOAD_CONST               0

 L. 325        50  LOAD_GLOBAL              time
               52  LOAD_METHOD              time
               54  CALL_METHOD_0         0  ''
               56  LOAD_FAST                'req_time'
               58  BINARY_SUBTRACT  
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                passwd_update_delay
               64  BINARY_ADD       

 L. 323        66  CALL_FUNCTION_2       2  ''
               68  STORE_FAST               'sleep_time'

 L. 327        70  LOAD_FAST                'self'
               72  LOAD_ATTR                logger
               74  LOAD_METHOD              debug

 L. 328        76  LOAD_STR                 'Deferring syncing password for %r for %f secs'

 L. 329        78  LOAD_FAST                'user_dn'

 L. 330        80  LOAD_FAST                'sleep_time'

 L. 327        82  CALL_METHOD_3         3  ''
               84  POP_TOP          

 L. 332        86  LOAD_GLOBAL              time
               88  LOAD_METHOD              sleep
               90  LOAD_FAST                'sleep_time'
               92  CALL_METHOD_1         1  ''
               94  POP_TOP          

 L. 333        96  LOAD_FAST                'self'
               98  LOAD_METHOD              _check_password
              100  LOAD_FAST                'user_dn'
              102  LOAD_FAST                'new_passwd'
              104  CALL_METHOD_2         2  ''
              106  POP_JUMP_IF_TRUE    126  'to 126'

 L. 335       108  LOAD_FAST                'self'
              110  LOAD_ATTR                logger
              112  LOAD_METHOD              warning
              114  LOAD_STR                 'Ignoring wrong password for %r'
              116  LOAD_FAST                'user_dn'
              118  CALL_METHOD_2         2  ''
              120  POP_TOP          

 L. 336       122  POP_BLOCK        
              124  JUMP_BACK             0  'to 0'
            126_0  COME_FROM           106  '106'

 L. 337       126  LOAD_FAST                'self'
              128  LOAD_METHOD              get_target_id
              130  LOAD_FAST                'user_dn'
              132  CALL_METHOD_1         1  ''
              134  STORE_FAST               'target_id'

 L. 338       136  LOAD_FAST                'target_id'
              138  LOAD_CONST               None
              140  COMPARE_OP               is
              142  POP_JUMP_IF_FALSE   162  'to 162'

 L. 340       144  LOAD_FAST                'self'
              146  LOAD_ATTR                logger
              148  LOAD_METHOD              warning

 L. 341       150  LOAD_STR                 'No target ID found for %r => ignore password change'

 L. 342       152  LOAD_FAST                'user_dn'

 L. 340       154  CALL_METHOD_2         2  ''
              156  POP_TOP          

 L. 344       158  POP_BLOCK        
              160  JUMP_BACK             0  'to 0'
            162_0  COME_FROM           142  '142'

 L. 345       162  LOAD_FAST                'self'
              164  LOAD_ATTR                logger
              166  LOAD_METHOD              debug
              168  LOAD_STR                 'Try to sync password for %r to %r'
              170  LOAD_FAST                'user_dn'
              172  LOAD_FAST                'target_id'
              174  CALL_METHOD_3         3  ''
              176  POP_TOP          

 L. 346       178  LOAD_FAST                'self'
              180  LOAD_METHOD              _update_target_password
              182  LOAD_FAST                'target_id'
              184  LOAD_FAST                'old_passwd'
              186  LOAD_FAST                'new_passwd'
              188  LOAD_FAST                'req_time'
              190  CALL_METHOD_4         4  ''
              192  POP_TOP          
              194  POP_BLOCK        
              196  JUMP_FORWARD        236  'to 236'
            198_0  COME_FROM_FINALLY    44  '44'

 L. 347       198  DUP_TOP          
              200  LOAD_GLOBAL              Exception
              202  COMPARE_OP               exception-match
              204  POP_JUMP_IF_FALSE   234  'to 234'
              206  POP_TOP          
              208  POP_TOP          
              210  POP_TOP          

 L. 348       212  LOAD_FAST                'self'
              214  LOAD_ATTR                logger
              216  LOAD_ATTR                error

 L. 349       218  LOAD_STR                 'Error syncing password for %r:\n'

 L. 350       220  LOAD_FAST                'user_dn'

 L. 351       222  LOAD_CONST               True

 L. 348       224  LOAD_CONST               ('exc_info',)
              226  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              228  POP_TOP          
              230  POP_EXCEPT       
              232  JUMP_FORWARD        252  'to 252'
            234_0  COME_FROM           204  '204'
              234  END_FINALLY      
            236_0  COME_FROM           196  '196'

 L. 354       236  LOAD_FAST                'self'
              238  LOAD_ATTR                logger
              240  LOAD_METHOD              info
              242  LOAD_STR                 'Synced password for %r to %r'
              244  LOAD_FAST                'user_dn'
              246  LOAD_FAST                'target_id'
              248  CALL_METHOD_3         3  ''
              250  POP_TOP          
            252_0  COME_FROM           232  '232'

 L. 355       252  LOAD_FAST                'self'
              254  LOAD_ATTR                _queue
              256  LOAD_METHOD              task_done
              258  CALL_METHOD_0         0  ''
              260  POP_TOP          
              262  JUMP_BACK             0  'to 0'

Parse error at or near `COME_FROM' instruction at offset 126_0


class PasswdModifyRequestValue(Sequence):
    __doc__ = '\n    PasswdModifyRequestValue ::= SEQUENCE {\n        userIdentity [0] OCTET STRING OPTIONAL\n        oldPasswd [1] OCTET STRING OPTIONAL\n        newPasswd [2] OCTET STRING OPTIONAL }\n    '

    class UserIdentity(OctetString):
        __doc__ = '\n        userIdentity [0] OCTET STRING OPTIONAL\n        '
        tagSet = OctetString.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 0))

    class OldPasswd(OctetString):
        __doc__ = '\n        oldPasswd [1] OCTET STRING OPTIONAL\n        '
        tagSet = OctetString.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 1))

    class NewPasswd(OctetString):
        __doc__ = '\n        newPasswd [2] OCTET STRING OPTIONAL\n        '
        tagSet = OctetString.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 2))

    componentType = NamedTypes(OptionalNamedType('userIdentity', UserIdentity()), OptionalNamedType('oldPasswd', OldPasswd('')), OptionalNamedType('newPasswd', NewPasswd('')))


class PassModHandler(SlapdSockHandler):
    __doc__ = '\n    Handler class which extracts new userPassword value\n    from EXTENDED operation\n    '

    def do_extended(self, request):
        """
        Handle EXTENDED operation
        """
        if request.oid != '1.3.6.1.4.1.4203.1.11.1':
            return 'CONTINUE'
        try:
            decoded_value, _ = pyasn1_decoder.decode((request.value),
              asn1Spec=(PasswdModifyRequestValue()))
            try:
                user_dn = str(decoded_value.getComponentByName('userIdentity'))
            except PyAsn1Error:
                user_dn = request.binddn
            else:
                self._log(logging.INFO, 'Intercepted PASSMOD operation for %r', user_dn)
                old_passwd = str(decoded_value.getComponentByName('oldPasswd')) or None
                new_passwd = str(decoded_value.getComponentByName('newPasswd')) or None
        except Exception as err:
            try:
                self._log((logging.ERROR),
                  'Unhandled exception processing PASSMOD request: %r',
                  err,
                  exc_info=True)
            finally:
                err = None
                del err

        else:
            self.server.pwsync_queue.put((
             user_dn,
             (
              old_passwd, new_passwd, time.time())))
        return 'CONTINUE'


class PassModServer(SlapdSockThreadingServer):
    __doc__ = '\n    This is used to pass in more parameters to the server instance\n    '
    ldapi_authz_id = LDAP_SASL_AUTHZID
    ldap_retry_max = LDAP_MAXRETRYCOUNT
    ldap_retry_delay = LDAP_RETRYDELAY
    ldap_cache_ttl = LDAP_CACHE_TTL

    def __init__(self, server_address, RequestHandlerClass, average_count, socket_timeout, socket_permissions, allowed_uids, allowed_gids, pwsync_queue, bind_and_activate=True, log_vars=None):
        self._ldap_conn = None
        self.pwsync_queue = pwsync_queue
        SlapdSockThreadingServer.__init__(self,
          server_address,
          RequestHandlerClass,
          combined_logger((self.__class__.__name__),
          LOG_LEVEL,
          sys_log_format=SYS_LOG_FORMAT,
          console_log_format=CONSOLE_LOG_FORMAT),
          average_count,
          socket_timeout,
          socket_permissions,
          allowed_uids,
          allowed_gids,
          bind_and_activate,
          monitor_dn=None,
          log_vars=log_vars)


def run():
    """
    The main script
    """
    script_name = os.path.abspath(sys.argv[0])
    pwsync_queue = DictQueue()
    log_level = LOG_LEVEL
    console_log_format = None
    if os.environ.get('DEBUG', 'no') == 'yes':
        log_level = logging.DEBUG
        console_log_format = CONSOLE_LOG_FORMAT
    my_logger = combined_logger((os.path.basename(script_name)),
      log_level,
      sys_log_format=SYS_LOG_FORMAT,
      console_log_format=console_log_format)
    my_logger.info('Starting %s %s (log level %d)', script_name, __version__, my_logger.level)
    my_logger.error("!!! Running in debug mode (log level %d)! Secret data will be logged! Don't do that!!!", my_logger.level)
    try:
        socket_path = sys.argv[1]
        local_ldap_uri = sys.argv[2]
        target_ldap_url = sys.argv[3]
        target_password_filename = sys.argv[4]
    except IndexError:
        my_logger.error('Not enough arguments => abort')
        sys.exit(1)
    else:
        try:
            local_ldap_uri_obj = LDAPUrl(local_ldap_uri)
            target_ldap_url_obj = LDAPUrl(target_ldap_url)
        except ValueError as err:
            try:
                my_logger.error('%s  => abort', err)
                sys.exit(1)
            finally:
                err = None
                del err

        else:
            cacert_filename = ldap0.get_option(ldap0.OPT_X_TLS_CACERTFILE)
            if not cacert_filename:
                my_logger.error('No CA certificate file defined => abort')
                sys.exit(1)
            try:
                with open(cacert_filename, 'r') as (cacert_file):
                    cacert = cacert_file.read()
            except IOError as err:
                try:
                    my_logger.error('Error reading CA cert file %r: %s => abort', cacert_filename, err)
                    sys.exit(1)
                finally:
                    err = None
                    del err

            else:
                my_logger.debug('Using CA cert file %r (%d bytes)', cacert_filename, len(cacert))
            try:
                with open(target_password_filename, 'r', encoding='utf-8') as (target_password_file):
                    target_ldap_url_obj.cred = target_password_file.read()
            except IOError as err:
                try:
                    my_logger.error('Error reading target password file %r: %s => abort', target_password_filename, err)
                    sys.exit(1)
                finally:
                    err = None
                    del err

            else:
                my_logger.debug('Using target password file %r', target_password_filename)
            pwsync_worker = PWSyncWorker(target_ldap_url_obj, pwsync_queue)
            pwsync_worker.ldapi_uri = local_ldap_uri_obj.connect_uri()
            pwsync_worker.setDaemon(True)
            pwsync_worker.start()
            try:
                slapd_sock_listener = PassModServer(socket_path,
                  PassModHandler,
                  AVERAGE_COUNT,
                  SOCKET_TIMEOUT,
                  SOCKET_PERMISSIONS, ALLOWED_UIDS,
                  ALLOWED_GIDS, pwsync_queue,
                  log_vars=DEBUG_VARS)
                slapd_sock_listener.ldapi_uri = local_ldap_uri_obj.connect_uri()
                slapd_sock_listener.ldap_trace_level = LDAP0_TRACE_LEVEL
                try:
                    slapd_sock_listener.serve_forever()
                except KeyboardInterrupt:
                    my_logger.warning('Received interrupt signal => shutdown')

            finally:
                my_logger.debug('Remove socket path %s', repr(socket_path))
                try:
                    os.remove(socket_path)
                except OSError:
                    pass


if __name__ == '__main__':
    run()