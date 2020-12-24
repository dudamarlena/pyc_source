# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/logic/async.py
# Compiled at: 2012-10-12 07:02:39
import os, re
from datetime import datetime
from xml.sax.saxutils import escape, unescape
from tempfile import mkstemp
from coils.core import Command, CoilsException
from coils.foundation import AuditEntry, BLOBManager

class AsyncronousCommand(Command):

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self._callback = params.get('callback', None)
        self._timeout = params.get('timeout', 1000)
        self._raise_error = params.get('raise_error', True)
        return

    def parse_success_response(self, data):
        pass

    def parse_failure_response(self, data):
        pass

    def local_callback(self, uuid, source, target, data):
        if self._callback:
            return self._callback(uuid, source, target, data)
        if 'status' in data:
            if data['status'] == 200:
                self.parse_success_response(data)
            elif self._raise_error:
                if 'text' in data:
                    raise CoilsException(data['text'])
                else:
                    raise CoilsException(('Received failure from "{0}" of "{1}" but no description.').format(source, data['status']))
            else:
                self.parse_failure_response(data)
        else:
            raise CoilsException(('Received response from "{0}" with no status indication.').format(source))
        return True

    def callout(self, target, payload):
        return self._ctx.send(None, target, payload, callback=self.local_callback)

    def wait(self):
        if not self._callback:
            self._ctx.wait(self._timeout)