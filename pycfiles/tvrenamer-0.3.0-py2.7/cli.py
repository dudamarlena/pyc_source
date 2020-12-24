# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.2.1-i686/egg/tvrenamer/cli.py
# Compiled at: 2015-11-08 18:30:19
"""Command-line interface to the TvRenamer APIs"""
import os, tempfile, lockfile
from tvrenamer import manager
from tvrenamer import service

@lockfile.locked(os.path.join(tempfile.gettempdir(), __package__), timeout=10)
def main():
    service.prepare_service()
    manager.run()
    return 0