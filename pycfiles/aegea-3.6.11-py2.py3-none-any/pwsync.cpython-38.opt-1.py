# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /aedir_pproc/pwsync.py
# Compiled at: 2020-04-01 11:05:46
# Size of source mod 2**32: 19800 bytes
__doc__ = '\naedir_pproc.pwsync - slapd-sock listener for password synchronisation\n\nThis demon intercepts password changes (Password modify extended operation)\nand sends the clear-text password to e.g. MS AD\n'
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
    """DictQueue"""

    def _init(self, maxsize):
        self.queue = OrderedDict()

    def _put(self, item):
        key, value = item
        self.queue[key] = value

    def _get(self):
        key, value = self.queue.popitem()
        return (
         key, value)


class PWSyncWorker(threading.Thread, LocalLDAPConn):
    """PWSyncWorker"""
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
                self._target_conn.simple_bind_s(self._target_ldap_url.who or , (self._target_ldap_url.cred or ).encode('utf-8'))
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
            return
        self.logger.debug('Extracted %s=%r from source_dn=%r', self.source_id_attr, uid, source_dn)
        target_filter = self.target_filter_format.format(self.target_id_attr, uid)
        self.logger.debug('Searching target entry with %r', target_filter)
        target_conn = self.target_conn()
        ldap_result = target_conn.search_s((self._target_ldap_url.dn),
          (self._target_ldap_url.scope or ),
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
    """PasswdModifyRequestValue"""

    class UserIdentity(OctetString):
        """PasswdModifyRequestValue.UserIdentity"""
        tagSet = OctetString.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 0))

    class OldPasswd(OctetString):
        """PasswdModifyRequestValue.OldPasswd"""
        tagSet = OctetString.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 1))

    class NewPasswd(OctetString):
        """PasswdModifyRequestValue.NewPasswd"""
        tagSet = OctetString.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 2))

    componentType = NamedTypes(OptionalNamedType('userIdentity', UserIdentity()), OptionalNamedType('oldPasswd', OldPasswd('')), OptionalNamedType('newPasswd', NewPasswd('')))


class PassModHandler(SlapdSockHandler):
    """PassModHandler"""

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
                old_passwd = str(decoded_value.getComponentByName('oldPasswd')) or 
                new_passwd = str(decoded_value.getComponentByName('newPasswd')) or 
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
    """PassModServer"""
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


def run--- This code section failed: ---

 L. 493         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              abspath
                6  LOAD_GLOBAL              sys
                8  LOAD_ATTR                argv
               10  LOAD_CONST               0
               12  BINARY_SUBSCR    
               14  CALL_METHOD_1         1  ''
               16  STORE_FAST               'script_name'

 L. 494        18  LOAD_GLOBAL              DictQueue
               20  CALL_FUNCTION_0       0  ''
               22  STORE_FAST               'pwsync_queue'

 L. 496        24  LOAD_GLOBAL              LOG_LEVEL
               26  STORE_FAST               'log_level'

 L. 497        28  LOAD_CONST               None
               30  STORE_FAST               'console_log_format'

 L. 498        32  LOAD_GLOBAL              os
               34  LOAD_ATTR                environ
               36  LOAD_METHOD              get
               38  LOAD_STR                 'DEBUG'
               40  LOAD_STR                 'no'
               42  CALL_METHOD_2         2  ''
               44  LOAD_STR                 'yes'
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE    60  'to 60'

 L. 499        50  LOAD_GLOBAL              logging
               52  LOAD_ATTR                DEBUG
               54  STORE_FAST               'log_level'

 L. 500        56  LOAD_GLOBAL              CONSOLE_LOG_FORMAT
               58  STORE_FAST               'console_log_format'
             60_0  COME_FROM            48  '48'

 L. 502        60  LOAD_GLOBAL              combined_logger

 L. 503        62  LOAD_GLOBAL              os
               64  LOAD_ATTR                path
               66  LOAD_METHOD              basename
               68  LOAD_FAST                'script_name'
               70  CALL_METHOD_1         1  ''

 L. 504        72  LOAD_FAST                'log_level'

 L. 505        74  LOAD_GLOBAL              SYS_LOG_FORMAT

 L. 506        76  LOAD_FAST                'console_log_format'

 L. 502        78  LOAD_CONST               ('sys_log_format', 'console_log_format')
               80  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               82  STORE_FAST               'my_logger'

 L. 509        84  LOAD_FAST                'my_logger'
               86  LOAD_METHOD              info

 L. 510        88  LOAD_STR                 'Starting %s %s (log level %d)'

 L. 511        90  LOAD_FAST                'script_name'

 L. 512        92  LOAD_GLOBAL              __version__

 L. 513        94  LOAD_FAST                'my_logger'
               96  LOAD_ATTR                level

 L. 509        98  CALL_METHOD_4         4  ''
              100  POP_TOP          

 L. 517       102  LOAD_FAST                'my_logger'
              104  LOAD_METHOD              error

 L. 518       106  LOAD_STR                 "!!! Running in debug mode (log level %d)! Secret data will be logged! Don't do that!!!"

 L. 520       108  LOAD_FAST                'my_logger'
              110  LOAD_ATTR                level

 L. 517       112  CALL_METHOD_2         2  ''
              114  POP_TOP          

 L. 523       116  SETUP_FINALLY       162  'to 162'

 L. 524       118  LOAD_GLOBAL              sys
              120  LOAD_ATTR                argv
              122  LOAD_CONST               1
              124  BINARY_SUBSCR    
              126  STORE_FAST               'socket_path'

 L. 525       128  LOAD_GLOBAL              sys
              130  LOAD_ATTR                argv
              132  LOAD_CONST               2
              134  BINARY_SUBSCR    
              136  STORE_FAST               'local_ldap_uri'

 L. 526       138  LOAD_GLOBAL              sys
              140  LOAD_ATTR                argv
              142  LOAD_CONST               3
              144  BINARY_SUBSCR    
              146  STORE_FAST               'target_ldap_url'

 L. 527       148  LOAD_GLOBAL              sys
              150  LOAD_ATTR                argv
              152  LOAD_CONST               4
              154  BINARY_SUBSCR    
              156  STORE_FAST               'target_password_filename'
              158  POP_BLOCK        
              160  JUMP_FORWARD        202  'to 202'
            162_0  COME_FROM_FINALLY   116  '116'

 L. 528       162  DUP_TOP          
              164  LOAD_GLOBAL              IndexError
              166  COMPARE_OP               exception-match
              168  POP_JUMP_IF_FALSE   200  'to 200'
              170  POP_TOP          
              172  POP_TOP          
              174  POP_TOP          

 L. 529       176  LOAD_FAST                'my_logger'
              178  LOAD_METHOD              error
              180  LOAD_STR                 'Not enough arguments => abort'
              182  CALL_METHOD_1         1  ''
              184  POP_TOP          

 L. 530       186  LOAD_GLOBAL              sys
              188  LOAD_METHOD              exit
              190  LOAD_CONST               1
              192  CALL_METHOD_1         1  ''
              194  POP_TOP          
              196  POP_EXCEPT       
              198  JUMP_FORWARD        202  'to 202'
            200_0  COME_FROM           168  '168'
              200  END_FINALLY      
            202_0  COME_FROM           198  '198'
            202_1  COME_FROM           160  '160'

 L. 532       202  SETUP_FINALLY       224  'to 224'

 L. 533       204  LOAD_GLOBAL              LDAPUrl
              206  LOAD_FAST                'local_ldap_uri'
              208  CALL_FUNCTION_1       1  ''
              210  STORE_FAST               'local_ldap_uri_obj'

 L. 534       212  LOAD_GLOBAL              LDAPUrl
              214  LOAD_FAST                'target_ldap_url'
              216  CALL_FUNCTION_1       1  ''
              218  STORE_FAST               'target_ldap_url_obj'
              220  POP_BLOCK        
              222  JUMP_FORWARD        282  'to 282'
            224_0  COME_FROM_FINALLY   202  '202'

 L. 535       224  DUP_TOP          
              226  LOAD_GLOBAL              ValueError
              228  COMPARE_OP               exception-match
          230_232  POP_JUMP_IF_FALSE   280  'to 280'
              234  POP_TOP          
              236  STORE_FAST               'err'
              238  POP_TOP          
              240  SETUP_FINALLY       268  'to 268'

 L. 536       242  LOAD_FAST                'my_logger'
              244  LOAD_METHOD              error
              246  LOAD_STR                 '%s  => abort'
              248  LOAD_FAST                'err'
              250  CALL_METHOD_2         2  ''
              252  POP_TOP          

 L. 537       254  LOAD_GLOBAL              sys
              256  LOAD_METHOD              exit
              258  LOAD_CONST               1
              260  CALL_METHOD_1         1  ''
              262  POP_TOP          
              264  POP_BLOCK        
              266  BEGIN_FINALLY    
            268_0  COME_FROM_FINALLY   240  '240'
              268  LOAD_CONST               None
              270  STORE_FAST               'err'
              272  DELETE_FAST              'err'
              274  END_FINALLY      
              276  POP_EXCEPT       
              278  JUMP_FORWARD        282  'to 282'
            280_0  COME_FROM           230  '230'
              280  END_FINALLY      
            282_0  COME_FROM           278  '278'
            282_1  COME_FROM           222  '222'

 L. 539       282  LOAD_GLOBAL              ldap0
              284  LOAD_METHOD              get_option
              286  LOAD_GLOBAL              ldap0
              288  LOAD_ATTR                OPT_X_TLS_CACERTFILE
              290  CALL_METHOD_1         1  ''
              292  STORE_FAST               'cacert_filename'

 L. 540       294  LOAD_FAST                'cacert_filename'
          296_298  POP_JUMP_IF_TRUE    320  'to 320'

 L. 541       300  LOAD_FAST                'my_logger'
              302  LOAD_METHOD              error
              304  LOAD_STR                 'No CA certificate file defined => abort'
              306  CALL_METHOD_1         1  ''
              308  POP_TOP          

 L. 542       310  LOAD_GLOBAL              sys
              312  LOAD_METHOD              exit
              314  LOAD_CONST               1
              316  CALL_METHOD_1         1  ''
              318  POP_TOP          
            320_0  COME_FROM           296  '296'

 L. 544       320  SETUP_FINALLY       356  'to 356'

 L. 545       322  LOAD_GLOBAL              open
              324  LOAD_FAST                'cacert_filename'
              326  LOAD_STR                 'r'
              328  CALL_FUNCTION_2       2  ''
              330  SETUP_WITH          346  'to 346'
              332  STORE_FAST               'cacert_file'

 L. 546       334  LOAD_FAST                'cacert_file'
              336  LOAD_METHOD              read
              338  CALL_METHOD_0         0  ''
              340  STORE_FAST               'cacert'
              342  POP_BLOCK        
              344  BEGIN_FINALLY    
            346_0  COME_FROM_WITH      330  '330'
              346  WITH_CLEANUP_START
              348  WITH_CLEANUP_FINISH
              350  END_FINALLY      
              352  POP_BLOCK        
              354  JUMP_FORWARD        416  'to 416'
            356_0  COME_FROM_FINALLY   320  '320'

 L. 547       356  DUP_TOP          
              358  LOAD_GLOBAL              IOError
              360  COMPARE_OP               exception-match
          362_364  POP_JUMP_IF_FALSE   414  'to 414'
              366  POP_TOP          
              368  STORE_FAST               'err'
              370  POP_TOP          
              372  SETUP_FINALLY       402  'to 402'

 L. 548       374  LOAD_FAST                'my_logger'
              376  LOAD_METHOD              error
              378  LOAD_STR                 'Error reading CA cert file %r: %s => abort'
              380  LOAD_FAST                'cacert_filename'
              382  LOAD_FAST                'err'
              384  CALL_METHOD_3         3  ''
              386  POP_TOP          

 L. 549       388  LOAD_GLOBAL              sys
              390  LOAD_METHOD              exit
              392  LOAD_CONST               1
              394  CALL_METHOD_1         1  ''
              396  POP_TOP          
              398  POP_BLOCK        
              400  BEGIN_FINALLY    
            402_0  COME_FROM_FINALLY   372  '372'
              402  LOAD_CONST               None
              404  STORE_FAST               'err'
              406  DELETE_FAST              'err'
              408  END_FINALLY      
              410  POP_EXCEPT       
              412  JUMP_FORWARD        434  'to 434'
            414_0  COME_FROM           362  '362'
              414  END_FINALLY      
            416_0  COME_FROM           354  '354'

 L. 551       416  LOAD_FAST                'my_logger'
              418  LOAD_METHOD              debug
              420  LOAD_STR                 'Using CA cert file %r (%d bytes)'
              422  LOAD_FAST                'cacert_filename'
              424  LOAD_GLOBAL              len
              426  LOAD_FAST                'cacert'
              428  CALL_FUNCTION_1       1  ''
              430  CALL_METHOD_3         3  ''
              432  POP_TOP          
            434_0  COME_FROM           412  '412'

 L. 554       434  SETUP_FINALLY       476  'to 476'

 L. 555       436  LOAD_GLOBAL              open
              438  LOAD_FAST                'target_password_filename'
              440  LOAD_STR                 'r'
              442  LOAD_STR                 'utf-8'
              444  LOAD_CONST               ('encoding',)
              446  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              448  SETUP_WITH          466  'to 466'
              450  STORE_FAST               'target_password_file'

 L. 556       452  LOAD_FAST                'target_password_file'
              454  LOAD_METHOD              read
              456  CALL_METHOD_0         0  ''
              458  LOAD_FAST                'target_ldap_url_obj'
              460  STORE_ATTR               cred
              462  POP_BLOCK        
              464  BEGIN_FINALLY    
            466_0  COME_FROM_WITH      448  '448'
              466  WITH_CLEANUP_START
              468  WITH_CLEANUP_FINISH
              470  END_FINALLY      
              472  POP_BLOCK        
              474  JUMP_FORWARD        536  'to 536'
            476_0  COME_FROM_FINALLY   434  '434'

 L. 557       476  DUP_TOP          
              478  LOAD_GLOBAL              IOError
              480  COMPARE_OP               exception-match
          482_484  POP_JUMP_IF_FALSE   534  'to 534'
              486  POP_TOP          
              488  STORE_FAST               'err'
              490  POP_TOP          
              492  SETUP_FINALLY       522  'to 522'

 L. 558       494  LOAD_FAST                'my_logger'
              496  LOAD_METHOD              error

 L. 559       498  LOAD_STR                 'Error reading target password file %r: %s => abort'

 L. 560       500  LOAD_FAST                'target_password_filename'

 L. 561       502  LOAD_FAST                'err'

 L. 558       504  CALL_METHOD_3         3  ''
              506  POP_TOP          

 L. 563       508  LOAD_GLOBAL              sys
              510  LOAD_METHOD              exit
              512  LOAD_CONST               1
              514  CALL_METHOD_1         1  ''
              516  POP_TOP          
              518  POP_BLOCK        
              520  BEGIN_FINALLY    
            522_0  COME_FROM_FINALLY   492  '492'
              522  LOAD_CONST               None
              524  STORE_FAST               'err'
              526  DELETE_FAST              'err'
              528  END_FINALLY      
              530  POP_EXCEPT       
              532  JUMP_FORWARD        548  'to 548'
            534_0  COME_FROM           482  '482'
              534  END_FINALLY      
            536_0  COME_FROM           474  '474'

 L. 565       536  LOAD_FAST                'my_logger'
              538  LOAD_METHOD              debug
              540  LOAD_STR                 'Using target password file %r'
              542  LOAD_FAST                'target_password_filename'
              544  CALL_METHOD_2         2  ''
              546  POP_TOP          
            548_0  COME_FROM           532  '532'

 L. 568       548  LOAD_GLOBAL              PWSyncWorker

 L. 569       550  LOAD_FAST                'target_ldap_url_obj'

 L. 570       552  LOAD_FAST                'pwsync_queue'

 L. 568       554  CALL_FUNCTION_2       2  ''
              556  STORE_FAST               'pwsync_worker'

 L. 572       558  LOAD_FAST                'local_ldap_uri_obj'
              560  LOAD_METHOD              connect_uri
              562  CALL_METHOD_0         0  ''
              564  LOAD_FAST                'pwsync_worker'
              566  STORE_ATTR               ldapi_uri

 L. 573       568  LOAD_FAST                'pwsync_worker'
              570  LOAD_METHOD              setDaemon
              572  LOAD_CONST               True
              574  CALL_METHOD_1         1  ''
              576  POP_TOP          

 L. 574       578  LOAD_FAST                'pwsync_worker'
              580  LOAD_METHOD              start
              582  CALL_METHOD_0         0  ''
              584  POP_TOP          

 L. 576       586  SETUP_FINALLY       680  'to 680'

 L. 577       588  LOAD_GLOBAL              PassModServer

 L. 578       590  LOAD_FAST                'socket_path'

 L. 579       592  LOAD_GLOBAL              PassModHandler

 L. 580       594  LOAD_GLOBAL              AVERAGE_COUNT

 L. 581       596  LOAD_GLOBAL              SOCKET_TIMEOUT

 L. 581       598  LOAD_GLOBAL              SOCKET_PERMISSIONS

 L. 582       600  LOAD_GLOBAL              ALLOWED_UIDS

 L. 582       602  LOAD_GLOBAL              ALLOWED_GIDS

 L. 583       604  LOAD_FAST                'pwsync_queue'

 L. 584       606  LOAD_GLOBAL              DEBUG_VARS

 L. 577       608  LOAD_CONST               ('log_vars',)
              610  CALL_FUNCTION_KW_9     9  '9 total positional and keyword args'
              612  STORE_FAST               'slapd_sock_listener'

 L. 586       614  LOAD_FAST                'local_ldap_uri_obj'
              616  LOAD_METHOD              connect_uri
              618  CALL_METHOD_0         0  ''
              620  LOAD_FAST                'slapd_sock_listener'
              622  STORE_ATTR               ldapi_uri

 L. 587       624  LOAD_GLOBAL              LDAP0_TRACE_LEVEL
              626  LOAD_FAST                'slapd_sock_listener'
              628  STORE_ATTR               ldap_trace_level

 L. 588       630  SETUP_FINALLY       644  'to 644'

 L. 589       632  LOAD_FAST                'slapd_sock_listener'
              634  LOAD_METHOD              serve_forever
              636  CALL_METHOD_0         0  ''
              638  POP_TOP          
              640  POP_BLOCK        
              642  JUMP_FORWARD        676  'to 676'
            644_0  COME_FROM_FINALLY   630  '630'

 L. 590       644  DUP_TOP          
              646  LOAD_GLOBAL              KeyboardInterrupt
              648  COMPARE_OP               exception-match
          650_652  POP_JUMP_IF_FALSE   674  'to 674'
              654  POP_TOP          
              656  POP_TOP          
              658  POP_TOP          

 L. 591       660  LOAD_FAST                'my_logger'
              662  LOAD_METHOD              warning
              664  LOAD_STR                 'Received interrupt signal => shutdown'
              666  CALL_METHOD_1         1  ''
              668  POP_TOP          
              670  POP_EXCEPT       
              672  JUMP_FORWARD        676  'to 676'
            674_0  COME_FROM           650  '650'
              674  END_FINALLY      
            676_0  COME_FROM           672  '672'
            676_1  COME_FROM           642  '642'
              676  POP_BLOCK        
              678  BEGIN_FINALLY    
            680_0  COME_FROM_FINALLY   586  '586'

 L. 593       680  LOAD_FAST                'my_logger'
              682  LOAD_METHOD              debug
              684  LOAD_STR                 'Remove socket path %s'
              686  LOAD_GLOBAL              repr
              688  LOAD_FAST                'socket_path'
              690  CALL_FUNCTION_1       1  ''
              692  CALL_METHOD_2         2  ''
              694  POP_TOP          

 L. 594       696  SETUP_FINALLY       712  'to 712'

 L. 595       698  LOAD_GLOBAL              os
              700  LOAD_METHOD              remove
              702  LOAD_FAST                'socket_path'
              704  CALL_METHOD_1         1  ''
              706  POP_TOP          
              708  POP_BLOCK        
              710  JUMP_FORWARD        734  'to 734'
            712_0  COME_FROM_FINALLY   696  '696'

 L. 596       712  DUP_TOP          
              714  LOAD_GLOBAL              OSError
              716  COMPARE_OP               exception-match
          718_720  POP_JUMP_IF_FALSE   732  'to 732'
              722  POP_TOP          
              724  POP_TOP          
              726  POP_TOP          

 L. 597       728  POP_EXCEPT       
              730  JUMP_FORWARD        734  'to 734'
            732_0  COME_FROM           718  '718'
              732  END_FINALLY      
            734_0  COME_FROM           730  '730'
            734_1  COME_FROM           710  '710'
              734  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 344


if __name__ == '__main__':
    run()