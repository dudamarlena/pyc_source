# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/zwsun/workspace/python/corunner/corunner/common/FileDispatcher.py
# Compiled at: 2013-11-05 09:04:39
import os, logging, NetUtil, ShellUtil

class FileDispatcher:

    def __init__(self, targetIP, targetPort=22, connectTimeout=3):
        self.logger = logging.getLogger()
        self.targetIP = targetIP
        self.targetPort = targetPort
        self.connectTimeout = connectTimeout

    def copyTo(self, localPath, remotePath, mkdir=True):
        self.__copy(localPath, remotePath, self.targetIP, self.targetPort, mkdir, True)

    def copyFrom(self, remotePath, localPath, mkdir=True):
        self.__copy(localPath, remotePath, self.targetIP, self.targetPort, mkdir, False)

    def __copy(self, localPath, remotePath, targetIP, targetPort, mkdir, isOut):
        if NetUtil.isLocal(targetIP):
            if isOut:
                if mkdir:
                    ShellUtil.execute(['mkdir', '-p', remotePath])
                ShellUtil.execute(['cp', '-r', localPath, remotePath])
            else:
                if mkdir:
                    ShellUtil.execute(['mkdir', '-p', localPath])
                ShellUtil.execute(['cp', '-r', remotePath, localPath])
            return
        if mkdir:
            if isOut:
                mkdirCommand = [
                 'ssh', '-o', 'ConnectTimeout=%d' % self.connectTimeout, '-p', str(targetPort), targetIP, 'mkdir', '-p', remotePath]
                ShellUtil.execute(mkdirCommand)
            else:
                ShellUtil.execute(['mkdir', '-p', localPath])
        command = [
         'scp', '-o', 'ConnectTimeout=%d' % self.connectTimeout, '-P', str(targetPort)]
        if os.path.isdir(localPath):
            command.append('-r')
        if isOut:
            command.append(localPath)
        command.append('%s:%s' % (targetIP, remotePath))
        if not isOut:
            command.append(localPath)
        ShellUtil.execute(command)