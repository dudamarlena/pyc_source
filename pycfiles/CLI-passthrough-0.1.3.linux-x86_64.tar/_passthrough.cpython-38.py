# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nemo/miniconda3/envs/cli/lib/python3.8/site-packages/cli_passthrough/_passthrough.py
# Compiled at: 2019-11-05 20:39:15
# Size of source mod 2**32: 1530 bytes
import errno, os, pty, sys
from select import select
from subprocess import Popen
from .utils import echo

def cli_passthrough(cmd=None, interactive=False):
    """Largely found in https://stackoverflow.com/a/31953436"""
    masters, slaves = zip(pty.openpty(), pty.openpty())
    if interactive:
        cmd = [
         '/bin/bash', '-i', '-c'] + cmd.split()
    else:
        cmd = cmd.split()
    with Popen(cmd, stdin=(slaves[0]), stdout=(slaves[0]), stderr=(slaves[1])) as (p):
        for fd in slaves:
            os.close(fd)
            readable = {masters[0]: sys.stdout.buffer, 
             masters[1]: sys.stderr.buffer}
        else:
            while readable:
                for fd in select(readable, [], [])[0]:
                    try:
                        data = os.read(fd, 1024)
                    except OSError as e:
                        try:
                            if e.errno != errno.EIO:
                                raise
                            del readable[fd]
                        finally:
                            e = None
                            del e

                    else:
                        if not data:
                            del readable[fd]
                        else:
                            if fd == masters[0]:
                                echo(data.rstrip())
                            else:
                                echo((data.rstrip()), err=True)
                            readable[fd].flush()

    for fd in masters:
        os.close(fd)
    else:
        return p.returncode