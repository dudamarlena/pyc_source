# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /data2/junwenwang/panwen/tools/cmdQueue/cmdQueue/plugins/sample.py
# Compiled at: 2017-08-29 17:07:58
from cmdQueue.plugin import Plugin

class samplePlugin(Plugin):

    def onQueueInit(self):
        self.cmdq.logger.info('Queue started!')

    def onJobInit(self, job):
        self.cmdq.logger.info('Job initiated: %s' % job)