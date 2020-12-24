# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acoddington/Documents/Projects/jirafs/jirafs/commands/log.py
# Compiled at: 2020-01-13 00:37:20
# Size of source mod 2**32: 306 bytes
import pydoc
from jirafs.plugin import CommandPlugin

class Command(CommandPlugin):
    __doc__ = ' Print the log for this issue '
    MIN_VERSION = '2.0.0'
    MAX_VERSION = '3.0.0'

    def main(self, folder, **kwargs):
        results = folder.get_log()
        pydoc.pager(results)
        return results