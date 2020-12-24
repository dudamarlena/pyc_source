# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\core\execution\daskexecutor.py
# Compiled at: 2018-07-06 18:13:02
# Size of source mod 2**32: 1047 bytes
from dask.diagnostics import Profiler, ResourceProfiler, CacheProfiler
from dask.diagnostics import visualize
from xicam.core import msg
from appdirs import user_config_dir
import distributed

class DaskExecutor(object):

    def __init__(self):
        super(DaskExecutor, self).__init__()
        self.client = None

    def execute(self, wf, client=None):
        if not wf.processes:
            return {}
        else:
            if client is None:
                if self.client is None:
                    self.client = distributed.Client()
                client = self.client
            dsk = wf.convertGraph()
            result = client.get(dsk[0], dsk[1])
            msg.logMessage('result:', result, level=(msg.DEBUG))
            wf.lastresult = result
            return result