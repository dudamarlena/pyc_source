# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/cli/commands/ipdiscover.py
# Compiled at: 2017-02-08 04:42:30
__doc__ = 'Calxeda: ipdiscover.py'
from cxmanage_api.cli import get_tftp, get_nodes, get_node_strings, run_command

def ipdiscover_command(args):
    """discover server IP addresses"""
    tftp = get_tftp(args)
    nodes = get_nodes(args, tftp)
    if not args.quiet:
        print 'Getting server-side IP addresses...'
    results, errors = run_command(args, nodes, 'get_server_ip', args.interface, args.ipv6, args.aggressive)
    if results:
        node_strings = get_node_strings(args, results, justify=True)
        print 'IP addresses (ECME, Server)'
        for node in nodes:
            if node in results:
                print '%s: %s' % (node_strings[node], results[node])

        print
    if not args.quiet and errors:
        print 'Some errors occurred during the command.'
    return len(errors) > 0