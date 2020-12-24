# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/cli/commands/mc.py
# Compiled at: 2017-02-08 04:42:30
__doc__ = 'Calxeda: mc.py'
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