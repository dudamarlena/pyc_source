# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/client/subp.py
# Compiled at: 2019-05-16 13:41:33
import subprocess, collections
ReturnTuple = collections.namedtuple('ReturnTuple', [
 'return_code', 'stdout', 'stderr'])

def subp(cmd):
    """
    Run a command as a subprocess.
    Return a triple of return code, standard out, standard err.
    """
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    return ReturnTuple(proc.returncode, stdout=out, stderr=err)