# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/linjiao/dv/beim/beim/osutils.py
# Compiled at: 2013-12-08 21:45:16
import shlex, subprocess

def spawn(cmd, cwd=None, env=None, stdin=None, stdout=None, stderr=None):
    """spawn a new process

    cmd: the command to execute in the new process
    cwd: the directory where the command will be executed
    env: the environment dictionary
    stdin, stdout, stderr:

    return: new process
    """
    args = shlex.split(cmd)
    p = subprocess.Popen(args, cwd=cwd, env=env, stdin=stdin, stdout=stdout, stderr=stderr)
    return p


def execute(cmd, input=None, cwd=None, env=None, dry_run=False):
    """execute a command and return the returncode, stdout data, and stderr data
    """
    print '* executing %r...' % cmd
    if dry_run:
        return
    p = spawn(cmd, cwd=cwd, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outdata, errdata = p.communicate(input=input)
    retcode = p.wait()
    return (retcode, outdata, errdata)


__id__ = '$Id$'