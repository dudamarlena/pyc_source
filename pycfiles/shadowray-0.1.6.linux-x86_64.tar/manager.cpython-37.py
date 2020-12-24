# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mt/PycharmProjects/Shadowray/venv/lib/python3.7/site-packages/shadowray/core/manager.py
# Compiled at: 2019-06-22 22:22:13
# Size of source mod 2**32: 2304 bytes
from shadowray.subscribe.parser import Parser
from shadowray.core.server import Server
from shadowray.core.execute import Execute
from shadowray.config.v2ray import SERVER_KEY_FROM_ORIGINAL, SERVER_KEY_FROM_SUBSCRIBE
import json

class Manager:

    def __init__(self, subscribe_file_name=None, server_file_name=None, binary=None):
        if subscribe_file_name is not None:
            self._Manager__subscribe = Parser(filename=subscribe_file_name)
        if server_file_name is not None:
            self._Manager__server = Server(filename=server_file_name)
        if binary is not None:
            self._Manager__execute = Execute(binary=binary)

    def add_subscribe(self, name, url):
        self._Manager__subscribe.add(name, url)

    def update_subscribe(self, show_info=False, **kwargs):
        (self._Manager__subscribe.update)(show_info=show_info, **kwargs)
        self._Manager__server.clear(SERVER_KEY_FROM_SUBSCRIBE)
        s = self._Manager__subscribe.get_servers()
        for i in s:
            self._Manager__server.add(protocol=(i['protocol']), config=(i['config']), ps=(i['ps']), key=SERVER_KEY_FROM_SUBSCRIBE, host=(i['host']))

    def delete_subscribe(self, name):
        self._Manager__subscribe.delete(name)

    def show_servers(self):
        servers = self._Manager__server.get_servers()
        count = 0
        for s in servers[SERVER_KEY_FROM_ORIGINAL]:
            count += 1
            print(str(count) + ' ---- ' + s['ps'] + ' ---- ' + s['protocol'])

        for s in servers[SERVER_KEY_FROM_SUBSCRIBE]:
            count += 1
            print(str(count) + ' ---- ' + s['ps'] + ' ---- ' + s['protocol'])

    def proxy(self, index=None, config=None, daemon=False):
        if config is not None:
            self._Manager__execute.exec((json.dumps(config)), daemon=daemon)
        else:
            if index is not None:
                self._Manager__execute.exec((json.dumps(self._Manager__server.get_config(index))), daemon=daemon)

    def save(self):
        self._Manager__server.save()
        self._Manager__subscribe.save()

    def save_servers(self):
        self._Manager__server.save()

    def save_subscribe(self):
        self._Manager__subscribe.save()

    def get_server(self, index):
        return self._Manager__server.get_server(index)

    @property
    def server_number(self):
        return self._Manager__server.original_servers_number + self._Manager__server.subscribe_servers_number