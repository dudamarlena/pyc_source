# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /oathldap_srv/bind_proxy.py
# Compiled at: 2020-04-13 17:14:28
# Size of source mod 2**32: 14354 bytes
"""
oathldap_srv.bind_proxy:
slapd-sock listener demon which sends intercepted BIND requests
to a remote LDAP server if needed
"""
import sys, os, os.path, logging, logging.config, socket, collections, ipaddress, ldap0
from ldap0 import LDAPError
from ldap0.ldapurl import LDAPUrl
from ldap0.ldapobject import LDAPObject
from ldap0.controls.sessiontrack import SessionTrackingControl, SESSION_TRACKING_FORMAT_OID_USERNAME
from slapdsock.ldaphelper import RESULT_CODE
from slapdsock.handler import SlapdSockHandler, SlapdSockHandlerError
from slapdsock.message import RESULTResponse, InvalidCredentialsResponse
from slapdsock.service import SlapdSockServer
from .__about__ import __version__
from . import cfg
from .logger import init_logger

class BindProxyConfig(cfg.Config):
    __doc__ = '\n    Configuration parameters\n    '
    default_section = 'bind_proxy'
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
    required_params = ('ldapi_uri', 'providers', 'socket_path')
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
    noproxy_peer_addrs = {
     '/run/slapd/ldapi',
     '127.0.0.1'}
    proxy_peer_addrs = {}
    proxy_peer_nets = (
     ipaddress.ip_network('0.0.0.0/0'),)
    providers = None
    proxy_user_filter = '(oathToken=*)'

    def __init__(self, cfg_filename):
        cfg.Config.__init__(self, cfg_filename)
        self.cache_ttl = {'BIND': self.cache_ttl}


class BindProxyHandler(SlapdSockHandler):
    __doc__ = '\n    Handler class which proxies some simple bind requests to remote server\n    '

    def _check_peername(self, peer):
        peer_type, peer_addr = peer.lower().rsplit(':')[0].split('=')
        if peer_addr in self.server.cfg.noproxy_peer_addrs:
            self._log(logging.DEBUG, 'Peer %r explicitly excluded => no OTP check', peer_addr)
            return False
        if peer_addr in self.server.cfg.proxy_peer_addrs:
            self._log(logging.DEBUG, 'Peer %r explicitly included => proxy OTP check', peer_addr)
            return True
        if not peer_type == 'ip':
            self._log(logging.DEBUG, 'Peer %r not an IP address => no OTP check', peer_addr)
            return False
        peer_ip_address = ipaddress.ip_address(peer_addr)
        for peer_net in self.server.cfg.proxy_peer_nets:
            if peer_ip_address in peer_net:
                self._log(logging.DEBUG, 'Peer %r in included net %r => proxy OTP check', peer_ip_address, peer_net)
                return True
            self._log(logging.DEBUG, 'Peer %r not included => no OTP check', peer_addr)
            return False

    def _shuffle_providers(self, request):
        ldap_uris = collections.deque(self.server.providers)
        ldap_uris.rotate(hash(request.dn.encode('utf-8')) % len(self.server.providers))
        return ldap_uris

    def _check_user_filter(self, request):
        """
        Additional check whether bind request has to be sent to remote LDAP
        server by searching the bind-DN's entry with a filter
        """
        if self.server.cfg.proxy_user_filter is None:
            return
        try:
            try:
                local_ldap_conn = self.server.get_ldapi_conn()
                ldap_result = local_ldap_conn.search_s((request.dn),
                  (ldap0.SCOPE_BASE),
                  (self.server.cfg.proxy_user_filter),
                  attrlist=[
                 '1.1'])
            except ldap0.SERVER_DOWN as ldap_error:
                try:
                    self.server.disable_ldapi_conn()
                    raise ldap_error
                finally:
                    ldap_error = None
                    del ldap_error

        except LDAPError as ldap_error:
            try:
                raise SlapdSockHandlerError(ldap_error,
                  log_level=(logging.WARN),
                  response=(InvalidCredentialsResponse(request.msgid)),
                  log_vars=(self.server._log_vars))
            finally:
                ldap_error = None
                del ldap_error

        else:
            if not ldap_result:
                raise SlapdSockHandlerError((Exception('No result reading %r with filter %r' % (
                 request.dn,
                 self.server.cfg.proxy_user_filter))),
                  log_level=(logging.INFO),
                  response='CONTINUE\n',
                  log_vars=(self.server._log_vars))

    def do_bind(self, request):
        """
        This method first checks whether the BIND request must be sent
        to the upstream replica
        """
        if not self._check_peername(request.peername):
            self._log(logging.DEBUG, 'Peer %r not in %r and %r => let slapd continue', request.peername, self.server.cfg.proxy_peer_addrs, self.server.cfg.proxy_peer_nets)
            return 'CONTINUE\n'
        self._check_user_filter(request)
        providers = self._shuffle_providers(request)
        self._log(logging.DEBUG, 'providers = %r', providers)
        try:
            try:
                while providers:
                    remote_ldap_uri = providers.popleft()
                    self._log(logging.DEBUG, 'Sending request to %r', remote_ldap_uri)
                    try:
                        remote_ldap_conn = LDAPObject(remote_ldap_uri,
                          trace_level=0)
                        remote_ldap_conn.set_tls_options(cacert_filename=(self.server.cfg.cacert_file))
                        remote_ldap_conn.simple_bind_s((request.dn),
                          (request.cred),
                          req_ctrls=[
                         SessionTrackingControl(request.peername, socket.getfqdn(), SESSION_TRACKING_FORMAT_OID_USERNAME, request.dn)])
                    except ldap0.SERVER_DOWN as ldap_error:
                        try:
                            self._log(logging.WARN, 'Connecting to %r failed: %s => try next', remote_ldap_uri, ldap_error)
                            if not providers:
                                raise
                        finally:
                            ldap_error = None
                            del ldap_error

                    break

            except ldap0.SERVER_DOWN as ldap_error:
                try:
                    self._log(logging.ERROR, 'Could not connect to any provider')
                    result_code = RESULT_CODE['unavailable']
                    info = 'OATH providers unavailable'
                finally:
                    ldap_error = None
                    del ldap_error

            except LDAPError as ldap_error:
                try:
                    try:
                        result_code = RESULT_CODE[type(ldap_error)]
                    except KeyError:
                        result_code = RESULT_CODE['other']
                    else:
                        try:
                            info = ldap_error.args[0]['info'].decode('utf-8')
                        except (AttributeError, KeyError, TypeError):
                            info = None
                        else:
                            self._log(logging.ERROR, 'LDAPError from %s: %s => return %s %r', remote_ldap_uri, ldap_error, ldap_error, result_code)
                finally:
                    ldap_error = None
                    del ldap_error

            else:
                result_code = 'success'
                info = None
                self._log(logging.INFO, 'Validation ok for %r (from %r) using provider %r => RESULT: %s', request.dn, request.peername, remote_ldap_conn.uri, result_code)
        finally:
            try:
                remote_ldap_conn.unbind_s()
            except Exception:
                pass

        self._log(logging.DEBUG, 'msgid=%s result_code=%s info=%s', request.msgid, result_code, info)
        return RESULTResponse((request.msgid),
          result_code,
          info=info)


class BindProxyServer(SlapdSockServer):
    __doc__ = '\n    This is used to pass in more parameters to the server instance\n    '

    def __init__(self, scfg, logger):
        self.cfg = scfg
        SlapdSockServer.__init__(self,
          (self.cfg.socket_path),
          BindProxyHandler,
          logger,
          (self.cfg.avg_count),
          (self.cfg.socket_timeout),
          (self.cfg.socket_perms),
          (self.cfg.allowed_uids),
          (self.cfg.allowed_gids),
          bind_and_activate=True,
          monitor_dn=None,
          log_vars=(self.cfg.log_vars))
        self._ldap_conn = None
        self.ldapi_uri = self.cfg.ldapi_uri.connect_uri()
        self.ldap_trace_level = self.cfg.ldap0_trace_level
        self.providers = self.cfg.providers
        self.ldap_authz_id = self.cfg.ldapi_sasl_authzid
        self.ldap_retry_max = self.cfg.ldap_max_retries
        self.ldap_retry_delay = self.cfg.ldap_retry_delay
        self.ldap_cache_ttl = self.cfg.ldap_cache_ttl


def run():
    """
    The main script
    """
    scfg = BindProxyConfig(sys.argv[1])
    my_logger = init_logger(scfg)
    my_logger.info('Starting %s %s (log level %d)', os.path.basename(os.path.abspath(sys.argv[0])), __version__, my_logger.level)
    for name in sorted(dir(scfg)):
        if not name.startswith('__'):
            my_logger.debug('%s.%s = %r', scfg.__class__.__name__, name, getattr(scfg, name))
        my_logger.error("!!! Running in debug mode (log level %d)! Secret data will be logged! Don't do that!!!", my_logger.level)
        try:
            slapd_sock_listener = BindProxyServer(scfg, my_logger)
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