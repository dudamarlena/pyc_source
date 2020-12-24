# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pykzee/Plugin.py
# Compiled at: 2018-12-26 06:11:30
# Size of source mod 2**32: 443 bytes


class Plugin:
    __slots__ = ('get', 'subscribe', 'mount', 'addPlugin', 'removePlugin', 'command')

    def __init__(self, get, subscribe, mount, removePlugin, addPlugin, command):
        self.get = get
        self.subscribe = subscribe
        self.mount = mount
        self.addPlugin = addPlugin
        self.removePlugin = removePlugin
        self.command = command