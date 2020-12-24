# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cantools/scripts/pubsub/channel.py
# Compiled at: 2019-08-05 00:35:42
from cantools import config

class PubSubChannel(object):

    def __init__(self, name, server):
        self._log = server._log
        self.server = server
        self.name = name
        self.users = set()
        self.history = []
        self._log('NEW CHANNEL: "%s"' % (name,), 1, True)

    def data(self):
        return {'name': self.name, 
           'users': [ u.name for u in self.users ]}

    def _broadcast(self, obj):
        for user in self.users:
            if config.pubsub.echo or user.name != obj['data']['user']:
                user.write(obj)

        for user in list(self.server.admins.values()):
            user.write(obj)

    def meta(self, subobj):
        subobj['channel'] = self.name
        obj = {'action': 'meta', 
           'data': subobj}
        self._broadcast(obj)

    def write(self, subobj):
        subobj['channel'] = self.name
        obj = {'action': 'publish', 
           'data': subobj}
        self._broadcast(obj)
        self.history.append(subobj)
        self.history = self.history[-config.pubsub.history:]

    def leave(self, user):
        if user in self.users:
            self.users.remove(user)
            user.leave(self)
            self._broadcast({'action': 'unsubscribe', 
               'data': {'user': user.name, 
                        'channel': self.name}})

    def join(self, user):
        data = {'user': user.name, 
           'channel': self.name}
        if config.pubsub.meta:
            data['meta'] = user.meta
        self._broadcast({'action': 'subscribe', 
           'data': data})
        self.users.add(user)
        user.join(self)