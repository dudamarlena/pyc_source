# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acoddington/Documents/Projects/jirafs/jirafs/commands/log.py
# Compiled at: 2019-03-11 23:04:44
import pydoc
from jirafs.plugin import CommandPlugin

class Command(CommandPlugin):
    """ Print the log for this issue """
    MIN_VERSION = '1.15'
    MAX_VERSION = '1.99.99'

    def main(self, folder, **kwargs):
        results = folder.get_log()
        pydoc.pager(results)
        return results