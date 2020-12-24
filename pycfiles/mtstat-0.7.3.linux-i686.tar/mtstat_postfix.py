# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/mtstat/plugins/mtstat_postfix.py
# Compiled at: 2006-12-12 18:59:17
import glob

class mtstat_postfix(mtstat):

    def __init__(self):
        self.name = 'postfix'
        self.format = ('d', 4, 100)
        self.vars = ('incoming', 'active', 'deferred', 'bounce', 'defer')
        self.nick = ('inco', 'actv', 'dfrd', 'bnce', 'defr')
        self.init(self.vars, 1)

    def check(self):
        if not os.access('/var/spool/postfix/active', os.R_OK):
            raise Exception, 'Module cannot access postfix queues'
        return True

    def extract(self):
        global glob
        for item in self.vars:
            self.val[item] = len(glob.glob('/var/spool/postfix/' + item + '/*/*'))