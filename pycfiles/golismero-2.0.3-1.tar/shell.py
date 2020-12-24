# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/lib/core/shell.py
# Compiled at: 2013-12-09 06:41:17
"""
Copyright (c) 2006-2013 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""
import atexit, os, rlcompleter
from lib.core import readlineng as readline
from lib.core.common import Backend
from lib.core.data import logger
from lib.core.data import paths
from lib.core.enums import OS

def saveHistory():
    historyPath = os.path.expanduser(paths.SQLMAP_HISTORY)
    readline.write_history_file(historyPath)


def loadHistory():
    historyPath = os.path.expanduser(paths.SQLMAP_HISTORY)
    if os.path.exists(historyPath):
        try:
            readline.read_history_file(historyPath)
        except IOError as msg:
            warnMsg = "there was a problem loading the history file '%s' (%s)" % (historyPath, msg)
            logger.warn(warnMsg)


class CompleterNG(rlcompleter.Completer):

    def global_matches(self, text):
        """
        Compute matches when text is a simple name.
        Return a list of all names currently defined in self.namespace
        that match.
        """
        matches = []
        n = len(text)
        for ns in (self.namespace,):
            for word in ns:
                if word[:n] == text:
                    matches.append(word)

        return matches


def autoCompletion(sqlShell=False, osShell=False):
    if not readline._readline:
        return
    else:
        if osShell:
            if Backend.isOs(OS.WINDOWS):
                completer = CompleterNG({'copy': None, 
                   'del': None, 'dir': None, 'echo': None, 
                   'md': None, 'mem': None, 'move': None, 
                   'net': None, 'netstat -na': None, 'ver': None, 
                   'xcopy': None, 'whoami': None})
            else:
                completer = CompleterNG({'cp': None, 
                   'rm': None, 'ls': None, 'echo': None, 
                   'mkdir': None, 'free': None, 'mv': None, 
                   'ifconfig': None, 'netstat -natu': None, 'pwd': None, 
                   'uname': None, 'id': None})
            readline.set_completer(completer.complete)
            readline.parse_and_bind('tab: complete')
        loadHistory()
        atexit.register(saveHistory)
        return