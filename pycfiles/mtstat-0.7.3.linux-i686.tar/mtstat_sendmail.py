# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/mtstat/plugins/mtstat_sendmail.py
# Compiled at: 2006-12-12 18:59:18
import glob

class mtstat_sendmail(mtstat):

    def __init__(self):
        self.name = 'sendmail'
        self.format = ('d', 4, 100)
        self.vars = ('queue', )
        self.nick = ('queu', )
        self.init(self.vars, 1)

    def check(self):
        if not os.access('/var/spool/mqueue', os.R_OK):
            raise Exception, 'Module cannot access sendmail queue'
        return True

    def extract(self):
        global glob
        self.val['queue'] = len(glob.glob('/var/spool/mqueue/qf*'))