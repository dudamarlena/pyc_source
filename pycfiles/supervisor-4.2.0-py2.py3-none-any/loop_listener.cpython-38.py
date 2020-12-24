# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/scripts/loop_listener.py
# Compiled at: 2017-07-24 14:57:05
# Size of source mod 2**32: 716 bytes
import os
from supervisor import childutils

def main():
    rpcinterface = childutils.getRPCInterface(os.environ)
    while True:
        headers, payload = childutils.listener.wait()
        if headers['eventname'].startswith('PROCESS_COMMUNICATION'):
            pheaders, pdata = childutils.eventdata(payload)
            pname = '%s:%s' % (pheaders['processname'], pheaders['groupname'])
            rpcinterface.supervisor.sendProcessStdin(pname, 'Got it yo\n')
        childutils.listener.ok()


if __name__ == '__main__':
    main()