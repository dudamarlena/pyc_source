# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /slapdsock/handler.py
# Compiled at: 2020-05-13 07:52:48
# Size of source mod 2**32: 13544 bytes
"""
slapdsock.handler - request handler

slapdsock - OpenLDAP back-sock listeners with Python
see https://www.stroeder.com/slapdsock.html

(c) 2015-2019 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import sys, pwd, struct, time, socket, logging, inspect, datetime
from socketserver import BaseRequestHandler
import ldap0.functions
from ldap0.base import encode_entry_dict
import slapdsock.message
from .message import ENTRYResponse, RESULTResponse, InternalErrorResponse, CONTINUE_RESPONSE
__all__ = [
 'SlapdSockHandler',
 'NoopHandler']
SO_PEERCRED_DICT = {'linux': (17, '3i')}

class SlapdSockHandlerError(Exception):
    __doc__ = '\n    Exception class to be raised within handler methods\n    '

    def __init__(self, orig_exc, log_level=None, response=None, log_vars=None):
        Exception.__init__(self)
        self.orig_exc = orig_exc
        self.log_level = log_level
        self.log_args = ()
        self.response = response
        log_vars = log_vars or []
        frame = inspect.currentframe()
        try:
            var_dict = frame.f_back.f_locals
        finally:
            del frame

        self.log_vars = dict([(
         log_var, var_dict[log_var]) for log_var in log_vars if log_var in var_dict])

    def log(self, logger):
        """
        Write exception log message to logger
        """
        if logger.getEffectiveLevel() <= logging.DEBUG:
            for var_name, var_value in self.log_vars.items():
                logger.debug('%s = %r', var_name, var_value)

        if self.log_args:
            (logger.log)(
 self.log_level, *(self.log_args), **{'exc_info': self.log_level >= logging.ERROR})
        logger.log((self.log_level),
          '%r => response %r',
          (self.orig_exc),
          (self.response),
          exc_info=(self.log_level >= logging.ERROR))


class SlapdSockHandler(BaseRequestHandler):
    __doc__ = "\n    Base class for a handler receiving requests from\n    OpenLDAP's back-sock.\n\n    Note that when using this class as base class you have to implement\n    a method for all request types hitting your handler.\n    "
    cache_ttl = {}

    def __init__(self, *args, **kwargs):
        self._logged_vars = set()
        self.now_dt = datetime.datetime.utcnow()
        self.now_str = ldap0.functions.datetime2str(self.now_dt)
        (BaseRequestHandler.__init__)(self, *args, **kwargs)

    def _get_peer_cred(self):
        """
        Currently works only on Linux
        """
        try:
            so_num, struct_fmt = SO_PEERCRED_DICT[sys.platform]
        except KeyError:
            return (None, None, None)
        else:
            peer_creds_struct = self.request.getsockopt(socket.SOL_SOCKET, so_num, struct.calcsize(struct_fmt))
            return struct.unpack(struct_fmt, peer_creds_struct)

    def _check_access(self, uid=None):
        """
        Check whether the POSIX-UID shall be granted access
        """
        if self.peer_uid in self.server._allowed_uids:
            self._log(logging.DEBUG, 'Access granted for peer UID %d', self.peer_uid)
            result = True
        else:
            if self.peer_gid in self.server._allowed_gids:
                self._log(logging.DEBUG, 'Access granted for peer GID %d', self.peer_gid)
                result = True
            else:
                if uid != None:
                    try:
                        peer_pwd = pwd.getpwuid(self.peer_uid)
                    except KeyError:
                        self._log(logging.WARN, 'Username for peer UID %d not found', self.peer_uid)
                        result = False
                    else:
                        self._log(logging.DEBUG, 'peer_pwd.pw_name = %r', peer_pwd.pw_name)
                        result = peer_pwd.pw_name == uid
                else:
                    result = False
        return result

    def _log(self, log_level, *args, **kwargs):
        """
        Wrapper method adding log prefix
        """
        if self.server.logger.getEffectiveLevel() <= logging.DEBUG:
            frame = inspect.currentframe()
            try:
                all_vars = frame.f_back.f_locals
            finally:
                del frame

            for var_name in self.server._log_vars:
                if var_name in all_vars and var_name not in self._logged_vars:
                    self._logged_vars.add(var_name)
                    self._log(logging.DEBUG, '%s = %r', var_name, all_vars[var_name])

        (self.server.logger.log)(
 log_level,
 ' '.join((self.log_prefix, args[0])), *(args[1:]), **kwargs)

    def do_monitor(self, request):
        """
        Return ENTRY response with monitoring data in response
        to MONITOR request
        """
        if not self._check_access():
            error_message = 'Peer %d/%d not authorized to query monitor' % (
             self.peer_uid,
             self.peer_gid)
            self._log(logging.ERROR, error_message)
            return RESULTResponse((request.msgid),
              'insufficientAccessRights',
              info=error_message)
        monitor_entry = self.server.monitor_entry()
        self._log(logging.DEBUG, 'self.server.monitor_dn = %r', self.server.monitor_dn)
        self._log(logging.DEBUG, 'monitor_entry = %r', monitor_entry)
        return ENTRYResponse(request.msgid, self.server.monitor_dn.encode('utf-8'), encode_entry_dict(monitor_entry))

    def handle(self):
        """
        Handle the incoming request
        """
        self.request_timestamp = time.time()
        self.server._req_count += 1
        msgid = None
        self.log_prefix = str(id(self))
        reqtype = '-/-'
        try:
            self.peer_pid, self.peer_uid, self.peer_gid = self._get_peer_cred()
            self._log(logging.DEBUG, '----- incoming request via %r from pid=%s uid=%s gid=%s -----', self.request.getsockname(), self.peer_pid, self.peer_uid, self.peer_gid)
            request_data = self.request.recv(500000)
            self._log(logging.DEBUG, 'request_data = %r', request_data)
            self.server._bytes_received += len(request_data)
            req_lines = request_data.split(b'\n')
            reqtype = req_lines[0].decode('ascii')
            self._log(logging.DEBUG, 'reqtype = %r', reqtype)
            request_class = getattr(slapdsock.message, '%sRequest' % reqtype)
            self._log(logging.DEBUG, 'request_class=%r', request_class)
            sock_req = request_class(req_lines)
            self.server._req_counters[reqtype.lower()] += 1
            self._log(logging.DEBUG, 'sock_req = %r // %r', sock_req, sock_req.__dict__)
            self.log_prefix = sock_req.log_prefix(self.log_prefix)
            msgid = sock_req.msgid
            cache_key = sock_req.cache_key()
            try:
                try:
                    response = self.server.req_cache[reqtype][cache_key]
                except KeyError:
                    self._log(logging.DEBUG, 'Request not cached: cache_key = %r', cache_key)
                    handle_method = getattr(self, 'do_%s' % reqtype.lower())
                    response = handle_method(sock_req)
                    if cache_key:
                        if reqtype in self.server.req_cache:
                            self.server.req_cache[reqtype][cache_key] = response
                            self._log(logging.DEBUG, 'Response stored in cache: cache_key = %r', cache_key)
                else:
                    self._log(logging.DEBUG, 'Response from cache: cache_key = %r', cache_key)
            except SlapdSockHandlerError as handler_exc:
                try:
                    handler_exc.log(self.server.logger)
                    response = handler_exc.response or InternalErrorResponse(msgid)
                finally:
                    handler_exc = None
                    del handler_exc

        except Exception:
            self._log((logging.ERROR),
              'Unhandled exception during processing request:',
              exc_info=True)
            response = InternalErrorResponse(msgid)
        else:
            try:
                if isinstance(response, str):
                    response_str = response.encode('utf-8')
                else:
                    response_str = bytes(response)
                self._log(logging.DEBUG, 'response_str = %r', response_str)
                if response_str:
                    self.request.sendall(response_str)
            except Exception:
                self._log((logging.ERROR),
                  'Unhandled exception while sending response:',
                  exc_info=True)
            else:
                response_delay = time.time() - self.request_timestamp
                self.server.update_monitor_data(len(response_str), response_delay)
                self._log(logging.DEBUG, 'response_delay = %0.3f', response_delay)


class NoopHandler(SlapdSockHandler):
    __doc__ = '\n    This handler simply returns CONTINUE+LF for every sockops request\n    and empty string for sockresps and unbind requests.\n\n    This is handy to be used as safe base class for own custom handler\n    to make sure each back-sock request is always answered in\n    case of misconfigured "overlay sock" section.\n    '

    def do_add(self, request):
        """
        ADD
        """
        _ = (
         self, request)
        return CONTINUE_RESPONSE

    def do_bind(self, request):
        """
        BIND
        """
        _ = (
         self, request)
        return CONTINUE_RESPONSE

    def do_compare(self, request):
        """
        COMPARE
        """
        _ = (
         self, request)
        return CONTINUE_RESPONSE

    def do_delete(self, request):
        """
        DELETE
        """
        _ = (
         self, request)
        return CONTINUE_RESPONSE

    def do_modify(self, request):
        """
        MODIFY
        """
        _ = (
         self, request)
        return CONTINUE_RESPONSE

    def do_modrdn(self, request):
        """
        MODRDN
        """
        _ = (
         self, request)
        return CONTINUE_RESPONSE

    def do_search(self, request):
        """
        SEARCH
        """
        _ = (
         self, request)
        return CONTINUE_RESPONSE

    def do_unbind(self, request):
        """
        UNBIND
        """
        _ = (
         self, request)
        return ''

    def do_result(self, request):
        """
        RESULT
        """
        _ = (
         self, request)
        return ''

    def do_entry(self, request):
        """
        ENTRY
        """
        _ = (
         self, request)
        return ''

    def do_extended(self, request):
        """
        EXTERNAL
        """
        _ = (
         self, request)
        return CONTINUE_RESPONSE