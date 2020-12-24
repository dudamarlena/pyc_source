# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/swarmy/shell.py
# Compiled at: 2011-09-22 05:10:23
import os, subprocess, sys

def pipe_to_pager(text, command=None):
    """ Pipe text to a pager and wait for the user to exit the pager. """
    if command is None:
        command = os.environ['PAGER'] if 'PAGER' in os.environ else 'more'
    pager = subprocess.Popen(command, stdin=subprocess.PIPE)
    print >> pager.stdin, text,
    pager.stdin = sys.stdin
    pager.wait()
    return