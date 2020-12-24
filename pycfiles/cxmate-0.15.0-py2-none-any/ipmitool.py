# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/cli/commands/ipmitool.py
# Compiled at: 2017-02-08 04:42:30
__doc__ = 'Calxeda: ipmitool.py'
from cxmanage_api.cli import get_tftp, get_nodes, get_node_strings, run_command

def ipmitool_command(args):
    """run arbitrary ipmitool command"""
    if args.lanplus:
        ipmitool_args = [
         '-I', 'lanplus'] + args.ipmitool_args
    else:
        ipmitool_args = args.ipmitool_args
    tftp = get_tftp(args)
    nodes = get_nodes(args, tftp)
    if not args.quiet:
        print 'Running IPMItool command...'
    results, errors = run_command(args, nodes, 'ipmitool_command', ipmitool_args)
    node_strings = get_node_strings(args, results, justify=False)
    for node in nodes:
        if node in results and results[node] != '':
            print '[ IPMItool output from %s ]' % node_strings[node]
            print results[node]
            print

    if not args.quiet and errors:
        print 'Some errors occured during the command.\n'
    return len(errors) > 0