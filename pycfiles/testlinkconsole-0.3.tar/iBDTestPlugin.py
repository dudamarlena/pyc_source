# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cbrun/Projets/Perso/projets/dev/testlinkconsole/testlinkconsole/libs/iBDTestPlugin.py
# Compiled at: 2014-07-09 07:29:26
from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton

class IBDTestPlugin(IPlugin):

    def __init__(self):
        super(IBDTestPlugin, self).__init__()

    def activate(self):
        super(IBDTestPlugin, self).activate()
        return 'IBDTestPlugin actif'

    def deactivate(self):
        super(IBDTestPlugin, self).deactivate()
        return 'IBDTestPlugin inactif'