# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\core\execution\localexecutor.py
# Compiled at: 2018-05-17 15:54:06
# Size of source mod 2**32: 468 bytes
from dask.diagnostics import Profiler, ResourceProfiler, CacheProfiler
from dask.diagnostics import visualize
import dask.threaded
from distributed import LocalCluster
from xicam.core import msg
from appdirs import user_config_dir
from .daskexecutor import DaskExecutor

class LocalExecutor(DaskExecutor):

    def execute(self, wf, client=None):
        if not client:
            client = dask.threaded
        return super(LocalExecutor, self).execute(wf, client)