# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/docbook2sla/util.py
# Compiled at: 2008-03-14 13:07:50
__author__ = 'Timo Stollenwerk (timo@zmag.de)'
__license__ = 'GNU General Public License (GPL)'
__revision__ = '$Rev$'
__date__ = '$Date$'
__URL__ = '$URL$'
import sys, tempfile
from subprocess import Popen, PIPE
from logger import LOG
win32 = sys.platform == 'win32'

def newTempfile(suffix=''):
    return tempfile.mktemp(suffix=suffix)


def runcmd(cmd):
    """ Execute a command using the subprocess module """
    if win32:
        cmd = cmd.replace('\\', '/')
        s = Popen(cmd, shell=False)
        s.wait()
        return (0, '')
    else:
        stdin = open('/dev/null')
        stdout = stderr = PIPE
        p = Popen(cmd, shell=True, stdin=stdin, stdout=stdout, stderr=stderr)
        status = p.wait()
        stdout_ = p.stdout.read().strip()
        stderr_ = p.stderr.read().strip()
        if stdout_:
            LOG.info(stdout_)
        if stderr_:
            LOG.info(stderr_)
        return (
         status, stdout_ + stderr_)