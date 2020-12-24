# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/cli/commands/config.py
# Compiled at: 2017-02-08 04:42:30
"""Calxeda: config.py  """
from cxmanage_api.cli import get_tftp, get_nodes, get_node_strings, run_command
from cxmanage_api.ubootenv import validate_boot_args, validate_pxe_interface

def config_reset_command(args):
    """reset to factory default settings"""
    tftp = get_tftp(args)
    nodes = get_nodes(args, tftp, verify_prompt=True)
    if not args.quiet:
        print 'Sending config reset command...'
    _, errors = run_command(args, nodes, 'config_reset')
    if not args.quiet and not errors:
        print 'Command completed successfully.\n'
    return len(errors) > 0


def config_boot_command(args):
    """set A9 boot order"""
    if args.boot_order == ['status']:
        return config_boot_status_command(args)
    validate_boot_args(args.boot_order)
    tftp = get_tftp(args)
    nodes = get_nodes(args, tftp)
    if not args.quiet:
        print 'Setting boot order...'
    _, errors = run_command(args, nodes, 'set_boot_order', args.boot_order)
    if not args.quiet and not errors:
        print 'Command completed successfully.\n'
    return len(errors) > 0


def config_boot_status_command(args):
    """Get boot status command."""
    tftp = get_tftp(args)
    nodes = get_nodes(args, tftp)
    if not args.quiet:
        print 'Getting boot order...'
    results, errors = run_command(args, nodes, 'get_boot_order')
    if results:
        node_strings = get_node_strings(args, results, justify=True)
        print 'Boot order'
        for node in nodes:
            if node in results:
                print '%s: %s' % (node_strings[node], (',').join(results[node]))

        print
    if not args.quiet and errors:
        print 'Some errors occured during the command.\n'
    return len(errors) > 0


def config_pxe_command(args):
    """set the PXE boot interface"""
    if args.interface == 'status':
        return config_pxe_status_command(args)
    validate_pxe_interface(args.interface)
    tftp = get_tftp(args)
    nodes = get_nodes(args, tftp)
    if not args.quiet:
        print 'Setting pxe interface...'
    _, errors = run_command(args, nodes, 'set_pxe_interface', args.interface)
    if not args.quiet and not errors:
        print 'Command completed successfully.\n'
    return len(errors) > 0


def config_pxe_status_command(args):
    """Gets pxe status."""
    tftp = get_tftp(args)
    nodes = get_nodes(args, tftp)
    if not args.quiet:
        print 'Getting pxe interface...'
    results, errors = run_command(args, nodes, 'get_pxe_interface')
    if results:
        node_strings = get_node_strings(args, results, justify=True)
        print 'PXE interface'
        for node in nodes:
            if node in results:
                print '%s: %s' % (node_strings[node], results[node])

        print
    if not args.quiet and errors:
        print 'Some errors occured during the command.\n'
    return len(errors) > 0