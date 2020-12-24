# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/inspector/hwlib/biosdevname.py
# Compiled at: 2018-01-10 00:48:14
# Size of source mod 2**32: 1447 bytes
import shlex, subprocess

def get_name(interface):
    command = 'biosdevname --policy physical -i %s' % interface
    p = subprocess.Popen((shlex.split(command)), stdout=(subprocess.PIPE),
      stderr=(subprocess.PIPE))
    out, err = p.communicate()
    if p.returncode:
        if p.returncode == 2:
            return
        else:
            if p.returncode == 3:
                raise OSError('biosdevname must be run as the root user')
            if p.returncode == 4:
                return
        raise Exception('Problem running biosdevname: %d' % p.returncode)
    return out.strip()