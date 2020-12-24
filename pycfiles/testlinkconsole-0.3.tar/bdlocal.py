# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cbrun/Projets/Perso/projets/dev/testlinkconsole/testlinkconsole/plugins/bdlocal.py
# Compiled at: 2014-07-09 07:30:28
from libs.iBDTestPlugin import IBDTestPlugin

class BDLocalPlugin(IBDTestPlugin):

    def __init__(self):
        super(BDLocalPlugin, self).__init__()

    def activate(self):
        super(BDLocalPlugin, self).activate()
        return 'BDLocal plugin actif'

    def deactivate(self):
        super(BDLocalPlugin, self).deactivate()
        return 'BDLocal plugin inactif'

    def run(self, browser, script):
        print 'BDLocal run %s with %s' % (script, browser)

    @staticmethod
    def do_createlocal(self, line):
        print 'Bonjour du plugins'

    @staticmethod
    def help_createlocal(self):
        print ('\n').join([' createlocal plugins',
         'juste un test pour le fun'])