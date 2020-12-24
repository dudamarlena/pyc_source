# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/inqbus/ocf/agents/test/dummy_daemon.py
# Compiled at: 2011-11-29 14:20:24
"""
Simple implementation of a unix daemon process.
For testign purposes only.
"""
import daemon, sys
from lockfile.pidlockfile import PIDLockFile
from time import sleep

def main():
    if len(sys.argv) == 2:
        pid_file_path = sys.argv[1]
    else:
        pid_file_path = '/tmp/dummy_daemon.pid'
    pidfile = PIDLockFile(pid_file_path)
    context = daemon.DaemonContext(pidfile=pidfile)
    with context:
        while True:
            sleep(1)


if __name__ == '__main__':
    main()