# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /oathldap_srv/hotp_validator.py
# Compiled at: 2020-04-13 17:14:45
# Size of source mod 2**32: 40138 bytes
"""
oathldap_srv.hotp_validator:
slapd-sock listener demon which performs
- password checking and HOTP validation on intercepted BIND requests
- or only HOTP validation on COMPARE requests
"""
import os, logging, sys, json, glob, cryptography.hazmat.backends, cryptography.hazmat.primitives.twofactor.hotp, cryptography.hazmat.primitives.hashes, passlib.context
try:
    from jwcrypto.jwk import JWK
    from jwcrypto.jwe import JWE
except ImportError:
    JWE = JWK = None
else:
    import ldap0, ldap0.functions
    from ldap0 import LDAPError
    from ldap0.ldapurl import LDAPUrl
    from ldap0.controls.simple import RelaxRulesControl
    from ldap0.controls.libldap import AssertionControl
    from ldap0.functions import is_expired
    from slapdsock.handler import SlapdSockHandler, SlapdSockHandlerError
    from slapdsock.message import CONTINUE_RESPONSE, InternalErrorResponse, SuccessResponse, InvalidCredentialsResponse, CompareFalseResponse, CompareTrueResponse
    from slapdsock.service import SlapdSockServer
    from .__about__ import __version__
    from . import cfg
    from .logger import init_logger
    DEBUG_VARS = [
     'oath_hotp_current_counter',
     'oath_hotp_lookahead',
     'oath_hotp_next_counter',
     'oath_max_usage_count',
     'oath_otp_length',
     'oath_params_dn',
     'oath_params_entry',
     'oath_secret_max_age',
     'oath_token_dn',
     'oath_token_identifier',
     'oath_token_identifier_length',
     'oath_token_identifier_req',
     'oath_token_secret_time',
     'otp_compare',
     'otp_value',
     'user_password_compare',
     'user_password_length']
    DEBUG_VARS.extend([
     'otp_token_entry',
     'user_entry',
     'user_password_hash'])

    class HOTPValidatorConfig(cfg.Config):
        __doc__ = '\n    Configuration parameters\n    '
        default_section = 'hotp_validator'
        type_map = {'allowed_gids':cfg.val_list, 
         'allowed_uids':cfg.val_list, 
         'avg_count':int, 
         'cache_ttl':float, 
         'ldap0_trace_level':int, 
         'ldap_cache_ttl':float, 
         'ldapi_uri':LDAPUrl, 
         'ldap_max_retries':int, 
         'ldap_retry_delay':float, 
         'ldap_timeout':float, 
         'log_level':str.upper, 
         'noproxy_peer_addrs':cfg.val_list, 
         'providers':cfg.ldap_url_list, 
         'proxy_peer_addrs':cfg.val_list, 
         'proxy_peer_nets':cfg.ip_network_list, 
         'socket_timeout':float}
        required_params = ('ldapi_uri', 'socket_path')
        cache_ttl = -1.0
        ldapi_uri = 'ldapi://'
        cacert_file = '/etc/ssl/ca-bundle.pem'
        allowed_uids = [
         0, 'ldap']
        allowed_gids = [0]
        socket_perms = '0666'
        ldap0_trace_level = 0
        ldap_max_retries = 10
        ldap_retry_delay = 0.1
        ldapi_sasl_authzid = None
        ldap_cache_ttl = 180.0
        ldap_timeout = 3.0
        socket_timeout = 2 * ldap_timeout
        avg_count = 100
        log_vars = DEBUG_VARS
        user_filter = '(&(objectClass=oathHOTPUser)(oathHOTPToken=*))'
        oath_token_filter = '(&(objectClass=oathHOTPToken)(oathHOTPCounter>=0)(oathSecret=*))'
        user_notbefore_attr = 'aeNotBefore'
        user_notafter_attr = 'aeNotAfter'
        oath_params_cache_ttl = 600
        master_key_files = None
        response_info = True

        def __init__(self, cfg_filename):
            cfg.Config.__init__(self, cfg_filename)
            self.cache_ttl = {'BIND': self.cache_ttl}


    class DetailedResponseInfo:
        __doc__ = '\n    message catalog with informative messages\n    '
        HOTP_COUNTER_EXCEEDED = 'HOTP counter limit exceeded'
        OTP_TOKEN_EXPIRED = 'HOTP token expired'
        VERIFICATION_FAILED = 'user_password_compare={user_password_compare}/otp_compare={otp_compare}'
        HOTP_WRONG_TOKEN_ID = 'wrong token identifier'
        ENTRY_NOT_VALID = 'not within validity period'
        OTP_TOKEN_ERROR = 'Error reading OTP token'


    class SparseResponseInfo:
        __doc__ = '\n    message catalog with no messages to avoid giving hints to attackers\n    '
        HOTP_COUNTER_EXCEEDED = ''
        OTP_TOKEN_EXPIRED = ''
        VERIFICATION_FAILED = ''
        HOTP_WRONG_TOKEN_ID = ''
        ENTRY_NOT_VALID = ''
        OTP_TOKEN_ERROR = ''


    class HOTPValidationServer(SlapdSockServer):
        __doc__ = '\n    This is used to pass in more parameters to the server instance.\n\n    By purpose this is a single-threaded listener serializing all requests!\n    '

        def __init__(self, cfg, logger):
            self.cfg = cfg
            SlapdSockServer.__init__(self,
              (self.cfg.socket_path),
              HOTPValidationHandler,
              logger,
              (self.cfg.avg_count),
              (self.cfg.socket_timeout),
              (self.cfg.socket_perms),
              (self.cfg.allowed_uids),
              (self.cfg.allowed_gids),
              bind_and_activate=True,
              monitor_dn=None,
              log_vars=(cfg.log_vars))
            self.ldap_timeout = self.cfg.ldap_timeout
            self.ldapi_uri = self.cfg.ldapi_uri.connect_uri()
            self.ldap_trace_level = self.cfg.ldap0_trace_level
            self.ldap_authz_id = self.cfg.ldapi_sasl_authzid
            self.ldap_retry_max = self.cfg.ldap_max_retries
            self.ldap_retry_delay = self.cfg.ldap_retry_delay
            self.ldap_cache_ttl = self.cfg.ldap_cache_ttl
            self.max_lookahead_seen = 0
            if JWK:
                self._load_keys((self.cfg.master_key_files), reset=True)

        def _load_keys(self, key_files, reset=False):
            """
        Load JWE keys defined by globbing pattern in :key_files:
        """
            if reset:
                self.master_keys = {}
            else:
                return key_files or None
            self.logger.debug('Read JWK files with glob pattern %r', key_files)
            for private_key_filename in glob.glob(key_files):
                try:
                    with open(private_key_filename, 'rb') as (privkey_file):
                        privkey_json = privkey_file.read()
                    private_key = JWK(**json.loads(privkey_json))
                except (IOError, ValueError) as err:
                    try:
                        self.logger.error('Error reading/decoding JWK file %r: %s', private_key_filename, err)
                    finally:
                        err = None
                        del err

                else:
                    self.master_keys[private_key.key_id] = private_key
            else:
                self.logger.info('Read %d JWK files, key IDs: %s', len(self.master_keys), ' '.join(self.master_keys.keys()))

        def monitor_entry(self):
            """
        Returns entry dictionary with monitoring data.
        """
            monitor_entry = SlapdSockServer.monitor_entry(self)
            monitor_entry.update({'sockHOTPMaxLookAheadSeen':[
              str(self.max_lookahead_seen)], 
             'sockHOTPKeyCount':[
              str(len(self.master_keys))], 
             'sockHOTPKeyIDs':self.master_keys.keys()})
            return monitor_entry


    class HOTPValidationHandler(SlapdSockHandler):
        __doc__ = "\n    Handler class which validates user's password and HOTP value\n    "
        infomsg = {False:SparseResponseInfo, 
         True:DetailedResponseInfo}
        token_attr_list = [
         'createTimestamp',
         'oathHOTPCounter',
         'oathHOTPParams',
         'oathSecret',
         'oathSecretTime',
         'oathTokenIdentifier',
         'oathTokenSerialNumber',
         'oathFailureCount']
        compare_assertion_type = 'oathHOTPValue'

        def __init__(self, *args, **kwargs):
            (SlapdSockHandler.__init__)(self, *args, **kwargs)
            self._ldapi_conn = None

        def _check_validity_period--- This code section failed: ---

 L. 351         0  LOAD_FAST                'entry'
                2  LOAD_METHOD              get
                4  LOAD_FAST                'not_before_attr'
                6  LOAD_CONST               None
                8  BUILD_LIST_1          1 
               10  CALL_METHOD_2         2  ''
               12  LOAD_CONST               0
               14  BINARY_SUBSCR    
               16  STORE_FAST               'not_before'

 L. 352        18  LOAD_FAST                'entry'
               20  LOAD_METHOD              get
               22  LOAD_FAST                'not_after_attr'
               24  LOAD_CONST               None
               26  BUILD_LIST_1          1 
               28  CALL_METHOD_2         2  ''
               30  LOAD_CONST               0
               32  BINARY_SUBSCR    
               34  STORE_FAST               'not_after'

 L. 354        36  LOAD_FAST                'not_before'
               38  LOAD_CONST               None
               40  COMPARE_OP               is
               42  POP_JUMP_IF_TRUE     62  'to 62'
               44  LOAD_GLOBAL              ldap0
               46  LOAD_ATTR                functions
               48  LOAD_METHOD              str2datetime
               50  LOAD_FAST                'not_before'
               52  CALL_METHOD_1         1  ''
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                now_dt
               58  COMPARE_OP               <=
               60  JUMP_IF_FALSE_OR_POP    86  'to 86'
             62_0  COME_FROM            42  '42'

 L. 355        62  LOAD_FAST                'not_after'
               64  LOAD_CONST               None
               66  COMPARE_OP               is
               68  JUMP_IF_TRUE_OR_POP    86  'to 86'
               70  LOAD_GLOBAL              ldap0
               72  LOAD_ATTR                functions
               74  LOAD_METHOD              str2datetime
               76  LOAD_FAST                'not_after'
               78  CALL_METHOD_1         1  ''
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                now_dt
               84  COMPARE_OP               >=
             86_0  COME_FROM            68  '68'
             86_1  COME_FROM            60  '60'

 L. 353        86  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 86

        def _update_token_entry(self, request, token_dn, success, oath_hotp_next_counter, otp_token_entry):
            """
        update OATH token entry
        """
            mod_ctrls = None
            if success:
                mods = [
                 (
                  ldap0.MOD_REPLACE, b'oathFailureCount', [b'0']),
                 (
                  ldap0.MOD_REPLACE, b'oathLastLogin', [self.now_str.encode('ascii')])]
            else:
                mods = [
                 (
                  {False:ldap0.MOD_ADD, 
                   True:ldap0.MOD_INCREMENT}[('oathFailureCount' in otp_token_entry)],
                  b'oathFailureCount',
                  [
                   b'1']),
                 (
                  ldap0.MOD_REPLACE, b'oathLastFailure', [self.now_str.encode('ascii')])]
            if oath_hotp_next_counter is not None:
                mods.append((
                 ldap0.MOD_REPLACE,
                 b'oathHOTPCounter',
                 [
                  str(oath_hotp_next_counter).encode('ascii')]))
                mod_ctrls = [
                 AssertionControl(True, '(oathHOTPCounter<=%d)' % (oath_hotp_next_counter,))]
            try:
                self._ldapi_conn.modify_s(token_dn,
                  mods,
                  req_ctrls=mod_ctrls)
            except LDAPError as err:
                try:
                    self._log(logging.ERROR, 'LDAPError updating token entry %r with %r: %s => unwillingToPerform', token_dn, mods, err)
                    raise SlapdSockHandlerError(err,
                      log_level=(logging.ERROR),
                      response=(InternalErrorResponse(request.msgid)),
                      log_vars=(self.server._log_vars))
                finally:
                    err = None
                    del err

            else:
                self._log(logging.DEBUG, 'Updated token entry %r with %r', token_dn, mods)

        def _update_pwdfailuretime(self, user_dn, user_entry, success):
            """
        update user's entry after successful login
        """
            if not success:
                mods = [(ldap0.MOD_ADD, b'pwdFailureTime', [self.now_str.encode('ascii')])]
            else:
                if 'pwdFailureTime' in user_entry:
                    mods = [
                     (
                      ldap0.MOD_DELETE, b'pwdFailureTime', None)]
                else:
                    self._log(logging.DEBUG, 'No update of user entry %r', user_dn)
                    return
            try:
                self._ldapi_conn.modify_s(user_dn,
                  mods,
                  req_ctrls=[
                 RelaxRulesControl(True)])
            except LDAPError as err:
                try:
                    self._log(logging.ERROR, 'Error updating user entry %r with %r: %s', user_dn, mods, err)
                finally:
                    err = None
                    del err

            else:
                self._log(logging.DEBUG, 'Updated user entry %r with %r', user_dn, mods)

        def _check_userpassword(self, user_dn, user_entry, user_password_clear):
            """
        validate user's clear-text password against {CRYPT} password hash
        in attribute 'userPassword' of user's entry
        """
            try:
                user_password_hash = user_entry['userPassword'][0][7:]
            except KeyError:
                self._log(logging.WARN, 'No userPassword attribute found %r', user_dn)
                result = False
            else:
                pw_context = passlib.context.CryptContext(schemes=['sha512_crypt'])
                result = pw_context.verify(user_password_clear, user_password_hash)
            return result

        def _get_user_entry(self, request, failure_response_class):
            """
        Read user entry
        """
            user_entry = response = None
            try:
                user = self._ldapi_conn.read_s((request.dn),
                  (self.server.cfg.user_filter),
                  attrlist=(filter(None, [
                 'oathHOTPToken',
                 'pwdFailureTime',
                 'userPassword',
                 self.server.cfg.user_notbefore_attr,
                 self.server.cfg.user_notafter_attr])))
            except ldap0.NO_SUCH_OBJECT as err:
                try:
                    self._log(logging.INFO, 'User entry %r not found: %s => CONTINUE', request.dn, err)
                    response = CONTINUE_RESPONSE
                finally:
                    err = None
                    del err

            except LDAPError as err:
                try:
                    self._log(logging.WARN, 'Reading user entry %r failed: %s => %s', request.dn, err, failure_response_class.__name__)
                    response = failure_response_class(request.msgid)
                finally:
                    err = None
                    del err

            else:
                if user is None:
                    self._log(logging.INFO, 'No result reading user entry %r with filter %r => CONTINUE', request.dn, self.server.cfg.user_filter)
                    response = CONTINUE_RESPONSE
                else:
                    response = None
                    user_entry = user.entry_s
                return (
                 user_entry, response)

        def _get_oath_token_entry(self, user_dn, user_entry):
            """
        Read the OATH token entry
        """
            try:
                oath_token_dn = user_entry['oathHOTPToken'][0]
            except KeyError:
                oath_token_dn = user_dn
            else:
                try:
                    otp_token = self._ldapi_conn.read_s(oath_token_dn,
                      (self.server.cfg.oath_token_filter),
                      attrlist=(self.token_attr_list),
                      cache_ttl=0)
                except LDAPError as err:
                    try:
                        self._log(logging.ERROR, 'Error reading token %r: %s', oath_token_dn, err)
                        otp_token_entry = None
                    finally:
                        err = None
                        del err

                else:
                    if otp_token is None:
                        otp_token_entry = None
                        self._log(logging.ERROR, 'Empty result reading token %r', oath_token_dn)
                    else:
                        otp_token_entry = otp_token.entry_s

        def _get_oath_token_params(self, otp_token_entry):
            """
        Read OATH token parameters from referenced oathHOTPParams entry
        """
            oath_params_entry = {}
            if 'oathHOTPParams' in otp_token_entry:
                oath_params_dn = otp_token_entry['oathHOTPParams'][0]
                try:
                    oath_params = self._ldapi_conn.read_s(oath_params_dn,
                      '(objectClass=oathHOTPParams)',
                      attrlist=[
                     'oathMaxUsageCount',
                     'oathHOTPLookAhead',
                     'oathOTPLength',
                     'oathSecretMaxAge'],
                      cache_ttl=(self.server.cfg.oath_params_cache_ttl))
                except LDAPError as err:
                    try:
                        self._log(logging.ERROR, 'Error reading OATH params from %r: %s => use defaults', oath_params_dn, err)
                    finally:
                        err = None
                        del err

                else:
                    if oath_params is not None:
                        oath_params_entry = oath_params.entry_s
            if not oath_params_entry:
                self._log(logging.WARN, 'No OATH params! Using defaults.')
            oath_otp_length = int(oath_params_entry.get('oathOTPLength', ['6'])[0])
            oath_hotp_lookahead = int(oath_params_entry.get('oathHOTPLookAhead', ['5'])[0])
            oath_max_usage_count = int(oath_params_entry.get('oathMaxUsageCount', ['-1'])[0])
            oath_secret_max_age = int(oath_params_entry.get('oathSecretMaxAge', ['0'])[0])
            return (oath_otp_length, oath_hotp_lookahead, oath_max_usage_count, oath_secret_max_age)

        def _decrypt_oath_secret--- This code section failed: ---

 L. 630         0  LOAD_GLOBAL              JWE
                2  POP_JUMP_IF_FALSE    12  'to 12'
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                server
                8  LOAD_ATTR                master_keys
               10  POP_JUMP_IF_TRUE     30  'to 30'
             12_0  COME_FROM             2  '2'

 L. 631        12  LOAD_FAST                'self'
               14  LOAD_METHOD              _log

 L. 632        16  LOAD_GLOBAL              logging
               18  LOAD_ATTR                DEBUG

 L. 633        20  LOAD_STR                 'no JWK keys configured => return raw oathSecret value'

 L. 631        22  CALL_METHOD_2         2  ''
               24  POP_TOP          

 L. 635        26  LOAD_FAST                'oath_secret'
               28  RETURN_VALUE     
             30_0  COME_FROM            10  '10'

 L. 636        30  SETUP_FINALLY        46  'to 46'

 L. 637        32  LOAD_GLOBAL              json
               34  LOAD_METHOD              loads
               36  LOAD_FAST                'oath_secret'
               38  CALL_METHOD_1         1  ''
               40  STORE_FAST               'json_s'
               42  POP_BLOCK        
               44  JUMP_FORWARD        104  'to 104'
             46_0  COME_FROM_FINALLY    30  '30'

 L. 638        46  DUP_TOP          
               48  LOAD_GLOBAL              ValueError
               50  COMPARE_OP               exception-match
               52  POP_JUMP_IF_FALSE   102  'to 102'
               54  POP_TOP          
               56  STORE_FAST               'err'
               58  POP_TOP          
               60  SETUP_FINALLY        90  'to 90'

 L. 639        62  LOAD_FAST                'self'
               64  LOAD_METHOD              _log

 L. 640        66  LOAD_GLOBAL              logging
               68  LOAD_ATTR                DEBUG

 L. 641        70  LOAD_STR                 'error decoding JWE data: %s => return raw oathSecret value'

 L. 642        72  LOAD_FAST                'err'

 L. 639        74  CALL_METHOD_3         3  ''
               76  POP_TOP          

 L. 644        78  LOAD_FAST                'oath_secret'
               80  ROT_FOUR         
               82  POP_BLOCK        
               84  POP_EXCEPT       
               86  CALL_FINALLY         90  'to 90'
               88  RETURN_VALUE     
             90_0  COME_FROM            86  '86'
             90_1  COME_FROM_FINALLY    60  '60'
               90  LOAD_CONST               None
               92  STORE_FAST               'err'
               94  DELETE_FAST              'err'
               96  END_FINALLY      
               98  POP_EXCEPT       
              100  JUMP_FORWARD        104  'to 104'
            102_0  COME_FROM            52  '52'
              102  END_FINALLY      
            104_0  COME_FROM           100  '100'
            104_1  COME_FROM            44  '44'

 L. 645       104  LOAD_FAST                'json_s'
              106  LOAD_STR                 'header'
              108  BINARY_SUBSCR    
              110  LOAD_STR                 'kid'
              112  BINARY_SUBSCR    
              114  STORE_FAST               'key_id'

 L. 646       116  LOAD_FAST                'self'
              118  LOAD_METHOD              _log
              120  LOAD_GLOBAL              logging
              122  LOAD_ATTR                DEBUG
              124  LOAD_STR                 'JWE references key ID: %r'
              126  LOAD_FAST                'key_id'
              128  CALL_METHOD_3         3  ''
              130  POP_TOP          

 L. 647       132  LOAD_GLOBAL              JWE
              134  CALL_FUNCTION_0       0  ''
              136  STORE_FAST               'jwe_decrypter'

 L. 648       138  SETUP_FINALLY       156  'to 156'

 L. 649       140  LOAD_FAST                'self'
              142  LOAD_ATTR                server
              144  LOAD_ATTR                master_keys
              146  LOAD_FAST                'key_id'
              148  BINARY_SUBSCR    
              150  STORE_FAST               'oath_master_secret'
              152  POP_BLOCK        
              154  JUMP_FORWARD        190  'to 190'
            156_0  COME_FROM_FINALLY   138  '138'

 L. 650       156  DUP_TOP          
              158  LOAD_GLOBAL              KeyError
              160  COMPARE_OP               exception-match
              162  POP_JUMP_IF_FALSE   188  'to 188'
              164  POP_TOP          
              166  POP_TOP          
              168  POP_TOP          

 L. 651       170  LOAD_GLOBAL              KeyError
              172  LOAD_STR                 'OATH master key with key-id %r not found'
              174  LOAD_FAST                'key_id'
              176  BUILD_TUPLE_1         1 
              178  BINARY_MODULO    
              180  CALL_FUNCTION_1       1  ''
              182  RAISE_VARARGS_1       1  'exception instance'
              184  POP_EXCEPT       
              186  JUMP_FORWARD        190  'to 190'
            188_0  COME_FROM           162  '162'
              188  END_FINALLY      
            190_0  COME_FROM           186  '186'
            190_1  COME_FROM           154  '154'

 L. 652       190  LOAD_FAST                'jwe_decrypter'
              192  LOAD_METHOD              deserialize
              194  LOAD_FAST                'oath_secret'
              196  LOAD_FAST                'oath_master_secret'
              198  CALL_METHOD_2         2  ''
              200  POP_TOP          

 L. 653       202  LOAD_FAST                'jwe_decrypter'
              204  LOAD_ATTR                plaintext
              206  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 82

        def _check_hotp(self, oath_secret, otp_value, counter, length=6, drift=0):
            """
        this function validates HOTP value
        """
            if drift < 0:
                raise ValueError('OATH counter drift must be >= 0, but was %d' % (drift,))
            else:
                otp_instance = cryptography.hazmat.primitives.twofactor.hotp.HOTP((self._decrypt_oath_secret(oath_secret)),
                  length,
                  (cryptography.hazmat.primitives.hashes.SHA1()),
                  backend=(cryptography.hazmat.backends.default_backend()))
                result = None
                max_counter = counter + drift
                while True:
                    if counter <= max_counter:
                        try:
                            otp_instance.verify(otp_value, counter)
                        except cryptography.hazmat.primitives.twofactor.hotp.InvalidToken:
                            counter += 1
                        else:
                            result = counter + 1
                            break

            return result

        def do_bind--- This code section failed: ---

 L. 695         0  LOAD_FAST                'self'
                2  LOAD_ATTR                server
                4  LOAD_METHOD              get_ldapi_conn
                6  CALL_METHOD_0         0  ''
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _ldapi_conn

 L. 698        12  LOAD_FAST                'self'
               14  LOAD_METHOD              _get_user_entry
               16  LOAD_FAST                'request'
               18  LOAD_GLOBAL              InvalidCredentialsResponse
               20  CALL_METHOD_2         2  ''
               22  UNPACK_SEQUENCE_2     2 
               24  STORE_FAST               'user_entry'
               26  STORE_FAST               'response'

 L. 699        28  LOAD_FAST                'user_entry'
               30  LOAD_CONST               None
               32  COMPARE_OP               is
               34  POP_JUMP_IF_FALSE    40  'to 40'

 L. 700        36  LOAD_FAST                'response'
               38  RETURN_VALUE     
             40_0  COME_FROM            34  '34'

 L. 703        40  LOAD_FAST                'self'
               42  LOAD_METHOD              _get_oath_token_entry
               44  LOAD_FAST                'request'
               46  LOAD_ATTR                dn
               48  LOAD_FAST                'user_entry'
               50  CALL_METHOD_2         2  ''
               52  UNPACK_SEQUENCE_2     2 
               54  STORE_FAST               'oath_token_dn'
               56  STORE_FAST               'otp_token_entry'

 L. 704        58  LOAD_FAST                'otp_token_entry'
               60  POP_JUMP_IF_TRUE     88  'to 88'

 L. 706        62  LOAD_GLOBAL              InvalidCredentialsResponse
               64  LOAD_FAST                'request'
               66  LOAD_ATTR                msgid
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                infomsg
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                server
               76  LOAD_ATTR                cfg
               78  LOAD_ATTR                response_info
               80  BINARY_SUBSCR    
               82  LOAD_ATTR                OTP_TOKEN_ERROR
               84  CALL_FUNCTION_2       2  ''
               86  RETURN_VALUE     
             88_0  COME_FROM            60  '60'

 L. 709        88  LOAD_FAST                'otp_token_entry'
               90  LOAD_METHOD              get
               92  LOAD_STR                 'oathTokenIdentifier'
               94  LOAD_STR                 ''
               96  BUILD_LIST_1          1 
               98  CALL_METHOD_2         2  ''
              100  LOAD_CONST               0
              102  BINARY_SUBSCR    
              104  STORE_FAST               'oath_token_identifier'

 L. 710       106  LOAD_GLOBAL              len
              108  LOAD_FAST                'oath_token_identifier'
              110  CALL_FUNCTION_1       1  ''
              112  STORE_FAST               'oath_token_identifier_length'

 L. 711       114  LOAD_FAST                'otp_token_entry'
              116  LOAD_METHOD              get

 L. 712       118  LOAD_STR                 'oathSecretTime'

 L. 713       120  LOAD_FAST                'otp_token_entry'
              122  LOAD_METHOD              get

 L. 714       124  LOAD_STR                 'createTimestamp'

 L. 715       126  LOAD_CONST               None
              128  BUILD_LIST_1          1 

 L. 713       130  CALL_METHOD_2         2  ''

 L. 711       132  CALL_METHOD_2         2  ''

 L. 717       134  LOAD_CONST               0

 L. 711       136  BINARY_SUBSCR    
              138  STORE_FAST               'oath_token_secret_time'

 L. 720       140  SETUP_FINALLY       174  'to 174'

 L. 721       142  LOAD_GLOBAL              int
              144  LOAD_FAST                'otp_token_entry'
              146  LOAD_STR                 'oathHOTPCounter'
              148  BINARY_SUBSCR    
              150  LOAD_CONST               0
              152  BINARY_SUBSCR    
              154  CALL_FUNCTION_1       1  ''
              156  STORE_FAST               'oath_hotp_current_counter'

 L. 722       158  LOAD_FAST                'otp_token_entry'
              160  LOAD_STR                 'oathSecret'
              162  BINARY_SUBSCR    
              164  LOAD_CONST               0
              166  BINARY_SUBSCR    
              168  STORE_FAST               'oath_secret'
              170  POP_BLOCK        
              172  JUMP_FORWARD        244  'to 244'
            174_0  COME_FROM_FINALLY   140  '140'

 L. 723       174  DUP_TOP          
              176  LOAD_GLOBAL              KeyError
              178  COMPARE_OP               exception-match
              180  POP_JUMP_IF_FALSE   242  'to 242'
              182  POP_TOP          
              184  STORE_FAST               'err'
              186  POP_TOP          
              188  SETUP_FINALLY       230  'to 230'

 L. 724       190  LOAD_FAST                'self'
              192  LOAD_METHOD              _log

 L. 725       194  LOAD_GLOBAL              logging
              196  LOAD_ATTR                ERROR

 L. 726       198  LOAD_STR                 'Missing OATH attributes in %r: %s => %s'

 L. 727       200  LOAD_FAST                'oath_token_dn'

 L. 728       202  LOAD_FAST                'err'

 L. 729       204  LOAD_GLOBAL              InvalidCredentialsResponse
              206  LOAD_ATTR                __name__

 L. 724       208  CALL_METHOD_5         5  ''
              210  POP_TOP          

 L. 731       212  LOAD_GLOBAL              InvalidCredentialsResponse
              214  LOAD_FAST                'request'
              216  LOAD_ATTR                msgid
              218  CALL_FUNCTION_1       1  ''
              220  ROT_FOUR         
              222  POP_BLOCK        
              224  POP_EXCEPT       
              226  CALL_FINALLY        230  'to 230'
              228  RETURN_VALUE     
            230_0  COME_FROM           226  '226'
            230_1  COME_FROM_FINALLY   188  '188'
              230  LOAD_CONST               None
              232  STORE_FAST               'err'
              234  DELETE_FAST              'err'
              236  END_FINALLY      
              238  POP_EXCEPT       
              240  JUMP_FORWARD        244  'to 244'
            242_0  COME_FROM           180  '180'
              242  END_FINALLY      
            244_0  COME_FROM           240  '240'
            244_1  COME_FROM           172  '172'

 L. 734       244  LOAD_FAST                'self'
              246  LOAD_METHOD              _get_oath_token_params
              248  LOAD_FAST                'otp_token_entry'
              250  CALL_METHOD_1         1  ''

 L. 733       252  UNPACK_SEQUENCE_4     4 
              254  STORE_FAST               'oath_otp_length'
              256  STORE_FAST               'oath_hotp_lookahead'
              258  STORE_FAST               'oath_max_usage_count'
              260  STORE_FAST               'oath_secret_max_age'

 L. 740       262  LOAD_GLOBAL              len
              264  LOAD_FAST                'request'
              266  LOAD_ATTR                cred
              268  CALL_FUNCTION_1       1  ''
              270  LOAD_FAST                'oath_otp_length'
              272  BINARY_SUBTRACT  
              274  LOAD_FAST                'oath_token_identifier_length'
              276  BINARY_SUBTRACT  
              278  STORE_FAST               'user_password_length'

 L. 743       280  LOAD_FAST                'request'
              282  LOAD_ATTR                cred
              284  LOAD_CONST               0
              286  LOAD_FAST                'user_password_length'
              288  BUILD_SLICE_2         2 
              290  BINARY_SUBSCR    

 L. 744       292  LOAD_FAST                'request'
              294  LOAD_ATTR                cred
              296  LOAD_FAST                'user_password_length'
              298  LOAD_FAST                'oath_otp_length'
              300  UNARY_NEGATIVE   
              302  BUILD_SLICE_2         2 
              304  BINARY_SUBSCR    

 L. 745       306  LOAD_FAST                'request'
              308  LOAD_ATTR                cred
              310  LOAD_FAST                'oath_otp_length'
              312  UNARY_NEGATIVE   
              314  LOAD_CONST               None
              316  BUILD_SLICE_2         2 
              318  BINARY_SUBSCR    

 L. 742       320  ROT_THREE        
              322  ROT_TWO          
              324  STORE_FAST               'user_password_clear'
              326  STORE_FAST               'oath_token_identifier_req'
              328  STORE_FAST               'otp_value'

 L. 748       330  LOAD_FAST                'self'
              332  LOAD_METHOD              _check_userpassword

 L. 749       334  LOAD_FAST                'request'
              336  LOAD_ATTR                dn

 L. 750       338  LOAD_FAST                'user_entry'

 L. 751       340  LOAD_FAST                'user_password_clear'

 L. 748       342  CALL_METHOD_3         3  ''
              344  STORE_FAST               'user_password_compare'

 L. 755       346  LOAD_FAST                'otp_value'
          348_350  POP_JUMP_IF_TRUE    376  'to 376'

 L. 756       352  LOAD_CONST               None
              354  STORE_FAST               'oath_hotp_next_counter'

 L. 758       356  LOAD_FAST                'self'
              358  LOAD_METHOD              _log

 L. 759       360  LOAD_GLOBAL              logging
              362  LOAD_ATTR                WARN

 L. 760       364  LOAD_STR                 'Empty OTP value sent for %r'

 L. 761       366  LOAD_FAST                'request'
              368  LOAD_ATTR                dn

 L. 758       370  CALL_METHOD_3         3  ''
              372  POP_TOP          
              374  JUMP_FORWARD        468  'to 468'
            376_0  COME_FROM           348  '348'

 L. 766       376  LOAD_FAST                'self'
              378  LOAD_ATTR                _check_hotp

 L. 767       380  LOAD_FAST                'oath_secret'

 L. 768       382  LOAD_FAST                'otp_value'

 L. 769       384  LOAD_FAST                'oath_hotp_current_counter'

 L. 770       386  LOAD_FAST                'oath_otp_length'

 L. 771       388  LOAD_FAST                'oath_hotp_lookahead'

 L. 766       390  LOAD_CONST               ('length', 'drift')
              392  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              394  STORE_FAST               'oath_hotp_next_counter'

 L. 773       396  LOAD_FAST                'oath_hotp_next_counter'
              398  LOAD_CONST               None
              400  COMPARE_OP               is-not
          402_404  POP_JUMP_IF_FALSE   452  'to 452'

 L. 774       406  LOAD_FAST                'oath_hotp_next_counter'
              408  LOAD_FAST                'oath_hotp_current_counter'
              410  BINARY_SUBTRACT  
              412  STORE_FAST               'oath_hotp_drift'

 L. 775       414  LOAD_FAST                'self'
              416  LOAD_METHOD              _log

 L. 776       418  LOAD_GLOBAL              logging
              420  LOAD_ATTR                DEBUG

 L. 777       422  LOAD_STR                 'OTP value valid (drift %d) for %r'

 L. 778       424  LOAD_FAST                'oath_hotp_drift'

 L. 779       426  LOAD_FAST                'oath_token_dn'

 L. 775       428  CALL_METHOD_4         4  ''
              430  POP_TOP          

 L. 782       432  LOAD_GLOBAL              max

 L. 783       434  LOAD_FAST                'self'
              436  LOAD_ATTR                server
              438  LOAD_ATTR                max_lookahead_seen

 L. 784       440  LOAD_FAST                'oath_hotp_drift'

 L. 782       442  CALL_FUNCTION_2       2  ''
              444  LOAD_FAST                'self'
              446  LOAD_ATTR                server
              448  STORE_ATTR               max_lookahead_seen
              450  JUMP_FORWARD        468  'to 468'
            452_0  COME_FROM           402  '402'

 L. 787       452  LOAD_FAST                'self'
              454  LOAD_METHOD              _log

 L. 788       456  LOAD_GLOBAL              logging
              458  LOAD_ATTR                DEBUG

 L. 789       460  LOAD_STR                 'OTP value invalid for %r'

 L. 790       462  LOAD_FAST                'oath_token_dn'

 L. 787       464  CALL_METHOD_3         3  ''
              466  POP_TOP          
            468_0  COME_FROM           450  '450'
            468_1  COME_FROM           374  '374'

 L. 793       468  LOAD_FAST                'oath_hotp_next_counter'
              470  LOAD_CONST               None
              472  COMPARE_OP               is-not
              474  STORE_FAST               'otp_compare'

 L. 797       476  LOAD_FAST                'self'
              478  LOAD_METHOD              _update_token_entry

 L. 798       480  LOAD_FAST                'request'

 L. 799       482  LOAD_FAST                'oath_token_dn'

 L. 800       484  LOAD_FAST                'otp_compare'
          486_488  JUMP_IF_FALSE_OR_POP   496  'to 496'
              490  LOAD_FAST                'oath_token_identifier'
              492  LOAD_FAST                'oath_token_identifier_req'
              494  COMPARE_OP               ==
            496_0  COME_FROM           486  '486'

 L. 801       496  LOAD_FAST                'oath_hotp_next_counter'

 L. 802       498  LOAD_FAST                'otp_token_entry'

 L. 797       500  CALL_METHOD_5         5  ''
              502  POP_TOP          

 L. 807       504  LOAD_FAST                'self'
              506  LOAD_METHOD              _check_validity_period

 L. 808       508  LOAD_FAST                'user_entry'

 L. 809       510  LOAD_FAST                'self'
              512  LOAD_ATTR                server
              514  LOAD_ATTR                cfg
              516  LOAD_ATTR                user_notbefore_attr

 L. 810       518  LOAD_FAST                'self'
              520  LOAD_ATTR                server
              522  LOAD_ATTR                cfg
              524  LOAD_ATTR                user_notafter_attr

 L. 807       526  CALL_METHOD_3         3  ''
          528_530  POP_JUMP_IF_TRUE    584  'to 584'

 L. 813       532  LOAD_FAST                'self'
              534  LOAD_METHOD              _log

 L. 814       536  LOAD_GLOBAL              logging
              538  LOAD_ATTR                WARN

 L. 815       540  LOAD_STR                 'Validity period of %r violated! => %s'

 L. 816       542  LOAD_FAST                'request'
              544  LOAD_ATTR                dn

 L. 817       546  LOAD_GLOBAL              InvalidCredentialsResponse
              548  LOAD_ATTR                __name__

 L. 813       550  CALL_METHOD_4         4  ''
              552  POP_TOP          

 L. 819       554  LOAD_GLOBAL              InvalidCredentialsResponse
              556  LOAD_FAST                'request'
              558  LOAD_ATTR                msgid
              560  LOAD_FAST                'self'
              562  LOAD_ATTR                infomsg
              564  LOAD_FAST                'self'
              566  LOAD_ATTR                server
              568  LOAD_ATTR                cfg
              570  LOAD_ATTR                response_info
              572  BINARY_SUBSCR    
              574  LOAD_ATTR                ENTRY_NOT_VALID
              576  CALL_FUNCTION_2       2  ''
              578  STORE_FAST               'response'
          580_582  JUMP_FORWARD        904  'to 904'
            584_0  COME_FROM           528  '528'

 L. 821       584  LOAD_FAST                'oath_token_identifier'
              586  LOAD_FAST                'oath_token_identifier_req'
              588  LOAD_METHOD              decode
              590  LOAD_STR                 'utf-8'
              592  CALL_METHOD_1         1  ''
              594  COMPARE_OP               !=
          596_598  POP_JUMP_IF_FALSE   650  'to 650'

 L. 823       600  LOAD_FAST                'self'
              602  LOAD_METHOD              _log

 L. 824       604  LOAD_GLOBAL              logging
              606  LOAD_ATTR                WARN

 L. 825       608  LOAD_STR                 'Token ID mismatch! oath_token_identifier=%r / oath_token_identifier_req=%r => %s'

 L. 826       610  LOAD_FAST                'oath_token_identifier'

 L. 827       612  LOAD_FAST                'oath_token_identifier_req'

 L. 828       614  LOAD_GLOBAL              InvalidCredentialsResponse
              616  LOAD_ATTR                __name__

 L. 823       618  CALL_METHOD_5         5  ''
              620  POP_TOP          

 L. 830       622  LOAD_GLOBAL              InvalidCredentialsResponse
              624  LOAD_FAST                'request'
              626  LOAD_ATTR                msgid
              628  LOAD_FAST                'self'
              630  LOAD_ATTR                infomsg
              632  LOAD_FAST                'self'
              634  LOAD_ATTR                server
              636  LOAD_ATTR                cfg
              638  LOAD_ATTR                response_info
              640  BINARY_SUBSCR    
              642  LOAD_ATTR                HOTP_WRONG_TOKEN_ID
              644  CALL_FUNCTION_2       2  ''
              646  STORE_FAST               'response'
              648  JUMP_FORWARD        904  'to 904'
            650_0  COME_FROM           596  '596'

 L. 832       650  LOAD_FAST                'oath_max_usage_count'
              652  LOAD_CONST               0
              654  COMPARE_OP               >=
          656_658  POP_JUMP_IF_FALSE   722  'to 722'

 L. 833       660  LOAD_FAST                'oath_hotp_current_counter'
              662  LOAD_FAST                'oath_max_usage_count'
              664  COMPARE_OP               >

 L. 832   666_668  POP_JUMP_IF_FALSE   722  'to 722'

 L. 835       670  LOAD_FAST                'self'
              672  LOAD_METHOD              _log

 L. 836       674  LOAD_GLOBAL              logging
              676  LOAD_ATTR                INFO

 L. 837       678  LOAD_STR                 'counter limit %d exceeded for %r => %s'

 L. 838       680  LOAD_FAST                'oath_max_usage_count'

 L. 839       682  LOAD_FAST                'request'
              684  LOAD_ATTR                dn

 L. 840       686  LOAD_GLOBAL              InvalidCredentialsResponse
              688  LOAD_ATTR                __name__

 L. 835       690  CALL_METHOD_5         5  ''
              692  POP_TOP          

 L. 842       694  LOAD_GLOBAL              InvalidCredentialsResponse
              696  LOAD_FAST                'request'
              698  LOAD_ATTR                msgid
              700  LOAD_FAST                'self'
              702  LOAD_ATTR                infomsg
              704  LOAD_FAST                'self'
              706  LOAD_ATTR                server
              708  LOAD_ATTR                cfg
              710  LOAD_ATTR                response_info
              712  BINARY_SUBSCR    
              714  LOAD_ATTR                HOTP_COUNTER_EXCEEDED
              716  CALL_FUNCTION_2       2  ''
              718  STORE_FAST               'response'
              720  JUMP_FORWARD        904  'to 904'
            722_0  COME_FROM           666  '666'
            722_1  COME_FROM           656  '656'

 L. 844       722  LOAD_GLOBAL              is_expired

 L. 845       724  LOAD_FAST                'oath_token_secret_time'

 L. 846       726  LOAD_FAST                'oath_secret_max_age'

 L. 847       728  LOAD_FAST                'self'
              730  LOAD_ATTR                now_dt

 L. 848       732  LOAD_CONST               0

 L. 844       734  LOAD_CONST               ('now', 'disable_secs')
              736  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
          738_740  POP_JUMP_IF_FALSE   798  'to 798'

 L. 851       742  LOAD_FAST                'self'
              744  LOAD_METHOD              _log

 L. 852       746  LOAD_GLOBAL              logging
              748  LOAD_ATTR                INFO

 L. 854       750  LOAD_STR                 'Token %r of %r is expired (oath_token_secret_time=%r, oath_secret_max_age=%r) => %s'

 L. 857       752  LOAD_FAST                'oath_token_dn'

 L. 858       754  LOAD_FAST                'request'
              756  LOAD_ATTR                dn

 L. 859       758  LOAD_FAST                'oath_token_secret_time'

 L. 860       760  LOAD_FAST                'oath_secret_max_age'

 L. 861       762  LOAD_GLOBAL              InvalidCredentialsResponse
              764  LOAD_ATTR                __name__

 L. 851       766  CALL_METHOD_7         7  ''
              768  POP_TOP          

 L. 863       770  LOAD_GLOBAL              InvalidCredentialsResponse
              772  LOAD_FAST                'request'
              774  LOAD_ATTR                msgid
              776  LOAD_FAST                'self'
              778  LOAD_ATTR                infomsg
              780  LOAD_FAST                'self'
              782  LOAD_ATTR                server
              784  LOAD_ATTR                cfg
              786  LOAD_ATTR                response_info
              788  BINARY_SUBSCR    
              790  LOAD_ATTR                OTP_TOKEN_EXPIRED
              792  CALL_FUNCTION_2       2  ''
              794  STORE_FAST               'response'
              796  JUMP_FORWARD        904  'to 904'
            798_0  COME_FROM           738  '738'

 L. 865       798  LOAD_FAST                'user_password_compare'
          800_802  POP_JUMP_IF_FALSE   810  'to 810'
              804  LOAD_FAST                'otp_compare'
          806_808  POP_JUMP_IF_TRUE    876  'to 876'
            810_0  COME_FROM           800  '800'

 L. 867       810  LOAD_FAST                'self'
              812  LOAD_METHOD              _log

 L. 868       814  LOAD_GLOBAL              logging
              816  LOAD_ATTR                INFO

 L. 870       818  LOAD_STR                 'Verification failed for %r (user_password_compare=%s / otp_compare=%s) => %s'

 L. 872       820  LOAD_FAST                'request'
              822  LOAD_ATTR                dn

 L. 873       824  LOAD_FAST                'user_password_compare'

 L. 874       826  LOAD_FAST                'otp_compare'

 L. 875       828  LOAD_GLOBAL              InvalidCredentialsResponse
              830  LOAD_ATTR                __name__

 L. 867       832  CALL_METHOD_6         6  ''
              834  POP_TOP          

 L. 877       836  LOAD_GLOBAL              InvalidCredentialsResponse

 L. 878       838  LOAD_FAST                'request'
              840  LOAD_ATTR                msgid

 L. 879       842  LOAD_FAST                'self'
              844  LOAD_ATTR                infomsg
              846  LOAD_FAST                'self'
              848  LOAD_ATTR                server
              850  LOAD_ATTR                cfg
              852  LOAD_ATTR                response_info
              854  BINARY_SUBSCR    
              856  LOAD_ATTR                VERIFICATION_FAILED
              858  LOAD_ATTR                format

 L. 880       860  LOAD_FAST                'user_password_compare'

 L. 881       862  LOAD_FAST                'otp_compare'

 L. 879       864  LOAD_CONST               ('user_password_compare', 'otp_compare')
              866  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 877       868  LOAD_CONST               ('info',)
              870  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              872  STORE_FAST               'response'
              874  JUMP_FORWARD        904  'to 904'
            876_0  COME_FROM           806  '806'

 L. 887       876  LOAD_FAST                'self'
              878  LOAD_METHOD              _log

 L. 888       880  LOAD_GLOBAL              logging
              882  LOAD_ATTR                INFO

 L. 889       884  LOAD_STR                 'Validation ok for %r => response = success'

 L. 890       886  LOAD_FAST                'request'
              888  LOAD_ATTR                dn

 L. 887       890  CALL_METHOD_3         3  ''
              892  POP_TOP          

 L. 892       894  LOAD_GLOBAL              SuccessResponse
              896  LOAD_FAST                'request'
              898  LOAD_ATTR                msgid
              900  CALL_FUNCTION_1       1  ''
              902  STORE_FAST               'response'
            904_0  COME_FROM           874  '874'
            904_1  COME_FROM           796  '796'
            904_2  COME_FROM           720  '720'
            904_3  COME_FROM           648  '648'
            904_4  COME_FROM           580  '580'

 L. 894       904  LOAD_FAST                'self'
              906  LOAD_METHOD              _update_pwdfailuretime

 L. 895       908  LOAD_FAST                'request'
              910  LOAD_ATTR                dn

 L. 896       912  LOAD_FAST                'user_entry'

 L. 897       914  LOAD_GLOBAL              isinstance
              916  LOAD_FAST                'response'
              918  LOAD_GLOBAL              SuccessResponse
              920  CALL_FUNCTION_2       2  ''

 L. 894       922  CALL_METHOD_3         3  ''
              924  POP_TOP          

 L. 900       926  LOAD_FAST                'response'
              928  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 222

        def do_compare--- This code section failed: ---

 L. 910         0  LOAD_FAST                'request'
                2  LOAD_ATTR                atype
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                compare_assertion_type
                8  COMPARE_OP               !=
               10  POP_JUMP_IF_FALSE    38  'to 38'

 L. 911        12  LOAD_FAST                'self'
               14  LOAD_METHOD              _log

 L. 912        16  LOAD_GLOBAL              logging
               18  LOAD_ATTR                DEBUG

 L. 913        20  LOAD_STR                 'Assertion type %r does not match %r => CONTINUE'

 L. 914        22  LOAD_FAST                'request'
               24  LOAD_ATTR                atype

 L. 915        26  LOAD_FAST                'self'
               28  LOAD_ATTR                compare_assertion_type

 L. 911        30  CALL_METHOD_4         4  ''
               32  POP_TOP          

 L. 917        34  LOAD_GLOBAL              CONTINUE_RESPONSE
               36  RETURN_VALUE     
             38_0  COME_FROM            10  '10'

 L. 920        38  LOAD_FAST                'self'
               40  LOAD_ATTR                server
               42  LOAD_METHOD              get_ldapi_conn
               44  CALL_METHOD_0         0  ''
               46  LOAD_FAST                'self'
               48  STORE_ATTR               _ldapi_conn

 L. 923        50  LOAD_FAST                'self'
               52  LOAD_METHOD              _get_user_entry
               54  LOAD_FAST                'request'
               56  LOAD_GLOBAL              InternalErrorResponse
               58  CALL_METHOD_2         2  ''
               60  UNPACK_SEQUENCE_2     2 
               62  STORE_FAST               'user_entry'
               64  STORE_FAST               'response'

 L. 924        66  LOAD_FAST                'user_entry'
               68  LOAD_CONST               None
               70  COMPARE_OP               is
               72  POP_JUMP_IF_FALSE    78  'to 78'

 L. 925        74  LOAD_FAST                'response'
               76  RETURN_VALUE     
             78_0  COME_FROM            72  '72'

 L. 928        78  LOAD_FAST                'self'
               80  LOAD_METHOD              _get_oath_token_entry
               82  LOAD_FAST                'request'
               84  LOAD_ATTR                dn
               86  LOAD_FAST                'user_entry'
               88  CALL_METHOD_2         2  ''
               90  UNPACK_SEQUENCE_2     2 
               92  STORE_FAST               'oath_token_dn'
               94  STORE_FAST               'otp_token_entry'

 L. 929        96  LOAD_FAST                'otp_token_entry'
               98  POP_JUMP_IF_TRUE    126  'to 126'

 L. 931       100  LOAD_GLOBAL              InvalidCredentialsResponse
              102  LOAD_FAST                'request'
              104  LOAD_ATTR                msgid
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                infomsg
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                server
              114  LOAD_ATTR                cfg
              116  LOAD_ATTR                response_info
              118  BINARY_SUBSCR    
              120  LOAD_ATTR                OTP_TOKEN_ERROR
              122  CALL_FUNCTION_2       2  ''
              124  RETURN_VALUE     
            126_0  COME_FROM            98  '98'

 L. 934       126  LOAD_FAST                'otp_token_entry'
              128  LOAD_METHOD              get
              130  LOAD_STR                 'oathTokenIdentifier'
              132  LOAD_STR                 ''
              134  BUILD_LIST_1          1 
              136  CALL_METHOD_2         2  ''
              138  LOAD_CONST               0
              140  BINARY_SUBSCR    
              142  STORE_FAST               'oath_token_identifier'

 L. 935       144  LOAD_FAST                'otp_token_entry'
              146  LOAD_METHOD              get

 L. 936       148  LOAD_STR                 'oathSecretTime'

 L. 937       150  LOAD_FAST                'otp_token_entry'
              152  LOAD_METHOD              get

 L. 938       154  LOAD_STR                 'createTimestamp'

 L. 939       156  LOAD_CONST               None
              158  BUILD_LIST_1          1 

 L. 937       160  CALL_METHOD_2         2  ''

 L. 935       162  CALL_METHOD_2         2  ''

 L. 941       164  LOAD_CONST               0

 L. 935       166  BINARY_SUBSCR    
              168  STORE_FAST               'oath_token_secret_time'

 L. 944       170  SETUP_FINALLY       204  'to 204'

 L. 945       172  LOAD_GLOBAL              int
              174  LOAD_FAST                'otp_token_entry'
              176  LOAD_STR                 'oathHOTPCounter'
              178  BINARY_SUBSCR    
              180  LOAD_CONST               0
              182  BINARY_SUBSCR    
              184  CALL_FUNCTION_1       1  ''
              186  STORE_FAST               'oath_hotp_current_counter'

 L. 946       188  LOAD_FAST                'otp_token_entry'
              190  LOAD_STR                 'oathSecret'
              192  BINARY_SUBSCR    
              194  LOAD_CONST               0
              196  BINARY_SUBSCR    
              198  STORE_FAST               'oath_secret'
              200  POP_BLOCK        
              202  JUMP_FORWARD        276  'to 276'
            204_0  COME_FROM_FINALLY   170  '170'

 L. 947       204  DUP_TOP          
              206  LOAD_GLOBAL              KeyError
              208  COMPARE_OP               exception-match
          210_212  POP_JUMP_IF_FALSE   274  'to 274'
              214  POP_TOP          
              216  STORE_FAST               'err'
              218  POP_TOP          
              220  SETUP_FINALLY       262  'to 262'

 L. 948       222  LOAD_FAST                'self'
              224  LOAD_METHOD              _log

 L. 949       226  LOAD_GLOBAL              logging
              228  LOAD_ATTR                ERROR

 L. 950       230  LOAD_STR                 'Missing OATH attributes in %r: %s => %s'

 L. 951       232  LOAD_FAST                'oath_token_dn'

 L. 952       234  LOAD_FAST                'err'

 L. 953       236  LOAD_GLOBAL              InvalidCredentialsResponse
              238  LOAD_ATTR                __name__

 L. 948       240  CALL_METHOD_5         5  ''
              242  POP_TOP          

 L. 955       244  LOAD_GLOBAL              InvalidCredentialsResponse
              246  LOAD_FAST                'request'
              248  LOAD_ATTR                msgid
              250  CALL_FUNCTION_1       1  ''
              252  ROT_FOUR         
              254  POP_BLOCK        
              256  POP_EXCEPT       
              258  CALL_FINALLY        262  'to 262'
              260  RETURN_VALUE     
            262_0  COME_FROM           258  '258'
            262_1  COME_FROM_FINALLY   220  '220'
              262  LOAD_CONST               None
              264  STORE_FAST               'err'
              266  DELETE_FAST              'err'
              268  END_FINALLY      
              270  POP_EXCEPT       
              272  JUMP_FORWARD        276  'to 276'
            274_0  COME_FROM           210  '210'
              274  END_FINALLY      
            276_0  COME_FROM           272  '272'
            276_1  COME_FROM           202  '202'

 L. 958       276  LOAD_FAST                'self'
              278  LOAD_METHOD              _get_oath_token_params
              280  LOAD_FAST                'otp_token_entry'
              282  CALL_METHOD_1         1  ''

 L. 957       284  UNPACK_SEQUENCE_4     4 
              286  STORE_FAST               'oath_otp_length'
              288  STORE_FAST               'oath_hotp_lookahead'
              290  STORE_FAST               'oath_max_usage_count'
              292  STORE_FAST               'oath_secret_max_age'

 L. 965       294  LOAD_FAST                'request'
              296  LOAD_ATTR                avalue
              298  LOAD_CONST               0
              300  LOAD_FAST                'oath_otp_length'
              302  UNARY_NEGATIVE   
              304  BUILD_SLICE_2         2 
              306  BINARY_SUBSCR    

 L. 966       308  LOAD_FAST                'request'
              310  LOAD_ATTR                avalue
              312  LOAD_FAST                'oath_otp_length'
              314  UNARY_NEGATIVE   
              316  LOAD_CONST               None
              318  BUILD_SLICE_2         2 
              320  BINARY_SUBSCR    

 L. 964       322  ROT_TWO          
              324  STORE_FAST               'oath_token_identifier_req'
              326  STORE_FAST               'otp_value'

 L. 970       328  LOAD_FAST                'otp_value'
          330_332  POP_JUMP_IF_TRUE    358  'to 358'

 L. 971       334  LOAD_CONST               None
              336  STORE_FAST               'oath_hotp_next_counter'

 L. 973       338  LOAD_FAST                'self'
              340  LOAD_METHOD              _log

 L. 974       342  LOAD_GLOBAL              logging
              344  LOAD_ATTR                WARN

 L. 975       346  LOAD_STR                 'Empty OTP value sent for %r'

 L. 976       348  LOAD_FAST                'request'
              350  LOAD_ATTR                dn

 L. 973       352  CALL_METHOD_3         3  ''
              354  POP_TOP          
              356  JUMP_FORWARD        450  'to 450'
            358_0  COME_FROM           330  '330'

 L. 981       358  LOAD_FAST                'self'
              360  LOAD_ATTR                _check_hotp

 L. 982       362  LOAD_FAST                'oath_secret'

 L. 983       364  LOAD_FAST                'otp_value'

 L. 984       366  LOAD_FAST                'oath_hotp_current_counter'

 L. 985       368  LOAD_FAST                'oath_otp_length'

 L. 986       370  LOAD_FAST                'oath_hotp_lookahead'

 L. 981       372  LOAD_CONST               ('length', 'drift')
              374  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              376  STORE_FAST               'oath_hotp_next_counter'

 L. 988       378  LOAD_FAST                'oath_hotp_next_counter'
              380  LOAD_CONST               None
              382  COMPARE_OP               is-not
          384_386  POP_JUMP_IF_FALSE   434  'to 434'

 L. 989       388  LOAD_FAST                'oath_hotp_next_counter'
              390  LOAD_FAST                'oath_hotp_current_counter'
              392  BINARY_SUBTRACT  
              394  STORE_FAST               'oath_hotp_drift'

 L. 990       396  LOAD_FAST                'self'
              398  LOAD_METHOD              _log

 L. 991       400  LOAD_GLOBAL              logging
              402  LOAD_ATTR                DEBUG

 L. 992       404  LOAD_STR                 'OTP value valid (drift %d) for %r'

 L. 993       406  LOAD_FAST                'oath_hotp_drift'

 L. 994       408  LOAD_FAST                'oath_token_dn'

 L. 990       410  CALL_METHOD_4         4  ''
              412  POP_TOP          

 L. 997       414  LOAD_GLOBAL              max

 L. 998       416  LOAD_FAST                'self'
              418  LOAD_ATTR                server
              420  LOAD_ATTR                max_lookahead_seen

 L. 999       422  LOAD_FAST                'oath_hotp_drift'

 L. 997       424  CALL_FUNCTION_2       2  ''
              426  LOAD_FAST                'self'
              428  LOAD_ATTR                server
              430  STORE_ATTR               max_lookahead_seen
              432  JUMP_FORWARD        450  'to 450'
            434_0  COME_FROM           384  '384'

 L.1002       434  LOAD_FAST                'self'
              436  LOAD_METHOD              _log

 L.1003       438  LOAD_GLOBAL              logging
              440  LOAD_ATTR                DEBUG

 L.1004       442  LOAD_STR                 'OTP value invalid for %r'

 L.1005       444  LOAD_FAST                'oath_token_dn'

 L.1002       446  CALL_METHOD_3         3  ''
              448  POP_TOP          
            450_0  COME_FROM           432  '432'
            450_1  COME_FROM           356  '356'

 L.1008       450  LOAD_FAST                'oath_hotp_next_counter'
              452  LOAD_CONST               None
              454  COMPARE_OP               is-not
              456  STORE_FAST               'otp_compare'

 L.1012       458  LOAD_FAST                'self'
              460  LOAD_METHOD              _update_token_entry

 L.1013       462  LOAD_FAST                'request'

 L.1014       464  LOAD_FAST                'oath_token_dn'

 L.1015       466  LOAD_FAST                'otp_compare'
          468_470  JUMP_IF_FALSE_OR_POP   478  'to 478'
              472  LOAD_FAST                'oath_token_identifier'
              474  LOAD_FAST                'oath_token_identifier_req'
              476  COMPARE_OP               ==
            478_0  COME_FROM           468  '468'

 L.1016       478  LOAD_FAST                'oath_hotp_next_counter'

 L.1017       480  LOAD_FAST                'otp_token_entry'

 L.1012       482  CALL_METHOD_5         5  ''
              484  POP_TOP          

 L.1022       486  LOAD_FAST                'self'
              488  LOAD_METHOD              _check_validity_period

 L.1023       490  LOAD_FAST                'user_entry'

 L.1024       492  LOAD_FAST                'self'
              494  LOAD_ATTR                server
              496  LOAD_ATTR                cfg
              498  LOAD_ATTR                user_notbefore_attr

 L.1025       500  LOAD_FAST                'self'
              502  LOAD_ATTR                server
              504  LOAD_ATTR                cfg
              506  LOAD_ATTR                user_notafter_attr

 L.1022       508  CALL_METHOD_3         3  ''
          510_512  POP_JUMP_IF_TRUE    566  'to 566'

 L.1028       514  LOAD_FAST                'self'
              516  LOAD_METHOD              _log

 L.1029       518  LOAD_GLOBAL              logging
              520  LOAD_ATTR                WARN

 L.1030       522  LOAD_STR                 'Validity period of %r violated! => %s'

 L.1031       524  LOAD_FAST                'request'
              526  LOAD_ATTR                dn

 L.1032       528  LOAD_GLOBAL              InvalidCredentialsResponse
              530  LOAD_ATTR                __name__

 L.1028       532  CALL_METHOD_4         4  ''
              534  POP_TOP          

 L.1034       536  LOAD_GLOBAL              CompareFalseResponse
              538  LOAD_FAST                'request'
              540  LOAD_ATTR                msgid
              542  LOAD_FAST                'self'
              544  LOAD_ATTR                infomsg
              546  LOAD_FAST                'self'
              548  LOAD_ATTR                server
              550  LOAD_ATTR                cfg
              552  LOAD_ATTR                response_info
              554  BINARY_SUBSCR    
              556  LOAD_ATTR                ENTRY_NOT_VALID
              558  CALL_FUNCTION_2       2  ''
              560  STORE_FAST               'response'
          562_564  JUMP_FORWARD        842  'to 842'
            566_0  COME_FROM           510  '510'

 L.1036       566  LOAD_FAST                'oath_token_identifier'
              568  LOAD_FAST                'oath_token_identifier_req'
              570  COMPARE_OP               !=
          572_574  POP_JUMP_IF_FALSE   626  'to 626'

 L.1038       576  LOAD_FAST                'self'
              578  LOAD_METHOD              _log

 L.1039       580  LOAD_GLOBAL              logging
              582  LOAD_ATTR                WARN

 L.1040       584  LOAD_STR                 'Token ID mismatch! oath_token_identifier=%r / oath_token_identifier_req=%r => %s'

 L.1041       586  LOAD_FAST                'oath_token_identifier'

 L.1042       588  LOAD_FAST                'oath_token_identifier_req'

 L.1043       590  LOAD_GLOBAL              InvalidCredentialsResponse
              592  LOAD_ATTR                __name__

 L.1038       594  CALL_METHOD_5         5  ''
              596  POP_TOP          

 L.1045       598  LOAD_GLOBAL              CompareFalseResponse
              600  LOAD_FAST                'request'
              602  LOAD_ATTR                msgid
              604  LOAD_FAST                'self'
              606  LOAD_ATTR                infomsg
              608  LOAD_FAST                'self'
              610  LOAD_ATTR                server
              612  LOAD_ATTR                cfg
              614  LOAD_ATTR                response_info
              616  BINARY_SUBSCR    
              618  LOAD_ATTR                HOTP_WRONG_TOKEN_ID
              620  CALL_FUNCTION_2       2  ''
              622  STORE_FAST               'response'
              624  JUMP_FORWARD        842  'to 842'
            626_0  COME_FROM           572  '572'

 L.1047       626  LOAD_FAST                'oath_max_usage_count'
              628  LOAD_CONST               0
              630  COMPARE_OP               >=
          632_634  POP_JUMP_IF_FALSE   698  'to 698'

 L.1048       636  LOAD_FAST                'oath_hotp_current_counter'
              638  LOAD_FAST                'oath_max_usage_count'
              640  COMPARE_OP               >

 L.1047   642_644  POP_JUMP_IF_FALSE   698  'to 698'

 L.1050       646  LOAD_FAST                'self'
              648  LOAD_METHOD              _log

 L.1051       650  LOAD_GLOBAL              logging
              652  LOAD_ATTR                INFO

 L.1052       654  LOAD_STR                 'counter limit %d exceeded for %r => %s'

 L.1053       656  LOAD_FAST                'oath_max_usage_count'

 L.1054       658  LOAD_FAST                'request'
              660  LOAD_ATTR                dn

 L.1055       662  LOAD_GLOBAL              InvalidCredentialsResponse
              664  LOAD_ATTR                __name__

 L.1050       666  CALL_METHOD_5         5  ''
              668  POP_TOP          

 L.1057       670  LOAD_GLOBAL              CompareFalseResponse
              672  LOAD_FAST                'request'
              674  LOAD_ATTR                msgid
              676  LOAD_FAST                'self'
              678  LOAD_ATTR                infomsg
              680  LOAD_FAST                'self'
              682  LOAD_ATTR                server
              684  LOAD_ATTR                cfg
              686  LOAD_ATTR                response_info
              688  BINARY_SUBSCR    
              690  LOAD_ATTR                HOTP_COUNTER_EXCEEDED
              692  CALL_FUNCTION_2       2  ''
              694  STORE_FAST               'response'
              696  JUMP_FORWARD        842  'to 842'
            698_0  COME_FROM           642  '642'
            698_1  COME_FROM           632  '632'

 L.1059       698  LOAD_GLOBAL              is_expired

 L.1060       700  LOAD_FAST                'oath_token_secret_time'

 L.1061       702  LOAD_FAST                'oath_secret_max_age'

 L.1062       704  LOAD_FAST                'self'
              706  LOAD_ATTR                now_dt

 L.1063       708  LOAD_CONST               0

 L.1059       710  LOAD_CONST               ('now', 'disable_secs')
              712  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
          714_716  POP_JUMP_IF_FALSE   774  'to 774'

 L.1066       718  LOAD_FAST                'self'
              720  LOAD_METHOD              _log

 L.1067       722  LOAD_GLOBAL              logging
              724  LOAD_ATTR                INFO

 L.1069       726  LOAD_STR                 'Token %r of %r is expired (oath_token_secret_time=%r, oath_secret_max_age=%r) => %s'

 L.1072       728  LOAD_FAST                'oath_token_dn'

 L.1073       730  LOAD_FAST                'request'
              732  LOAD_ATTR                dn

 L.1074       734  LOAD_FAST                'oath_token_secret_time'

 L.1075       736  LOAD_FAST                'oath_secret_max_age'

 L.1076       738  LOAD_GLOBAL              InvalidCredentialsResponse
              740  LOAD_ATTR                __name__

 L.1066       742  CALL_METHOD_7         7  ''
              744  POP_TOP          

 L.1078       746  LOAD_GLOBAL              CompareFalseResponse
              748  LOAD_FAST                'request'
              750  LOAD_ATTR                msgid
              752  LOAD_FAST                'self'
              754  LOAD_ATTR                infomsg
              756  LOAD_FAST                'self'
              758  LOAD_ATTR                server
              760  LOAD_ATTR                cfg
              762  LOAD_ATTR                response_info
              764  BINARY_SUBSCR    
              766  LOAD_ATTR                OTP_TOKEN_EXPIRED
              768  CALL_FUNCTION_2       2  ''
              770  STORE_FAST               'response'
              772  JUMP_FORWARD        842  'to 842'
            774_0  COME_FROM           714  '714'

 L.1080       774  LOAD_FAST                'otp_compare'
          776_778  POP_JUMP_IF_TRUE    814  'to 814'

 L.1082       780  LOAD_FAST                'self'
              782  LOAD_METHOD              _log

 L.1083       784  LOAD_GLOBAL              logging
              786  LOAD_ATTR                INFO

 L.1084       788  LOAD_STR                 'HOTP verification failed for %r => %s'

 L.1085       790  LOAD_FAST                'request'
              792  LOAD_ATTR                dn

 L.1086       794  LOAD_GLOBAL              InvalidCredentialsResponse
              796  LOAD_ATTR                __name__

 L.1082       798  CALL_METHOD_4         4  ''
              800  POP_TOP          

 L.1088       802  LOAD_GLOBAL              CompareFalseResponse
              804  LOAD_FAST                'request'
              806  LOAD_ATTR                msgid
              808  CALL_FUNCTION_1       1  ''
              810  STORE_FAST               'response'
              812  JUMP_FORWARD        842  'to 842'
            814_0  COME_FROM           776  '776'

 L.1092       814  LOAD_FAST                'self'
              816  LOAD_METHOD              _log

 L.1093       818  LOAD_GLOBAL              logging
              820  LOAD_ATTR                INFO

 L.1094       822  LOAD_STR                 'Validation ok for %r => response = success'

 L.1095       824  LOAD_FAST                'request'
              826  LOAD_ATTR                dn

 L.1092       828  CALL_METHOD_3         3  ''
              830  POP_TOP          

 L.1097       832  LOAD_GLOBAL              CompareTrueResponse
              834  LOAD_FAST                'request'
              836  LOAD_ATTR                msgid
              838  CALL_FUNCTION_1       1  ''
              840  STORE_FAST               'response'
            842_0  COME_FROM           812  '812'
            842_1  COME_FROM           772  '772'
            842_2  COME_FROM           696  '696'
            842_3  COME_FROM           624  '624'
            842_4  COME_FROM           562  '562'

 L.1099       842  LOAD_FAST                'response'
              844  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 254


    def run():
        """
    The main script
    """
        scfg = HOTPValidatorConfig(sys.argv[1])
        my_logger = init_logger(scfg)
        my_logger.info('Starting %s %s (log level %d)', os.path.basename(os.path.abspath(sys.argv[0])), __version__, my_logger.level)
        for name in sorted(dir(scfg)):
            if not name.startswith('__'):
                my_logger.debug('%s.%s = %r', scfg.__class__.__name__, name, getattr(scfg, name))
            my_logger.error("!!! Running in debug mode (log level %d)! Secret data will be logged! Don't do that!!!", my_logger.level)
            try:
                slapd_sock_listener = HOTPValidationServer(scfg, my_logger)
                try:
                    slapd_sock_listener.serve_forever()
                except KeyboardInterrupt:
                    my_logger.warning('Received interrupt signal => shutdown')

            finally:
                my_logger.debug('Removing socket path %r', scfg.socket_path)
                try:
                    os.remove(scfg.socket_path)
                except OSError:
                    pass


    if __name__ == '__main__':
        run()