# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /slapdsock/service.py
# Compiled at: 2020-05-13 07:54:41
# Size of source mod 2**32: 8192 bytes
"""
slapdsock.service - The Unix domain listener

slapdsock - OpenLDAP back-sock listeners with Python
see https://www.stroeder.com/slapdsock.html

(c) 2015-2019 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import grp, os, pwd, socket, datetime, inspect, threading
from socketserver import UnixStreamServer, ThreadingMixIn
from collections import defaultdict
import ldap0.functions
from ldap0.lock import LDAPLock
from .ldaphelper import ldap_float_str, LocalLDAPConn
from .cache import CacheDict

class SlapdSockServer(UnixStreamServer, LocalLDAPConn):
    __doc__ = '\n    Base class for a Unix domain socket server implementing\n    an external back-sock listener\n    '
    cache_ttl = -1.0
    allow_reuse_address = True
    monitor_dn = 'cn=sock-monitor'

    def __init__(self, server_address, handler_class, logger, average_count, socket_timeout, socket_permissions, allowed_uids, allowed_gids, bind_and_activate=True, monitor_dn=None, log_vars=None):
        self.req_cache = {}
        for reqtype, cache_ttl in handler_class.cache_ttl.items():
            if cache_ttl > 0:
                self.req_cache[reqtype] = CacheDict(cache_ttl=cache_ttl)
            self.max_req_cache_time = 0.0
            self.logger = logger
            self._socket_timeout = socket_timeout
            self._socket_permissions = socket_permissions
            UnixStreamServer.__init__(self, server_address, handler_class, bind_and_activate)
            LocalLDAPConn.__init__(self, logger)
            self.logger.info('Initializing %s instance listening on %r', self.__class__.__name__, server_address)
            self._average_count = average_count
            self._start_time = datetime.datetime.utcnow()
            self._req_count = 0
            self._req_counters = defaultdict(lambda : 0)
            self._bytes_sent = 0
            self._bytes_received = 0
            self._avg_response_time = 0.0
            self._max_response_time = 0.0
            self._allowed_uids = self._map_names(pwd.getpwnam, pwd.getpwuid, allowed_uids)
            self._allowed_gids = self._map_names(grp.getgrnam, grp.getgrgid, allowed_gids)
            self._monitor_dn = monitor_dn or 'cn=%s' % self.__class__.__name__
            self._log_vars = sorted(log_vars or [])
            self.logger.debug('%s.log_vars=%s', self.__class__.__name__, log_vars)
            self._ldapi_conn = None
            self._ldapi_conn_lock = LDAPLock(desc=('get_ldapi_conn() in %r' % (self.__class__,)))

    def _map_names(self, map_name_func, map_id_func, nameorid_list):
        """
        Map user or group names to their POSIX id
        """
        id_set = set()
        for i in nameorid_list:
            if isinstance(i, int):
                try:
                    map_id_func(i)
                except KeyError:
                    self.logger.warning('Name for allowed ID %d not found', i)
                else:
                    id_set.add(i)
            else:
                if isinstance(i, str):
                    try:
                        mapped_id = map_name_func(i)[2]
                    except KeyError:
                        self.logger.warning('ID for allowed name %r not found', i)
                    else:
                        id_set.add(mapped_id)
                self.logger.debug('%s ID set: %s', map_name_func.__name__, ','.join([str(posix_id) for posix_id in id_set]))
                return id_set

    def update_monitor_data(self, r_len, r_delay):
        """
        Update some monitoring data
        """
        self._bytes_sent += r_len
        self._avg_response_time = ((self._average_count - 1) * self._avg_response_time + r_delay) / self._average_count
        self._max_response_time = max(self._max_response_time, r_delay)

    def monitor_entry(self):
        """
        Returns entry dictionary with monitoring data.

        Override this method to extend the monitor entry with additional
        attributes.
        """
        monitor_entry = {'sockPythonDebug':[
          str(True)], 
         'sockLogLevel':[
          str(self.logger.getEffectiveLevel())], 
         'sockThreadCount':[
          str(threading.activeCount())], 
         'sockStartTime':[
          ldap0.functions.datetime2str(self._start_time)], 
         'sockCurrentTime':[
          ldap0.functions.datetime2str(datetime.datetime.utcnow())], 
         'sockRequestAll':[
          str(self._req_count)], 
         'sockBytesReceived':[
          str(self._bytes_received)], 
         'sockBytesSent':[
          str(self._bytes_sent)], 
         'sockAvgResponseTime':[
          ldap_float_str(self._avg_response_time)], 
         'sockMaxResponseTime':[
          ldap_float_str(self._max_response_time)], 
         'sockLDAPIConnection':[
          repr(self._ldapi_conn)]}
        if self._ldapi_conn:
            monitor_entry['sockLDAPIAuthzID'] = [
             self._ldapi_conn.whoami_s()]
        else:
            monitor_entry['sockLDAPIAuthzID'] = [
             'None']
        for req_type, req_counter in sorted(self._req_counters.items()):
            req_type_str = (
             req_type[0].upper(), req_type[1:].lower())
            monitor_entry['sockRequest%s%sCount' % req_type_str] = [str(req_counter)]
        else:
            for req_type, req_cache in sorted(self.req_cache.items()):
                req_type_str = (
                 req_type[0].upper(), req_type[1:].lower())
                monitor_entry.update({'sockCache%s%sNum' % req_type_str: [str(len(req_cache))], 
                 'sockCache%s%sTTL' % req_type_str: [ldap_float_str(req_cache._cache_ttl)], 
                 'sockCache%s%sMaxHitTime' % req_type_str: [
                                                            ldap_float_str(req_cache.max_cache_hit_time)], 
                 
                 'sockCache%s%sHitCount' % req_type_str: [str(req_cache.cache_hit_count)]})
                if self._req_counters[req_type]:
                    monitor_entry['sockCache%s%sHitRate' % req_type_str] = [
                     ldap_float_str(100 * float(req_cache.cache_hit_count) / float(self._req_counters[req_type]))]
                else:
                    monitor_entry['sockCache%s%sHitRate' % req_type_str] = [
                     ldap_float_str(0.0)]
            else:
                return monitor_entry

    def server_bind(self):
        """Override server_bind to set socket options."""
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(self._socket_timeout)
        try:
            os.unlink(self.server_address)
        except OSError as os_error:
            try:
                if os.path.exists(self.server_address):
                    raise os_error
            finally:
                os_error = None
                del os_error

        else:
            UnixStreamServer.server_bind(self)
            os.chmod(self.server_address, int(self._socket_permissions, 8))


class SlapdSockThreadingServer(ThreadingMixIn, SlapdSockServer):
    __doc__ = '\n    This can be used to run as multi-threaded server\n    '