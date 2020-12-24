# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acoddington/Documents/Projects/jirafs/jirafs/commands/build.py
# Compiled at: 2020-01-04 20:13:43
# Size of source mod 2**32: 901 bytes
import json
from jirafs.plugin import CommandPlugin, CommandResult

class Command(CommandPlugin):
    __doc__ = ' Commit local changes for later submission to JIRA '
    MIN_VERSION = '2.0.0'
    MAX_VERSION = '3.0.0'

    def main(self, args, folder, **kwargs):
        return folder.process_plugin_builds()

    def cmd(self, *args, **kwargs):
        data = (self.main)(*args, **kwargs)
        result = CommandResult()
        for key, value in data.items():
            result = result.add_line('Ran build plugin {plugin}', plugin=key)
            if not value:
                continue
            if not isinstance(value, str):
                value = json.dumps(value, indent=4, sort_keys=True)
            for line in value.split('\n'):
                if not line.strip():
                    continue
                result = result.add_line('\t{line}', line=line)

        return result