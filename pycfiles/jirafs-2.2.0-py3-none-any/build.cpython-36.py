# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acoddington/Documents/Projects/jirafs/jirafs/commands/build.py
# Compiled at: 2019-03-11 23:04:44
# Size of source mod 2**32: 1078 bytes
from jirafs.plugin import CommandPlugin, CommandResult

class Command(CommandPlugin):
    __doc__ = ' Commit local changes for later submission to JIRA '
    MIN_VERSION = '1.16'
    MAX_VERSION = '1.99.99'

    def main(self, args, folder, **kwargs):
        return folder.process_plugin_builds()

    def cmd(self, *args, **kwargs):
        data = (self.main)(*args, **kwargs)
        result = CommandResult()
        for key, value in data.items():
            result = result.add_line('Ran build plugin {plugin}',
              plugin=key)
            if not value:
                pass
            else:
                if not isinstance(value, basestring):
                    value = json.dumps(value,
                      indent=4,
                      sort_keys=True)
                for line in value.split('\n'):
                    if not line.strip():
                        pass
                    else:
                        result = result.add_line('\t{line}',
                          line=line)

        return result