# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/commands/monitor.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 614 bytes
"""
Monitor a control source
"""
import sys
from ..project import importer
from ..util import log

def run(args):
    control = args.control[0]
    try:
        tc = importer.import_symbol(control, 'bibliopixel.control')
    except:
        log.error('Do not understand control "%s"', control)
        raise

    control_object = tc(pre_routing='()')
    control_object.set_project(log.printer)
    control_object.start()
    control_object.wait()


def add_arguments(parser):
    parser.add_argument('control',
      nargs=1, help='Name of a control to monitor')
    parser.set_defaults(run=run)