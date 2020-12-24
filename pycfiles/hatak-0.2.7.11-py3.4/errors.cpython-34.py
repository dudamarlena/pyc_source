# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hatak/errors.py
# Compiled at: 2014-09-25 03:28:39
# Size of source mod 2**32: 177 bytes


class PluginNotFound(Exception):

    def __init__(self, plugin):
        self.plugin = plugin

    def __repr__(self):
        return 'PluginNotFound: ' + self.plugin.__name__