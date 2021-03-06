# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/do_exec.py
# Compiled at: 2007-08-13 06:22:59
"""Execute a *nix command  and capture the output."""
import os, re
__version__ = '$Revision: 1.5 $'
_comment = re.compile('\\s*#')

def getall(s):
    """Read a list of lines from a process, after
        dropping junk like comments (beginning with whitespace then '#')
        or blank lines.
        Raises an exception if if the process returns
        a line beginning with 'ERR:'
        The argument s is a string containing the command and its 
        arguments.  S is normally passed to a shell."""
    pipe = os.popen(s, 'r')
    if pipe is None:
        raise RuntimeError, 'Cannot spawn pipe for {%s}' % s
    x = []
    while 1:
        line = pipe.readline()
        if line == '':
            break
        if line.startswith('#'):
            continue
        cs = _comment.search(line)
        if cs is not None:
            line = cs.string[:cs.start()]
        line = line.rstrip()
        if line == '':
            continue
        if line.startswith('ERR:'):
            raise RuntimeError, '%s from {%s}' % (line, s)
        x.append(line.strip())

    sts = pipe.close()
    if sts is None:
        sts = 0
    if sts != 0:
        raise RuntimeError, 'spawned command fails with %d from {%s}' % (sts, s)
    return x


def get(s):
    """Read a single line from a process, after
        dropping junk like comments (#) or blank lines.
        Returns a trouble indication if the process returns
        'ERR:' """
    x = getall(s)
    if len(x) < 1:
        raise RuntimeError, 'no output fron {%s}' % s
    return x[0]