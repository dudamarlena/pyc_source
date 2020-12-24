# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cantools/scripts/pubsub/user.py
# Compiled at: 2019-09-17 18:53:00
from datetime import datetime
from .actor import Actor

class PubSubUser(Actor):
    id = 0

    def __init__(self, conn, server, logger):
        PubSubUser.id += 1
        self.id = PubSubUser.id
        self.conn = conn
        self.server = server
        self._log = logger
        self.channels = set()
        self.conn.set_cb(self._register)
        self._log('NEW CONNECTION (%s)' % (self.id,), 1, True)

    def write(self, data):
        data['data']['datetime'] = str(datetime.utcnow())
        self.conn.write(data)

    def _read(self, obj):
        if obj['action'] == 'close':
            return self.conn.close()
        getattr(self.server, obj['action'])(obj['data'], self)

    def _close(self):
        if self.name in self.server.users:
            del self.server.users[self.name]
        else:
            if self.name in self.server.admins:
                del self.server.admins[self.name]
            for channel in list(self.channels):
                channel.leave(self)

    def _error(self, message):
        self.write({'action': 'error', 
           'data': {'message': message}})

    def _register(self, obj):
        name = obj.get('data')
        if not name:
            self._log('no name provided! assigning index (%s).' % (self.id,))
            name = str(self.id)
        self._log('REGISTER: "%s"' % (name,), 1, True)
        self.name = name
        self.meta = obj.get('meta')
        self.server.newUser(self)
        self.conn.set_cb(self._read)
        self.conn.set_close_cb(self._close)