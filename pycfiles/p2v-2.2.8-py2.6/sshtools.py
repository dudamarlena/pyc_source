# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p2v/sshtools.py
# Compiled at: 2012-07-09 05:02:32
import os

class Ssh:

    def __init__(self, server):
        self.server = server

    def del_keyfile(self):
        os.popen('ssh-keygen -R %s 2>/dev/null' % self.server, 'r')

    def copy_id(self):
        print '### Copie des clefs : ###\n'
        os.popen('ssh-copy-id %s 2>/dev/null' % self.server, 'r')

    def exec_cmd(self, cmd=''):
        CMD = os.popen("ssh -o 'StrictHostKeyChecking=no' root@%s '%s'" % (self.server, cmd), 'r')
        ret = CMD.readlines()
        return ret