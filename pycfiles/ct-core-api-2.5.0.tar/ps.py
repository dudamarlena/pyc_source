# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cantools/scripts/pubsub/ps.py
# Compiled at: 2019-08-05 00:35:42
import os, sys
from base64 import b64encode
from dez.network.websocket import WebSocketDaemon
from cantools import config
from cantools.util import log, set_log
from .user import PubSubUser
from .channel import PubSubChannel

class PubSub(WebSocketDaemon):

    def __init__(self, *args, **kwargs):
        if config.pubsub.log:
            set_log(os.path.join('logs', config.pubsub.log))
        kwargs['b64'] = config.pubsub.b64
        kwargs['isJSON'] = True
        kwargs['report_cb'] = self._log
        kwargs['cb'] = self.connect
        kwargs['certfile'] = config.ssl.pubsubcert or config.ssl.certfile
        kwargs['keyfile'] = config.ssl.pubsubkey or config.ssl.keyfile
        kwargs['cacerts'] = config.ssl.pubsubcacerts or config.ssl.cacerts
        if 'silent' in kwargs:
            self.silent = kwargs['silent']
            del kwargs['silent']
        else:
            self.silent = False
        WebSocketDaemon.__init__(self, *args, **kwargs)
        self.bots = {}
        self.users = {}
        self.admins = {}
        self.channels = {}
        self.loadBots()
        config.admin.update('pw', config.cache('admin password? '))
        self._log('Initialized PubSub Server @ %s:%s' % (self.hostname, self.port), important=True)

    def loadBots(self):
        self._log('Loading Bots: %s' % (config.pubsub.botnames,))
        sys.path.insert(0, 'bots')
        for bname in config.pubsub.botnames:
            self._log('Importing Bot: %s' % (bname,), 2)
            __import__(bname)

    def newUser(self, u):
        if not u.name:
            self._log('user disconnected without registering')
            u.conn.close()
        elif u.name.startswith('__admin__') and u.name.endswith(b64encode(config.admin.pw)):
            self.admins[u.name] = u
            self.snapshot(u)
        else:
            self.users[u.name] = u

    def client(self, name):
        return self.users.get(name) or self.bots.get(name) or self.admins.get(name)

    def snapshot(self, admin):
        admin.write({'action': 'snapshot', 
           'data': {'bots': [ b.data() for b in list(self.bots.values()) ], 'users': [ u.data() for u in list(self.users.values()) ], 'admins': [ a.data() for a in list(self.admins.values()) ], 'channels': [ c.data() for c in list(self.channels.values()) ]}})

    def pm(self, data, user):
        recipient = self.client(data['user'])
        if not recipient:
            return user._error('no such user!')
        recipient.write({'action': 'pm', 
           'data': {'user': user.name, 
                    'message': data['message']}})

    def subscribe(self, channel, user):
        self._check_channel(channel)
        chan = self.channels[channel]
        chan.join(user)
        self._log('SUBSCRIBE: "%s" -> "%s"' % (user.name, channel), 2)
        data = {'channel': channel, 
           'presence': [ u.name for u in chan.users ], 'history': chan.history}
        if config.pubsub.meta:
            data['meta'] = [ u.meta for u in chan.users ]
        user.write({'action': 'channel', 
           'data': data})

    def unsubscribe(self, channel, user):
        if self._check_channel(channel, True) and user in self.channels[channel].users:
            self.channels[channel].leave(user)
            self._log('UNSUBSCRIBE: "%s" -> "%s"' % (user.name, channel), 2)
        else:
            self._log('FAILED UNSUBSCRIBE: "%s" -> "%s"' % (user.name, channel), 2)

    def meta(self, data, user):
        channel = data['channel']
        self._check_channel(channel)
        user.meta = data['meta']
        self.channels[channel].meta({'meta': user.meta, 
           'user': user.name})

    def publish(self, data, user):
        channel = data['channel']
        self._check_channel(channel)
        self.channels[channel].write({'message': data['message'], 
           'user': user.name})

    def _new_channel(self, channel):
        self.channels[channel] = PubSubChannel(channel, self)
        botname = channel.split('_')[0]
        if botname in config.pubsub.bots:
            self._log("Generating Bot '%s' for channel '%s'" % (botname, channel), 2)
            config.pubsub.bots[botname](self, self.channels[channel])

    def _check_channel(self, channel, justBool=False):
        condition = channel in self.channels
        if not condition and not justBool:
            self._new_channel(channel)
        return condition

    def _log(self, data, level=0, important=False):
        if not self.silent:
            log(data, level=level, important=important)

    def connect(self, conn):
        PubSubUser(conn, self, self._log)