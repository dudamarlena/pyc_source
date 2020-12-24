# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cbrun/Projets/Perso/projets/dev/testlinkconsole/testlinkconsole/libs/iRunnerPlugin.py
# Compiled at: 2014-07-07 11:08:03
from yapsy.IPlugin import IPlugin

class IRunnerPlugin(IPlugin):

    def activate(self):
        super(IRunnerPlugin, self).activate()
        return 'IRunnerPlugin actif'

    def deactivate(self):
        super(IRunnerPlugin, self).deactivate()
        return 'IRunnerPlugin inactif'