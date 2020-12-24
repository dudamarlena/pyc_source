# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/zwsun/workspace/python/corunner/corunner/Config.py
# Compiled at: 2013-11-05 08:51:57
import os

class Config:

    def __init__(self):
        self.listenPort = 9000
        self.reportInterval = 3
        self.nWorker = 3
        self.nodeRoorDir = '/tmp/corunner'
        self.connectTimeout = 3

    def load(self, configFile):
        with open(configFile, 'r') as (f):
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith('#') or len(line) == 0:
                    continue
                s = line.split('=')
                if len(s) != 2:
                    raise ValueError('Bad config item %s' % line)
                if s[0].strip() == 'controller.worker.count':
                    v = int(s[1].strip())
                    if v < 1:
                        raise ValueError('controller.worker.count should be at least 1, while get %d' % v)
                    self.nWorker = v
                elif s[0].strip() == 'executor.report.interval':
                    v = int(s[1].strip())
                    self.reportInterval = v
                elif s[0].strip() == 'net.connect.timeout':
                    v = int(s[1].strip())
                    self.connectTimeout = v
                elif s[0].strip() == 'controller.listen.port':
                    v = int(s[1].strip())
                    if v < 1:
                        raise ValueError('controller.listen.port should be positive, while get %d' % v)
                    self.listenPort = v
                elif s[0].strip() == 'executor.root.default':
                    self.nodeRootDir = s[1].strip()

    def nodeBinRoot(self):
        return os.path.join(self.nodeRootDir, 'bin')

    def nodeOutputRoot(self):
        return os.path.join(self.nodeRootDir, 'output')

    def string(self):
        return '[listenPort=%d, reportInterval=%d, nWorker=%d, nodeRootDir=%s]' % (self.listenPort, self.reportInterval, self.nWorker, self.nodeRootDir)