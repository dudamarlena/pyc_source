# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/google/apputils/shellutil.py
# Compiled at: 2015-02-20 20:25:16
"""Utility functions for dealing with command interpreters."""
import os
win32 = os.name == 'nt'

def ShellEscapeList(words):
    """Turn a list of words into a shell-safe string.

  Args:
    words: A list of words, e.g. for a command.

  Returns:
    A string of shell-quoted and space-separated words.
  """
    if win32:
        return (' ').join(words)
    s = ''
    for word in words:
        s += "'" + word.replace("'", '\'"\'"\'') + "' "

    return s[:-1]


def ShellifyStatus(status):
    """Translate from a wait() exit status to a command shell exit status."""
    if not win32:
        if os.WIFEXITED(status):
            status = os.WEXITSTATUS(status)
        else:
            status = 128 + os.WTERMSIG(status)
    return status