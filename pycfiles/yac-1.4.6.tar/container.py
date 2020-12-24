# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x0ox/Dropbox/ActiveDev/yac/yac/cli/container.py
# Compiled at: 2017-11-16 20:28:40
import argparse, sys, os, yac.cli.build, yac.cli.push, yac.cli.start
from yac.cli.primer import show_primer

def main():
    if len(sys.argv) == 1 or sys.argv[1] == '-h':
        show_primer(['container', 'primer'])
    else:
        command = sys.argv[1]
        sys.argv = sys.argv[1:]
        if command == 'start':
            return yac.cli.start.main()
        if command == 'build':
            return yac.cli.build.main()
        if command == 'push':
            return yac.cli.push.main()
        print 'Command not supported or known'
        show_primer(['container', 'primer'])