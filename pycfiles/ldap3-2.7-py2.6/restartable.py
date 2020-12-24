# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\strategy\restartable.py
# Compiled at: 2020-02-23 02:01:40
"""
"""
from time import sleep
import socket
from .. import get_config_parameter
from .sync import SyncStrategy
from ..core.exceptions import LDAPSocketOpenError, LDAPOperationResult, LDAPMaximumRetriesError
from ..utils.log import log, log_enabled, ERROR, BASIC

class RestartableStrategy(SyncStrategy):

    def __init__(self, ldap_connection):
        SyncStrategy.__init__(self, ldap_connection)
        self.sync = True
        self.no_real_dsa = False
        self.pooled = False
        self.can_stream = False
        self.restartable_sleep_time = get_config_parameter('RESTARTABLE_SLEEPTIME')
        self.restartable_tries = get_config_parameter('RESTARTABLE_TRIES')
        self._restarting = False
        self._last_bind_controls = None
        self._current_message_type = None
        self._current_request = None
        self._current_controls = None
        self._restart_tls = None
        self.exception_history = []
        return

    def open(self, reset_usage=False, read_server_info=True):
        SyncStrategy.open(self, reset_usage, read_server_info)

    def _open_socket(self, address, use_ssl=False, unix_socket=False):
        """
        Try to open and connect a socket to a Server
        raise LDAPExceptionError if unable to open or connect socket
        if connection is restartable tries for the number of restarting requested or forever
        """
        try:
            SyncStrategy._open_socket(self, address, use_ssl, unix_socket)
            self._reset_exception_history()
            return
        except Exception, e:
            if log_enabled(ERROR):
                log(ERROR, '<%s> while restarting <%s>', e, self.connection)
                self._add_exception_to_history(type(e)(str(e)))

        if not self._restarting:
            self._restarting = True
            counter = self.restartable_tries
            while counter > 0:
                if log_enabled(BASIC):
                    log(BASIC, 'try #%d to open Restartable connection <%s>', self.restartable_tries - counter, self.connection)
                sleep(self.restartable_sleep_time)
                if not self.connection.closed:
                    try:
                        self.connection.unbind()
                    except (socket.error, LDAPSocketOpenError):
                        pass
                    except Exception, e:
                        if log_enabled(ERROR):
                            log(ERROR, '<%s> while restarting <%s>', e, self.connection)
                        self._add_exception_to_history(type(e)(str(e)))

                try:
                    if self.connection.server_pool:
                        new_server = self.connection.server_pool.get_server(self.connection)
                        if self.connection.server != new_server:
                            self.connection.server = new_server
                            if self.connection.usage:
                                self.connection._usage.servers_from_pool += 1
                    SyncStrategy._open_socket(self, address, use_ssl, unix_socket)
                    if self.connection.usage:
                        self.connection._usage.restartable_successes += 1
                    self.connection.closed = False
                    self._restarting = False
                    self._reset_exception_history()
                    return
                except Exception, e:
                    if log_enabled(ERROR):
                        log(ERROR, '<%s> while restarting <%s>', e, self.connection)
                    self._add_exception_to_history(type(e)(str(e)))
                    if self.connection.usage:
                        self.connection._usage.restartable_failures += 1

                if not isinstance(self.restartable_tries, bool):
                    counter -= 1

            self._restarting = False
            self.connection.last_error = 'restartable connection strategy failed while opening socket'
            if log_enabled(ERROR):
                log(ERROR, '<%s> for <%s>', self.connection.last_error, self.connection)
            raise LDAPMaximumRetriesError(self.connection.last_error, self.exception_history, self.restartable_tries)

    def send(self, message_type, request, controls=None):
        self._current_message_type = message_type
        self._current_request = request
        self._current_controls = controls
        if not self._restart_tls:
            self._restart_tls = self.connection.tls_started
        if message_type == 'bindRequest':
            self._last_bind_controls = controls
        try:
            message_id = SyncStrategy.send(self, message_type, request, controls)
            self._reset_exception_history()
            return message_id
        except Exception, e:
            if log_enabled(ERROR):
                log(ERROR, '<%s> while restarting <%s>', e, self.connection)
            self._add_exception_to_history(type(e)(str(e)))

        if not self._restarting:
            self._restarting = True
            counter = self.restartable_tries
            while counter > 0:
                if log_enabled(BASIC):
                    log(BASIC, 'try #%d to send in Restartable connection <%s>', self.restartable_tries - counter, self.connection)
                sleep(self.restartable_sleep_time)
                if not self.connection.closed:
                    try:
                        self.connection.unbind()
                    except (socket.error, LDAPSocketOpenError):
                        pass
                    except Exception, e:
                        if log_enabled(ERROR):
                            log(ERROR, '<%s> while restarting <%s>', e, self.connection)
                        self._add_exception_to_history(type(e)(str(e)))

                failure = False
                try:
                    self.connection.open(reset_usage=False, read_server_info=False)
                    if self._restart_tls:
                        self.connection.start_tls(read_server_info=False)
                    if message_type != 'bindRequest':
                        self.connection.bind(read_server_info=False, controls=self._last_bind_controls)
                    if not self.connection.server.schema and not self.connection.server.info:
                        self.connection.refresh_server_info()
                    else:
                        self.connection._fire_deferred(read_info=False)
                except Exception, e:
                    if log_enabled(ERROR):
                        log(ERROR, '<%s> while restarting <%s>', e, self.connection)
                    self._add_exception_to_history(type(e)(str(e)))
                    failure = True

                if not failure:
                    try:
                        ret_value = self.connection.send(message_type, request, controls)
                        if self.connection.usage:
                            self.connection._usage.restartable_successes += 1
                        self._restarting = False
                        self._reset_exception_history()
                        return ret_value
                    except Exception, e:
                        if log_enabled(ERROR):
                            log(ERROR, '<%s> while restarting <%s>', e, self.connection)
                        self._add_exception_to_history(type(e)(str(e)))
                        failure = True

                if failure and self.connection.usage:
                    self.connection._usage.restartable_failures += 1
                if not isinstance(self.restartable_tries, bool):
                    counter -= 1

            self._restarting = False
        self.connection.last_error = 'restartable connection failed to send'
        if log_enabled(ERROR):
            log(ERROR, '<%s> for <%s>', self.connection.last_error, self.connection)
        raise LDAPMaximumRetriesError(self.connection.last_error, self.exception_history, self.restartable_tries)

    def post_send_single_response(self, message_id):
        try:
            ret_value = SyncStrategy.post_send_single_response(self, message_id)
            self._reset_exception_history()
            return ret_value
        except Exception, e:
            if log_enabled(ERROR):
                log(ERROR, '<%s> while restarting <%s>', e, self.connection)
            self._add_exception_to_history(type(e)(str(e)))

        try:
            ret_value = SyncStrategy.post_send_single_response(self, self.send(self._current_message_type, self._current_request, self._current_controls))
            self._reset_exception_history()
            return ret_value
        except Exception, e:
            if log_enabled(ERROR):
                log(ERROR, '<%s> while restarting <%s>', e, self.connection)
            self._add_exception_to_history(type(e)(str(e)))
            if not isinstance(e, LDAPOperationResult):
                self.connection.last_error = 'restartable connection strategy failed in post_send_single_response'
            if log_enabled(ERROR):
                log(ERROR, '<%s> for <%s>', self.connection.last_error, self.connection)
            raise

    def post_send_search(self, message_id):
        try:
            ret_value = SyncStrategy.post_send_search(self, message_id)
            self._reset_exception_history()
            return ret_value
        except Exception, e:
            if log_enabled(ERROR):
                log(ERROR, '<%s> while restarting <%s>', e, self.connection)
            self._add_exception_to_history(type(e)(str(e)))

        try:
            ret_value = SyncStrategy.post_send_search(self, self.connection.send(self._current_message_type, self._current_request, self._current_controls))
            self._reset_exception_history()
            return ret_value
        except Exception, e:
            if log_enabled(ERROR):
                log(ERROR, '<%s> while restarting <%s>', e, self.connection)
            self._add_exception_to_history(type(e)(str(e)))
            if not isinstance(e, LDAPOperationResult):
                self.connection.last_error = e.args
            if log_enabled(ERROR):
                log(ERROR, '<%s> for <%s>', self.connection.last_error, self.connection)
            raise e

    def _add_exception_to_history(self, exc):
        if not isinstance(self.restartable_tries, bool):
            if not isinstance(exc, LDAPMaximumRetriesError):
                self.exception_history.append(exc)

    def _reset_exception_history(self):
        if self.exception_history:
            self.exception_history = []

    def get_stream(self):
        raise NotImplementedError

    def set_stream(self, value):
        raise NotImplementedError