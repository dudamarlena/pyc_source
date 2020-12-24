# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data2/junwenwang/panwen/tools/cmdQueue/cmdQueue/plugins/sample.py
# Compiled at: 2017-08-29 17:07:58
from cmdQueue.plugin import Plugin

class samplePlugin(Plugin):

    def onQueueInit(self):
        self.cmdq.logger.info('Queue started!')

    def onJobInit(self, job):
        self.cmdq.logger.info('Job initiated: %s' % job)