# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/asyncluster/ndm/worker.py
# Compiled at: 2008-02-20 20:10:08
"""
The main module for worker clients, running as daemons.
"""
import os, sys
CONFIG_PATH = '/etc/asyncluster.conf'

class Manager(object):
    """
    I manage a child worker client.

    @ivar config: A L{configobj} config object loaded from the config file.
    
    """
    __module__ = __name__

    def __init__(self):
        from twisted.internet import reactor
        import configobj, client
        self.config = configobj.ConfigObj(CONFIG_PATH)
        self.client = client.Client(self)
        reactor.callWhenRunning(self.client.connect)
        reactor.run()


def run():
    """
    Runs a child worker L{Manager} in a process forked into the background.
    """
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        sys.exit(1)

    os.chdir('.')
    os.umask(0)
    os.setsid()
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        sys.exit(1)

    si = file('/dev/null', 'r')
    os.dup2(si.fileno(), sys.stdin.fileno())
    so = file('/dev/null', 'a+')
    os.dup2(so.fileno(), sys.stdout.fileno())
    se = file('/dev/null', 'a+', 0)
    os.dup2(se.fileno(), sys.stderr.fileno())
    Manager()