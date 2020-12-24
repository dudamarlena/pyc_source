# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zwsun/workspace/python/corunner/corunner/TaskExecutorProxy.py
# Compiled at: 2013-11-05 08:58:37
import os, common.NetUtil as netutil, common.ShellUtil as shellutil

class TaskExecutorProxy:

    def __init__(self, config, targetIP, targetPort=22):
        self.targetIP = targetIP
        self.targetPort = targetPort
        self.config = config

    def run(self, mainProgram, args):
        command = []
        if not netutil.isLocal(self.targetIP):
            command.append('ssh')
            command.append('-o')
            command.append('ConnectTimeout=%d' % self.config.connectTimeout)
            command.append('-p')
            command.append(self.targetPort)
            command.append(self.targetIP)
        command.append('python')
        command.append(os.path.join(self.config.nodeBinRoot(), 'TaskExecutor.py'))
        command.append('--output')
        command.append(self.config.nodeOutputRoot())
        command.append('--reportInterval')
        command.append(str(self.config.reportInterval))
        command.append('--controller')
        command.append('%s:%d' % (netutil.getLocalIP(), self.config.listenPort))
        command.append('--exec')
        command.append(mainProgram)
        for arg in args:
            command.append(arg)

        shellutil.execute(command, nohup=True)