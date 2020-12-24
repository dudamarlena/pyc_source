# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/sshtunnel.py
# Compiled at: 2007-12-02 16:26:58
from salamoia.h2o.exception import ProtocolError
import os

class SSHTunnel(object):
    __module__ = __name__

    def __init__(self, hostname, localport, remoteport, remotehost='localhost'):
        self.cmd = "ssh %s -C -L %s:%s:%s 'echo ok; cat'" % (hostname, localport, remotehost, remoteport)

    def run(self):
        self.pipe = os.popen3(self.cmd)

    def waitShell(self):
        str = self.pipe[1].readline()
        if str != 'ok\n':
            raise ProtocolError, 'expected ok from ssh'


from salamoia.tests import *
runDocTests()