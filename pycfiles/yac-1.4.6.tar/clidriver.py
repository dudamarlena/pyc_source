# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x0ox/Dropbox/ActiveDev/yac/yac/cli/clidriver.py
# Compiled at: 2018-01-05 13:50:32
import argparse, sys, os, yac.cli.stack, yac.cli.service, yac.cli.params, yac.cli.prefs, yac.cli.container, yac.cli.ssh, yac.cli.registry, yac.cli.task
from yac.cli.primer import show_primer

def main():
    if len(sys.argv) == 1 or sys.argv[1] == '-h':
        show_primer(['primer'])
    elif sys.argv[(len(sys.argv) - 1)] == 'primer':
        show_primer(sys.argv[1:])
    else:
        command = sys.argv[1]
        sys.argv = sys.argv[1:]
        if command == 'stack':
            return yac.cli.stack.main()
        if command == 'service':
            return yac.cli.service.main()
        if command == 'params':
            return yac.cli.params.main()
        if command == 'prefs':
            return yac.cli.prefs.main()
        if command == 'registry':
            return yac.cli.registry.main()
        if command == 'container':
            return yac.cli.container.main()
        if command == 'ssh':
            return yac.cli.ssh.main()
        if command == 'task':
            return yac.cli.task.main()
        return 'command not supported, or not yet implemented'