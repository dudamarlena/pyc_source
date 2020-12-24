# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/cli/commands/ipdiscover.py
# Compiled at: 2017-02-08 04:42:30
"""Calxeda: ipdiscover.py"""
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