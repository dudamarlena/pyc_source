# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dust/services/dustmail/dustmailHandler.py
# Compiled at: 2010-06-01 14:16:01
import os, time
from dust.util.ymap import YamlMap
from dust.services.dustmail.dustmailbackClient import DustmailbackClient

class DustmailHandler:

    def __init__(self, router):
        print('new DustmailHandler')
        self.dustmailback = DustmailbackClient(router)
        self.maildir = 'spool'

    def sendMessage(self, frm, to, message):
        print('sendMessage ' + str(frm) + ' ' + str(to) + ' ' + str(message))
        if not os.path.exists(self.maildir + '/' + frm):
            os.mkdir(self.maildir + '/' + to)
        filename = None
        while not filename or os.path.exists(filename):
            filename = self.makeName(frm, to)

        f = open(filename, 'w')
        f.write(message)
        f.close()
        return

    def makeName(self, frm, to):
        timestamp = str(time.time())
        return self.maildir + '/' + to + '/' + frm + '-' + timestamp