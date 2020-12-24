# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\supervisor\scripts\loop_listener.py
# Compiled at: 2015-07-18 10:13:56
import os
from supervisor import childutils

def main():
    rpcinterface = childutils.getRPCInterface(os.environ)
    while 1:
        headers, payload = childutils.listener.wait()
        if headers['eventname'].startswith('PROCESS_COMMUNICATION'):
            pheaders, pdata = childutils.eventdata(payload)
            pname = '%s:%s' % (pheaders['processname'], pheaders['groupname'])
            rpcinterface.supervisor.sendProcessStdin(pname, 'Got it yo\n')
        childutils.listener.ok()


if __name__ == '__main__':
    main()