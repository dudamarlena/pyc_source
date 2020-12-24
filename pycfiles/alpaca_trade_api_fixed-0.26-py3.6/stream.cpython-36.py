# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/alpaca_trade_api_fixed/stream.py
# Compiled at: 2020-02-14 14:55:34
# Size of source mod 2**32: 2342 bytes
import json, re, websocket
from .common import get_base_url, get_credentials
from .entity import Account, Entity

class StreamConn(object):
    __doc__ = 'Deprecated. Use stream2.StreamConn'

    def __init__(self, key_id=None, secret_key=None, base_url=None):
        self._key_id, self._secret_key = get_credentials(key_id, secret_key)
        base_url = re.sub('^http', 'ws', base_url or get_base_url())
        self._endpoint = base_url + '/stream'
        self._handlers = {}
        self._base_url = base_url

    def _connect(self):
        ws = websocket.WebSocket()
        ws.connect(self._endpoint)
        ws.send(json.dumps({'action':'authenticate', 
         'data':{'key_id':self._key_id, 
          'secret_key':self._secret_key}}))
        r = ws.recv()
        msg = json.loads(r)
        self._ws = ws
        self._dispatch('authenticated', msg)
        return ws

    def subscribe(self, streams):
        self._ws.send(json.dumps({'action':'listen', 
         'data':{'streams': streams}}))

    def run(self):
        ws = self._connect()
        try:
            while 1:
                r = ws.recv()
                msg = json.loads(r)
                stream = msg.get('stream')
                if stream is not None:
                    self._dispatch(stream, msg)

        finally:
            ws.close()

    def _cast(self, stream, msg):
        if stream == 'account_updates':
            return Account(msg)
        else:
            return Entity(msg)

    def _dispatch(self, stream, msg):
        for pat, handler in self._handlers.items():
            if pat.match(stream):
                ent = self._cast(stream, msg['data'])
                handler(self, stream, ent)

    def on(self, stream_pat):

        def decorator(func):
            self.register(stream_pat, func)
            return func

        return decorator

    def register(self, stream_pat, func):
        if isinstance(stream_pat, str):
            stream_pat = re.compile(stream_pat)
        self._handlers[stream_pat] = func

    def deregister(self, stream_pat):
        if isinstance(stream_pat, str):
            stream_pat = re.compile(stream_pat)
        del self._handlers[stream_pat]