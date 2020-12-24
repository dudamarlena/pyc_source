# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/powercmd/commands_dict.py
# Compiled at: 2019-08-05 13:21:47
# Size of source mod 2**32: 917 bytes
__doc__ = '\nCommand name -> Command object dictionary able to choose most appropriate\ncommand by partial name.\n'
from powercmd.command import Command
from powercmd.exceptions import InvalidInput
import powercmd.match_string as match_string

class CommandsDict(dict):
    """CommandsDict"""

    def choose(self, short_cmd: str, verbose: bool=False) -> Command:
        """Returns a command handler that matches SHORT_CMD."""
        matches = match_string(short_cmd, self, verbose=verbose)
        if not matches:
            raise InvalidInput('no such command: %s' % (short_cmd,))
        if len(matches) > 1:
            raise InvalidInput('ambigious command: %s (possible: %s)' % (
             short_cmd, ' '.join(matches)))
        return self[matches[0]]