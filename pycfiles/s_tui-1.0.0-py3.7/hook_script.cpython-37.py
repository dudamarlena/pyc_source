# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/s_tui/sources/hook_script.py
# Compiled at: 2019-12-27 09:31:39
# Size of source mod 2**32: 1981 bytes
import os, subprocess
from s_tui.sources.hook import Hook

class ScriptHook:
    __doc__ = '\n    Runs an arbitrary shell script stored in the filesystem when invoked\n    '

    def __init__(self, path, timeout_milliseconds=0):
        self.path = path
        self.hook = self._make_script_hook(path, timeout_milliseconds)

    def is_ready(self):
        return self.hook.is_ready()

    def invoke(self):
        self.hook.invoke()

    def _run_script(self, *args):
        with open(os.devnull, 'w') as (dev_null):
            subprocess.Popen([
             '/bin/sh', args[0][0]],
              stdout=dev_null,
              stderr=dev_null)

    def _make_script_hook(self, path, timeout_milliseconds):
        return Hook(self._run_script, timeout_milliseconds, path)