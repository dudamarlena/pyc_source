# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/commands/run.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 507 bytes
"""
Run specified project from file or URL
"""
from ..main import project_flags
from ..project import project_runner
from ..util import signal_handler

def run(args):
    for i in signal_handler.run(args.pid_filename, project_runner.stop):
        project_runner.run(args)


def add_arguments(parser):
    parser.set_defaults(run=run)
    project_flags.add_arguments(parser)
    parser.add_argument('name',
      nargs='*', help='Path project files - can be a URL or file system location')