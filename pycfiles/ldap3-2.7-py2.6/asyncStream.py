# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\strategy\asyncStream.py
# Compiled at: 2020-02-23 02:04:04
"""
"""
try:
    from queue import Queue
except ImportError:
    from Queue import Queue

from io import StringIO
from os import linesep
from ..protocol.rfc2849 import decode_persistent_search_control
from ..strategy.asynchronous import AsyncStrategy
from ..core.exceptions import LDAPLDIFError
from ..utils.conv import prepare_for_stream
from ..protocol.rfc2849 import persistent_search_response_to_ldif, add_ldif_header

class AsyncStreamStrategy(AsyncStrategy):
    """
    This strategy is asynchronous. It streams responses in a generator as they appear in the self._responses container
    """

    def __init__(self, ldap_connection):
        AsyncStrategy.__init__(self, ldap_connection)
        self.can_stream = True
        self.line_separator = linesep
        self.all_base64 = False
        self.stream = None
        self.order = dict()
        self._header_added = False
        self.persistent_search_message_id = None
        self.streaming = False
        self.callback = None
        if ldap_connection.pool_size:
            self.events = Queue(ldap_connection.pool_size)
        else:
            self.events = Queue()
        del self._requests
        return

    def _start_listen(self):
        AsyncStrategy._start_listen(self)
        if self.streaming:
            if not self.stream or isinstance(self.stream, StringIO) and self.stream.closed:
                self.set_stream(StringIO())

    def _stop_listen(self):
        AsyncStrategy._stop_listen(self)
        if self.streaming:
            self.stream.close()

    def accumulate_stream(self, message_id, change):
        if message_id == self.persistent_search_message_id:
            with self.async_lock:
                self._responses[message_id] = []
            if self.streaming:
                if not self._header_added and self.stream.tell() == 0:
                    header = add_ldif_header(['-'])[0]
                    self.stream.write(prepare_for_stream(header + self.line_separator + self.line_separator))
                ldif_lines = persistent_search_response_to_ldif(change)
                if self.stream and ldif_lines and not self.connection.closed:
                    fragment = self.line_separator.join(ldif_lines)
                    if not self._header_added and self.stream.tell() == 0:
                        self._header_added = True
                        header = add_ldif_header(['-'])[0]
                        self.stream.write(prepare_for_stream(header + self.line_separator + self.line_separator))
                    self.stream.write(prepare_for_stream(fragment + self.line_separator + self.line_separator))
            else:
                notification = decode_persistent_search_control(change)
                if notification:
                    change.update(notification)
                    del change['controls']['2.16.840.1.113730.3.4.7']
                if not self.callback:
                    self.events.put(change)
                else:
                    self.callback(change)

    def get_stream(self):
        if self.streaming:
            return self.stream
        else:
            return

    def set_stream(self, value):
        error = False
        try:
            if not value.writable():
                error = True
        except (ValueError, AttributeError):
            error = True

        if error:
            raise LDAPLDIFError('stream must be writable')
        self.stream = value
        self.streaming = True