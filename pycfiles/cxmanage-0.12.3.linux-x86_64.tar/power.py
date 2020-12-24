# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/cli/commands/power.py
# Compiled at: 2017-02-08 04:42:30
"""Calxeda: power.py """
from cxmanage_api.cli import get_tftp, get_nodes, get_node_strings, run_command

def power_command(args):
    """change the power state of a cluster or host"""
    tftp = get_tftp(args)
    nodes = get_nodes(args, tftp)
    if not args.quiet:
        print 'Sending power %s command...' % args.power_mode
    _, errors = run_command(args, nodes, 'set_power', args.power_mode)
    if not args.quiet and not errors:
        print 'Command completed successfully.\n'
    return len(errors) > 0


def power_status_command(args):
    """Executes the power status command with args."""
    tftp = get_tftp(args)
    nodes = get_nodes(args, tftp)
    if not args.quiet:
        print 'Getting power status...'
    results, errors = run_command(args, nodes, 'get_power')
    if results:
        node_strings = get_node_strings(args, results, justify=True)
        print 'Power status'
        for node in nodes:
            if node in results:
                result = 'on' if results[node] else 'off'
                print '%s: %s' % (node_strings[node], result)

        print
    if not args.quiet and errors:
        print 'Some errors occured during the command.\n'
    return len(errors) > 0


def power_policy_command(args):
    """Executes power policy command with args."""
    tftp = get_tftp(args)
    nodes = get_nodes(args, tftp)
    if not args.quiet:
        print 'Setting power policy to %s...' % args.policy
    _, errors = run_command(args, nodes, 'set_power_policy', args.policy)
    if not args.quiet and not errors:
        print 'Command completed successfully.\n'
    return len(errors) > 0


def power_policy_status_command(args):
    """Executes the power policy status command with args."""
    tftp = get_tftp(args)
    nodes = get_nodes(args, tftp)
    if not args.quiet:
        print 'Getting power policy status...'
    results, errors = run_command(args, nodes, 'get_power_policy')
    if results:
        node_strings = get_node_strings(args, results, justify=True)
        print 'Power policy status'
        for node in nodes:
            if node in results:
                print '%s: %s' % (node_strings[node], results[node])

        print
    if not args.quiet and errors:
        print 'Some errors occured during the command.\n'
    return len(errors) > 0