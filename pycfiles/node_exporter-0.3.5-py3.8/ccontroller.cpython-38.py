# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/node_exporter/collector/ccontroller.py
# Compiled at: 2020-01-14 05:18:01
# Size of source mod 2**32: 1424 bytes


class CollectorController:

    def __init__(self, white, black):
        self.white = white
        self.black = black
        self._collectors = {}
        self.initRegister()

    def initRegister(self):
        from node_exporter.collector.diskstats import DiskstatsCollector
        from node_exporter.collector.loadavg import LoadavgCollector
        from node_exporter.collector.filesystem import FilesystemCollector
        from node_exporter.collector.stat import StatCollector
        from node_exporter.collector.meminfo import MeminfoCollector
        from node_exporter.collector.cpu import CpuCollector
        ALLCOLLECTORS = [
         DiskstatsCollector,
         LoadavgCollector,
         FilesystemCollector,
         StatCollector,
         MeminfoCollector,
         CpuCollector]
        print('Enabled collectors:')
        for c in ALLCOLLECTORS:
            self._collectors[c.name] = c()
            self._collectors[c.name].register()
            print('  - {} '.format(c.name))

    def collect(self, names=[]):
        if len(names) == 0:
            for k, v in self._collectors.items():
                v.register()

        for name in names:
            self._collectors[name].register()
        else:
            for name in self._collectors.keys():
                if name not in names:
                    self._collectors[name].unregister()


CController = CollectorController([], [])