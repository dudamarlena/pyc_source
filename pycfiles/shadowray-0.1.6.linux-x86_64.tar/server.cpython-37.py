# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mt/PycharmProjects/Shadowray/venv/lib/python3.7/site-packages/shadowray/core/server.py
# Compiled at: 2019-06-22 22:16:36
# Size of source mod 2**32: 2269 bytes
import json
from shadowray.config.v2ray import SERVER_FILE
from shadowray.config.v2ray import SERVER_KEY_FROM_SUBSCRIBE, SERVER_KEY_FROM_ORIGINAL

class Server:

    def __init__(self, filename=None):
        self._Server__servers = json.loads('{"servers_subscribe": [] ,"servers_original": []}')
        self._Server__filename = SERVER_FILE
        if filename is not None:
            f = open(filename, 'r')
            self._Server__servers = json.load(f)
            f.close()
            self._Server__filename = filename

    def save(self, filename=None):
        if filename is None:
            filename = self._Server__filename
        f = open(filename, 'w')
        f.write(json.dumps(self._Server__servers))
        f.close()

    def add(self, protocol, config, ps, key, host):
        self._Server__servers[key].append({'protocol':protocol, 
         'config':config, 
         'ps':ps, 
         'host':host})

    def get(self, index):
        if self._Server__servers is None:
            return
        return self._Server__servers[index]

    def get_servers(self):
        return self._Server__servers

    @property
    def original_servers_number(self):
        return len(self._Server__servers[SERVER_KEY_FROM_ORIGINAL])

    @property
    def subscribe_servers_number(self):
        return len(self._Server__servers[SERVER_KEY_FROM_SUBSCRIBE])

    @property
    def servers_number(self):
        return self.subscribe_servers_number + self.original_servers_number

    def get_server(self, index):
        if index >= self.servers_number:
            print('Index out of range.')
            return
        if index < self.original_servers_number:
            return self._Server__servers[SERVER_KEY_FROM_ORIGINAL][index]
        return self._Server__servers[SERVER_KEY_FROM_SUBSCRIBE][(index - self.original_servers_number)]

    def get_config(self, index):
        if index >= self.servers_number:
            print('Index out of range.')
            return
        if index < self.original_servers_number:
            return self._Server__servers[SERVER_KEY_FROM_ORIGINAL][index]['config']
        return self._Server__servers[SERVER_KEY_FROM_SUBSCRIBE][(index - self.original_servers_number)]['config']

    def clear(self, key):
        self._Server__servers[key].clear()