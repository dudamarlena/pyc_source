# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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