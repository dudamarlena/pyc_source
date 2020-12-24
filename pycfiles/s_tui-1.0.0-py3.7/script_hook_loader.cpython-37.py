# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/s_tui/sources/script_hook_loader.py
# Compiled at: 2019-12-27 09:31:39
# Size of source mod 2**32: 1611 bytes
import os
from s_tui.sources.hook_script import ScriptHook

class ScriptHookLoader:
    __doc__ = '\n    Loads shell scripts from a directory into ScriptHooks for a given Source\n    '

    def __init__(self, dir_path):
        self.scripts_dir_path = os.path.join(dir_path, 'hooks.d')

    def load_script(self, source_name, timeoutMilliseconds=0):
        """
        Return ScriptHook for source_name Source and with a ready timeout
        of timeoutMilliseconds
        """
        script_path = os.path.join(self.scripts_dir_path, self._source_to_script_name(source_name))
        if os.path.isfile(script_path):
            return ScriptHook(script_path, timeoutMilliseconds)

    def _source_to_script_name(self, source_name):
        return source_name.lower() + '.sh'