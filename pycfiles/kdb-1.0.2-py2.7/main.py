# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kdb/main.py
# Compiled at: 2014-04-26 09:00:59
"""Main

Main entry point responsible for configuring and starting the application.
"""
import sys
from os.path import basename
from procname import setprocname
from circuits.app import Daemon
from circuits import Debugger, Manager, Worker
from .core import Core
from .config import Config

def main():
    setprocname(basename(sys.argv[0]))
    config = Config()
    manager = Manager()
    Worker(channel='workerthreads').register(manager)
    Worker(channel='workerprocesses').register(manager)
    if config.get('debug'):
        Debugger(events=config.get('verbose'), file=config.get('errorlog')).register(manager)
    if config.get('daemon'):
        manager += Daemon(config.get('pidfile'))
    Core(config).register(manager)
    manager.run()


if __name__ == '__main__':
    main()