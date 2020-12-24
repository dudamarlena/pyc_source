# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgp/pinentry/gpg_agent.py
# Compiled at: 2015-08-31 08:17:33
import os, socket
from urllib.parse import quote
from urllib.parse import unquote

class GPGAgentPinentry(object):

    def __init__(self, name=None, socket_path=None):
        if name is None:
            name = __name__
        if socket_path is None:
            socket_path = os.getenv('GPG_AGENT_INFO', ':::').split(':', 1)[0]
        self.socket_path = socket_path
        self._sock = None
        return

    def connect(self):
        self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._sock.connect(self.socket_path)
        self.get_response()

    def disconnect(self):
        self._sock.close()

    def send(self, data):
        if isinstance(data, str):
            data = data.encode('latin-1')
        self._sock.send(data + b'\n')

    def get_response(self):
        buf = b''
        lines = []
        while True:
            byte = self._sock.recv(1)
            if byte == b'\n':
                lines.append(buf)
                if buf[:2] == b'OK':
                    break
                elif buf[:3] == b'ERR':
                    raise ValueError(buf[4:].decode('latin-1'))
                buf = b''
            else:
                buf += byte

        return lines

    def get_passphrase(self, prompt=None, error_message=None, description=None, cache_id=None, use_cache=True, no_ask=False, qualitybar=False, repeat=0):
        self.connect()
        params = '--data'
        if no_ask:
            params += ' --no-ask'
        if qualitybar:
            params += ' --qualitybar'
        if repeat == 1:
            params += ' --repeat'
        else:
            if repeat > 1:
                params += ' --repeat={0}'.format(repeat)
            if cache_id:
                params += ' {0}'.format(quote(cache_id))
            else:
                params += ' X'
            if error_message:
                params += ' {0}'.format(quote(error_message))
            else:
                params += ' X'
            if prompt:
                params += ' {0}'.format(quote(prompt))
            else:
                params += ' X'
            if description:
                params += ' {0}'.format(quote(description))
            else:
                params += ' X'
        self.send('GET_PASSPHRASE {0}'.format(params))
        response = self.get_response()
        self.disconnect()
        return unquote(response[0][2:].decode('latin-1'))

    def clear_passphrase(self, cache_id):
        self.connect()
        self.send('CLEAR_PASSPHRASE {0}'.format(quote(cache_id)))
        self.disconnect()