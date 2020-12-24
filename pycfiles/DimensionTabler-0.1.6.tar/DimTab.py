# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: h:\dev\dimensiontabler\DimensionTabler\DimTab.py
# Compiled at: 2018-03-04 15:14:18
import time
from _libs.DimTabWorker import DimTabWorker
from DimTabConfig import DimTabConfig as Config
import sys, traceback

class DimTab(object):

    def __init__(self, configLst):
        super(DimTab, self).__init__()
        self._workerLst = []
        if type(configLst) is list and all(isinstance(element, Config) for element in configLst):
            for config in configLst:
                self._workerLst.append(DimTabWorker(config))

        else:
            raise Exception("Initialize with list of DimensionTabler.Config's.")

    def _iteration(self):
        for worker in self._workerLst:
            try:
                worker.Work()
            except Exception as ex:
                print '%s: %s' % (worker._config.Name, repr(ex))
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_tb(exc_traceback, file=sys.stdout)

    def MainLoop(self, seconds=1):
        while True:
            self._iteration()
            time.sleep(seconds)