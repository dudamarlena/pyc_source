# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/cli.py
# Compiled at: 2015-06-21 16:30:01
"""cli program

The main program that is the entry point for the SeedboxManager application.
Provides the ability to configure and start up processing.
"""
import os, tempfile, lockfile
from seedbox import process
from seedbox import service

@lockfile.locked(os.path.join(tempfile.gettempdir(), __package__), timeout=10)
def main():
    """Entry point for seedmgr"""
    service.prepare_service()
    process.start()