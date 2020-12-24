# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cbrun/Projets/Perso/projets/dev/testlinkconsole/testlinkconsole/plugins/behave.py
# Compiled at: 2014-07-07 10:43:37
from libs.iRunnerPlugin import IRunnerPlugin

class BehavePlugin(IRunnerPlugin):

    def activate(self):
        super(BehavePlugin, self).activate()
        return 'Behave plugin actif'

    def deactivate(self):
        super(BehavePlugin, self).deactivate()
        return 'Behave plugin inactif'

    def run(self, browser, script):
        print 'Behave run %s with %s' % (script, browser)