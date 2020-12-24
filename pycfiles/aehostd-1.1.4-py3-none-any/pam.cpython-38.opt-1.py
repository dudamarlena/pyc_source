# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /aehostd/pam.py
# Compiled at: 2020-05-10 16:57:15
# Size of source mod 2**32: 17032 bytes
"""
aehostd.pam - PAM authentication, authorisation and session handling
"""
import time, hashlib, logging, socket, threading, ldap0
from ldap0.controls.ppolicy import PasswordPolicyControl
import ldap0.filter
from ldap0.controls.sessiontrack import SessionTrackingControl, SESSION_TRACKING_FORMAT_OID_USERNAME
from ldap0.pw import random_string
import aedir
from .cfg import CFG
from . import req
from .passwd import PASSWD_NAME_MAP
from .ldapconn import LDAP_CONN
from . import refresh
PAM_REQ_AUTHC = 851969
PAM_REQ_AUTHZ = 851970
PAM_REQ_SESS_O = 851971
PAM_REQ_SESS_C = 851972
PAM_REQ_PWMOD = 851973
PAM_SUCCESS = 0
PAM_PERM_DENIED = 6
PAM_AUTH_ERR = 7
PAM_CRED_INSUFFICIENT = 8
PAM_AUTHINFO_UNAVAIL = 9
PAM_USER_UNKNOWN = 10
PAM_MAXTRIES = 11
PAM_NEW_AUTHTOK_REQD = 12
PAM_ACCT_EXPIRED = 13
PAM_SESSION_ERR = 14
PAM_AUTHTOK_ERR = 20
PAM_AUTHTOK_DISABLE_AGING = 23
PAM_IGNORE = 25
PAM_ABORT = 26
PAM_AUTHTOK_EXPIRED = 27
SESSION_ID_LENGTH = 25
SESSION_ID_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01234567890'
AUTHC_CACHE = {}

class AuthcCachePurgeThread(threading.Thread):
    __doc__ = '\n    Thread for purging expired entries from global AUTHC_CACHE\n    '
    schedule_interval = 0.4

    def __init__(self, purge_interval):
        threading.Thread.__init__(self,
          group=None,
          target=None,
          name=None,
          args=(),
          kwargs={})
        self.purge_interval = purge_interval
        self.enabled = True
        self._next_run = time.time()

    @staticmethod
    def _purge_expired(current_time):
        del_cache_keys = []
        for cache_key, val in AUTHC_CACHE.items():
            _, _, _, etime = val
            if etime < current_time:
                logging.debug('Cached PAM authc result expired => will remove it')
                del_cache_keys.append(cache_key)
            logging.debug('Found %d expired PAM authc results', len(del_cache_keys))
            expired = 0

        for cache_key in del_cache_keys:
            try:
                del AUTHC_CACHE[cache_key]
            except KeyError:
                pass
            else:
                expired += 1
        else:
            if expired:
                logging.info('Expired %d PAM authc result from cache', expired)

    def run(self):
        """
        retrieve data forever
        """
        logging.debug('Starting %s.run()', self.__class__.__name__)
        while self.enabled:
            current_time = time.time()
            if current_time > self._next_run:
                logging.debug('Invoking %s._purge_expired()', self.__class__.__name__)
                self._purge_expired(current_time)
                self._last_run = current_time
                self._next_run = current_time + self.purge_interval
            time.sleep(self.schedule_interval)

        logging.debug('Exiting %s.run()', self.__class__.__name__)


class PAMRequest(req.Request):
    __doc__ = '\n    base class for handling PAM requests (not directly used)\n    '

    def _get_rhost(self, params):
        if 'rhost' in params:
            if params['rhost']:
                return params['rhost']
        peer_env = self._get_peer_env(names=('SSH_CLIENT', ))
        self._log(logging.DEBUG, 'Retrieved peer env vars: %r', peer_env)
        return peer_env.get('SSH_CLIENT', '').split(' ')[0]

    def _session_tracking_control(self):
        """
        return SessionTrackingControl instance based on params
        """
        return SessionTrackingControl(self._params['rhost'], '%s::%s' % (socket.getfqdn(), self._params['service']), SESSION_TRACKING_FORMAT_OID_USERNAME, self._params.get('ruser', self._params['username']))


class PAMAuthcReq(PAMRequest):
    __doc__ = '\n    handles PAM authc requests\n    '
    rtype = PAM_REQ_AUTHC

    def _read_params(self) -> dict:
        params = dict(username=(self.tios.read_string()),
          service=(self.tios.read_string()),
          ruser=(self.tios.read_string()),
          rhost=(self.tios.read_string()),
          tty=(self.tios.read_string()),
          password=(self.tios.read_string()))
        params['rhost'] = self._get_rhost(params)
        return params

    def write(self, username, authc, authz, msg):
        """
        write result to PAM client
        """
        self.tios.write_int32(req.RES_BEGIN)
        self.tios.write_int32(authc)
        self.tios.write_string(username)
        self.tios.write_int32(authz)
        self.tios.write_string(msg)
        self.tios.write_int32(req.RES_END)

    def _cache_key(self):
        return hashlib.sha512(repr(sorted(self._params.items())).encode('ascii')).digest()

    def process(self):
        """
        handle request, mainly do LDAP simple bind
        """
        user_name = self._params['username']
        if user_name not in PASSWD_NAME_MAP:
            raise ValueError('Invalid user name %r' % user_name)
        pam_authc, pam_authz, pam_msg = PAM_AUTH_ERR, PAM_PERM_DENIED, 'Internal error'
        if CFG.pam_authc_cache_ttl > 0:
            cache_key = self._cache_key()
            try:
                pam_authc, pam_authz, pam_msg, etime = AUTHC_CACHE[cache_key]
            except KeyError:
                self._log(logging.DEBUG, 'No cached PAM authc result => proceed with LDAP simple bind')
            else:
                if etime >= time.time():
                    self._log(logging.DEBUG, 'Return cached PAM authc result: %r', (
                     pam_authc, pam_authz, pam_msg))
                    self.write(user_name, pam_authc, pam_authz, pam_msg)
                    return None
                self._log(logging.DEBUG, 'Cached PAM authc result expired => proceed with LDAP simple bind')
            ppolicy_ctrl = None
            uris = CFG.get_ldap_uris()
            if LDAP_CONN.current_ldap_uri is not None:
                uris.append(LDAP_CONN.current_ldap_uri)
            self._log(logging.DEBUG, 'Will try simple bind on servers %r', uris)
            try:
                while True:
                    ldap_uri = uris.pop()
                    self._log(logging.DEBUG, 'Try connecting to %r', ldap_uri)
                    try:
                        conn = aedir.AEDirObject(ldap_uri,
                          trace_level=0,
                          retry_max=0,
                          timeout=(CFG.timelimit),
                          cacert_filename=(CFG.tls_cacertfile),
                          cache_ttl=0.0)
                        search_base = conn.search_base
                    except ldap0.SERVER_DOWN:
                        if not uris:
                            raise
                    else:
                        self._log(logging.DEBUG, 'Connected to %r', conn.uri)
                        break

                if user_name == CFG.aehost_vaccount_t[0]:
                    self._log(logging.DEBUG, 'Use aehostd.conf binddn %r', CFG.binddn)
                    user_dn = CFG.binddn
                else:
                    self._log(logging.DEBUG, 'Construct short user bind-DN from %r and %r', user_name, search_base)
                    user_dn = 'uid=%s,%s' % (user_name, search_base)
                self._log(logging.DEBUG, 'user_dn = %r', user_dn)
                bind_res = conn.simple_bind_s(user_dn,
                  (self._params['password']),
                  req_ctrls=[
                 PasswordPolicyControl(),
                 self._session_tracking_control()])
            except ldap0.INVALID_CREDENTIALS as ldap_err:
                try:
                    self._log(logging.WARN, 'LDAP simple bind failed for %r: %s', user_dn, ldap_err)
                    pam_authc, pam_msg = PAM_AUTH_ERR, 'Wrong username or password'
                finally:
                    ldap_err = None
                    del ldap_err

            except ldap0.LDAPError as ldap_err:
                try:
                    self._log(logging.WARN, 'LDAP error checking password for %r: %s', user_dn, ldap_err)
                    pam_authc = PAM_AUTH_ERR
                finally:
                    ldap_err = None
                    del ldap_err

            else:
                self._log(logging.DEBUG, 'LDAP simple bind successful for %r on %r', user_dn, conn.uri)
                pam_authc = pam_authz = PAM_SUCCESS
                if user_name == CFG.aehost_vaccount_t[0]:
                    pam_msg = 'Host password check ok'
                    pam_authz = PAM_PERM_DENIED
                    CFG.bindpwfile.write((self._params['password'].encode('utf-8')), mode=416)
                    refresh.USERSUPDATER_TASK.reset()
                else:
                    pam_msg = 'User password check ok'
                for ctrl in bind_res.ctrls:
                    if ctrl.controlType == PasswordPolicyControl.controlType:
                        ppolicy_ctrl = ctrl
                        break
                    elif ppolicy_ctrl:
                        self._log(logging.DEBUG, 'PasswordPolicyControl: error=%r, timeBeforeExpiration=%r, graceAuthNsRemaining=%r', ppolicy_ctrl.error, ppolicy_ctrl.timeBeforeExpiration, ppolicy_ctrl.graceAuthNsRemaining)
                        if ppolicy_ctrl.error == 0:
                            pam_authz, pam_msg = PAM_AUTHTOK_EXPIRED, 'Password expired'
                            if ppolicy_ctrl.graceAuthNsRemaining is not None:
                                pam_msg += ', %d grace logins left' % (
                                 ppolicy_ctrl.graceAuthNsRemaining,)

        else:
            if ppolicy_ctrl.error is None:
                if ppolicy_ctrl.timeBeforeExpiration is not None:
                    pam_msg = 'Password will expire in %d seconds' % (
                     ppolicy_ctrl.timeBeforeExpiration,)
            if pam_authc == PAM_SUCCESS and pam_authz == PAM_SUCCESS:
                pam_log_level = logging.DEBUG
            else:
                pam_log_level = logging.WARN
            self._log(pam_log_level, 'PAM auth result for %r: authc=%d authz=%d msg=%r', user_name, pam_authc, pam_authz, pam_msg)
            if CFG.pam_authc_cache_ttl > 0:
                AUTHC_CACHE[self._cache_key()] = (
                 pam_authc,
                 pam_authz,
                 pam_msg,
                 time.time() + CFG.pam_authc_cache_ttl)
            self.write(user_name, pam_authc, pam_authz, pam_msg)


class PAMAuthzReq(PAMRequest):
    __doc__ = '\n    handles PAM authz requests\n    '
    rtype = PAM_REQ_AUTHZ

    def _read_params(self) -> dict:
        return dict(username=(self.tios.read_string()),
          service=(self.tios.read_string()),
          ruser=(self.tios.read_string()),
          rhost=(self.tios.read_string()),
          tty=(self.tios.read_string()))

    def write(self, authz, msg):
        """
        write result to PAM client
        """
        self.tios.write_int32(req.RES_BEGIN)
        self.tios.write_int32(authz)
        self.tios.write_string(msg)
        self.tios.write_int32(req.RES_END)

    def _check_authz_search(self):
        if not CFG.pam_authz_search:
            return
        variables = dict(((k, ldap0.filter.escape_str(v)) for k, v in self._params.items()))
        variables.update(hostname=(ldap0.filter.escape_str(socket.gethostname())),
          fqdn=(ldap0.filter.escape_str(socket.getfqdn())),
          uid=(variables['username']))
        filter_tmpl = CFG.pam_authz_search
        if 'rhost' in variables:
            if variables['rhost']:
                filter_tmpl = '(&%s(|(!(aeRemoteHost=*))(aeRemoteHost={rhost})))' % filter_tmpl
        ldap_filter = (filter_tmpl.format)(**variables)
        self._log(logging.DEBUG, 'check authz filter %r', ldap_filter)
        ldap_conn = LDAP_CONN.get_ldap_conn()
        ldap_conn.find_unique_entry((ldap_conn.search_base),
          filterstr=ldap_filter,
          attrlist=[
         '1.1'],
          req_ctrls=[
         self._session_tracking_control()])

    def process(self):
        """
        handle request, mainly do LDAP authz search
        """
        user_name = self._params['username']
        if user_name not in PASSWD_NAME_MAP:
            self._log(logging.WARN, 'Invalid user name %r', user_name)
            self.write(PAM_PERM_DENIED, 'Invalid user name')
            return None
        if user_name == CFG.aehost_vaccount_t[0]:
            self._log(logging.INFO, 'Reject login with host account %r', user_name)
            self.write(PAM_PERM_DENIED, 'Host account ok, but not authorized for login')
            return None
        try:
            self._check_authz_search()
        except ldap0.LDAPError as ldap_err:
            try:
                self._log(logging.WARNING, 'authz failed for %s: %s', user_name, ldap_err)
                self.write(PAM_PERM_DENIED, 'LDAP authz check failed')
            finally:
                ldap_err = None
                del ldap_err

        except (KeyError, ValueError, IndexError) as err:
            try:
                self._log(logging.WARNING, 'Value check failed for %s: %s', user_name, err)
                self.write(PAM_PERM_DENIED, 'LDAP authz check failed')
            finally:
                err = None
                del err

        else:
            self._log(logging.DEBUG, 'authz ok for %s', user_name)
            self.write(PAM_SUCCESS, '')


class PAMPassModReq(PAMRequest):
    __doc__ = '\n    handles PAM passmod requests\n    '
    rtype = PAM_REQ_PWMOD

    def _read_params(self) -> dict:
        return dict(username=(self.tios.read_string()),
          service=(self.tios.read_string()),
          ruser=(self.tios.read_string()),
          rhost=(self.tios.read_string()),
          tty=(self.tios.read_string()),
          asroot=(self.tios.read_int32()),
          oldpassword=(self.tios.read_string()),
          newpassword=(self.tios.read_string()))

    def write(self, res, msg):
        """
        write result to PAM client
        """
        self.tios.write_int32(req.RES_BEGIN)
        self.tios.write_int32(res)
        self.tios.write_string(msg)
        self.tios.write_int32(req.RES_END)

    def process(self):
        """
        handle request, just refuse password change
        """
        self.write(PAM_PERM_DENIED, CFG.pam_passmod_deny_msg)


class PAMSessOpenReq(PAMRequest):
    __doc__ = '\n    handles PAM session open requests\n    '
    rtype = PAM_REQ_SESS_O

    def _read_params(self) -> dict:
        return dict(username=(self.tios.read_string()),
          service=(self.tios.read_string()),
          ruser=(self.tios.read_string()),
          rhost=(self.tios.read_string()),
          tty=(self.tios.read_string()))

    def write(self, sessionid):
        """
        write result to PAM client
        """
        self.tios.write_int32(req.RES_BEGIN)
        self.tios.write_string(sessionid)
        self.tios.write_int32(req.RES_END)

    def process(self):
        """
        handle request, mainly return new generated session id
        """
        session_id = random_string(alphabet=SESSION_ID_ALPHABET, length=SESSION_ID_LENGTH)
        self._log(logging.DEBUG, 'New session ID: %s', session_id)
        self.write(session_id)


class PAMSessCloseReq(PAMRequest):
    __doc__ = '\n    handles PAM session close requests\n    '
    rtype = PAM_REQ_SESS_C

    def _read_params(self) -> dict:
        return dict(username=(self.tios.read_string()),
          service=(self.tios.read_string()),
          ruser=(self.tios.read_string()),
          rhost=(self.tios.read_string()),
          tty=(self.tios.read_string()),
          session_id=(self.tios.read_string()))

    def write(self):
        """
        write result to PAM client
        """
        self.tios.write_int32(req.RES_BEGIN)
        self.tios.write_int32(req.RES_END)

    def process(self):
        """
        handle request, do nothing yet
        """
        self.write()