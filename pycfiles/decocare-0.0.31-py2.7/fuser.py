# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/decocare/fuser.py
# Compiled at: 2015-12-16 01:43:41
import sys
from subprocess import Popen, PIPE

def in_use(device):
    if 'windows' in sys.platform:
        return False
    pipe = Popen(['fuser', device], stdout=PIPE, stderr=PIPE)
    stdout, stderr = pipe.communicate()
    return stdout is not ''


if __name__ == '__main__':
    from scan import scan
    candidate = (sys.argv[1:2] or [scan()]).pop()
    print in_use(candidate)