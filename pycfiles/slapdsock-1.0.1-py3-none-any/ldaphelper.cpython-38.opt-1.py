# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /slapdsock/ldaphelper.py
# Compiled at: 2020-04-01 12:29:52
# Size of source mod 2**32: 8064 bytes
"""
slapd.ldaphelper - Helper stuff for LDAP access

slapdsock - OpenLDAP back-sock listeners with Python
see https://www.stroeder.com/slapdsock.html

(c) 2015-2019 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import ldap0
from ldap0.ldapobject import ReconnectLDAPObject
from ldap0.ldapurl import LDAPUrl
from ldap0.lock import LDAPLock
__all__ = [
 'RESULT_CODE_NAME',
 'RESULT_CODE',
 'LocalLDAPConn']
LDAP_MAXRETRYCOUNT = 10
LDAP_RETRYDELAY = 0.1
LDAP_CACHETTL = 30.0
LDAP_TIMEOUT = 3.0
RESULT_CODE_NAME = {0:'success', 
 1:'operationsError', 
 2:'protocolError', 
 3:'timeLimitExceeded', 
 4:'sizeLimitExceeded', 
 5:'compareFalse', 
 6:'compareTrue', 
 7:'authMethodNotSupported', 
 8:'strongerAuthRequired', 
 10:'referral', 
 11:'adminLimitExceeded', 
 12:'unavailableCriticalExtension', 
 13:'confidentialityRequired', 
 14:'saslBindInProgress', 
 16:'noSuchAttribute', 
 17:'undefinedAttributeType', 
 18:'inappropriateMatching', 
 19:'constraintViolation', 
 20:'attributeOrValueExists', 
 21:'invalidAttributeSyntax', 
 32:'noSuchObject', 
 33:'aliasProblem', 
 34:'invalidDNSyntax', 
 36:'aliasDereferencingProblem', 
 48:'inappropriateAuthentication', 
 49:'invalidCredentials', 
 50:'insufficientAccessRights', 
 51:'busy', 
 52:'unavailable', 
 53:'unwillingToPerform', 
 54:'loopDetect', 
 64:'namingViolation', 
 65:'objectClassViolation', 
 66:'notAllowedOnNonLeaf', 
 67:'notAllowedOnRDN', 
 68:'entryAlreadyExists', 
 69:'objectClassModsProhibited', 
 71:'affectsMultipleDSAs', 
 80:'other'}
RESULT_CODE = {k:v for k, v in RESULT_CODE_NAME.items()}
RESULT_CODE.update({ldap0.SUCCESS: 0, 
 ldap0.OPERATIONS_ERROR: 1, 
 ldap0.PROTOCOL_ERROR: 2, 
 ldap0.TIMELIMIT_EXCEEDED: 3, 
 ldap0.SIZELIMIT_EXCEEDED: 4, 
 ldap0.COMPARE_FALSE: 5, 
 ldap0.COMPARE_TRUE: 6, 
 ldap0.AUTH_METHOD_NOT_SUPPORTED: 7, 
 ldap0.STRONG_AUTH_REQUIRED: 8, 
 ldap0.PARTIAL_RESULTS: 9, 
 ldap0.ADMINLIMIT_EXCEEDED: 11, 
 ldap0.CONFIDENTIALITY_REQUIRED: 13, 
 ldap0.NO_SUCH_ATTRIBUTE: 16, 
 ldap0.UNDEFINED_TYPE: 17, 
 ldap0.INAPPROPRIATE_MATCHING: 18, 
 ldap0.CONSTRAINT_VIOLATION: 19, 
 ldap0.TYPE_OR_VALUE_EXISTS: 20, 
 ldap0.INVALID_SYNTAX: 21, 
 ldap0.NO_SUCH_OBJECT: 32, 
 ldap0.ALIAS_PROBLEM: 33, 
 ldap0.INVALID_DN_SYNTAX: 34, 
 ldap0.IS_LEAF: 35, 
 ldap0.ALIAS_DEREF_PROBLEM: 36, 
 ldap0.X_PROXY_AUTHZ_FAILURE: 47, 
 ldap0.INAPPROPRIATE_AUTH: 48, 
 ldap0.INVALID_CREDENTIALS: 49, 
 ldap0.INSUFFICIENT_ACCESS: 50, 
 ldap0.BUSY: 51, 
 ldap0.UNAVAILABLE: 52, 
 ldap0.UNWILLING_TO_PERFORM: 53, 
 ldap0.LOOP_DETECT: 54, 
 ldap0.NAMING_VIOLATION: 64, 
 ldap0.OBJECT_CLASS_VIOLATION: 65, 
 ldap0.NOT_ALLOWED_ON_NONLEAF: 66, 
 ldap0.NOT_ALLOWED_ON_RDN: 67, 
 ldap0.ALREADY_EXISTS: 68, 
 ldap0.NO_OBJECT_CLASS_MODS: 69, 
 ldap0.RESULTS_TOO_LARGE: 70, 
 ldap0.AFFECTS_MULTIPLE_DSAS: 71, 
 ldap0.VLV_ERROR: 76, 
 ldap0.OTHER: 80})
LDAP_DATETIME_FORMAT = '%Y%m%d%H%M%SZ'

def ldap_float_str(fln: float) -> str:
    """
    Return fln as string formatted for NumString
    """
    return '%0.5f' % (fln,)


class LocalLDAPConn:
    __doc__ = '\n    mix-in class providing a lazily opened local LDAP connection\n    '
    ldapi_authz_id = ''
    ldap_retry_max = 4
    ldap_retry_delay = 1.0
    ldap_timeout = LDAP_TIMEOUT
    ldap_cache_ttl = 0.0
    ldap_trace_level = 0

    def __init__(self, logger, ldapi_uri='ldapi://'):
        self._logger = logger
        self._ldapi_uri = ldapi_uri
        self._ldapi_conn = None
        self._ldapi_conn_lock = LDAPLock(desc=('get_ldapi_conn() in %s' % repr(self.__class__)))

    @property
    def ldapi_uri(self):
        """
        return LDAPI URI used internally
        """
        return self._ldapi_uri

    @ldapi_uri.setter
    def ldapi_uri(self, ldapi_uri):
        """
        set LDAPI URI used internally, current LDAPI connection is terminated
        """
        if self._ldapi_uri != ldapi_uri:
            self._ldapi_uri = ldapi_uri
            self.disable_ldapi_conn()

    def disable_ldapi_conn(self):
        """
        Destroy local LDAPI connection and reset it to None.
        Should be invoked when catching a ldap0.SERVER_DOWN exception.
        """
        try:
            self._ldapi_conn_lock.acquire()
            if self._ldapi_conn:
                self._ldapi_conn.unbind_s()
        finally:
            del self._ldapi_conn
            self._ldapi_conn = None
            self._ldapi_conn_lock.release()

    def get_ldapi_conn(self):
        """
        Open a single local LDAPI connection and bind with SASL/EXTERNAL if
        needed
        """
        if isinstance(self._ldapi_conn, ReconnectLDAPObject):
            self._logger.debug('Use existing LDAP connection to %r (%r)', self._ldapi_conn.uri, self._ldapi_conn)
            return self._ldapi_conn
        try:
            self._ldapi_conn_lock.acquire()
            try:
                self._ldapi_conn = ReconnectLDAPObject((self.ldapi_uri),
                  trace_level=(self.ldap_trace_level),
                  cache_ttl=(self.ldap_cache_ttl),
                  retry_max=(self.ldap_retry_max),
                  retry_delay=(self.ldap_retry_delay))
                self._ldapi_conn.set_option(ldap0.OPT_NETWORK_TIMEOUT, self.ldap_timeout)
                self._ldapi_conn.set_option(ldap0.OPT_TIMEOUT, self.ldap_timeout)
                self._ldapi_conn.sasl_non_interactive_bind_s('EXTERNAL',
                  authz_id=(self.ldapi_authz_id or ''))
            except ldap0.LDAPError as ldap_error:
                try:
                    self._ldapi_conn = None
                    self._logger.error('LDAPError connecting to %r: %s', self.ldapi_uri, ldap_error)
                    raise ldap_error
                finally:
                    ldap_error = None
                    del ldap_error

            else:
                self._ldapi_conn.authz_id = self._ldapi_conn.whoami_s()
                self._logger.info('Successfully bound to %s as %s (%s)', repr(self.ldapi_uri), repr(self._ldapi_conn.authz_id), repr(self._ldapi_conn))
        finally:
            self._ldapi_conn_lock.release()

        return self._ldapi_conn