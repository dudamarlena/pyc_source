# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/cli/commands/mc.py
# Compiled at: 2017-02-08 04:42:30
"""Calxeda: mc.py"""
from cxmanage_api.cli import get_tftp, get_nodes, run_command

def mcreset_command(args):
    """reset the management controllers of a cluster or host"""
    tftp = get_tftp(args)
    nodes = get_nodes(args, tftp)
    if not args.quiet:
        print 'Sending MC reset command...'
    _, errors = run_command(args, nodes, 'mc_reset')
    if not args.quiet and not errors:
        print 'Command completed successfully.\n'
    return len(errors) > 0