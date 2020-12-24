# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/cli/commands/info.py
# Compiled at: 2017-02-08 04:42:30
"""Calxeda: info.py"""
from cxmanage_api.cli import get_tftp, get_nodes, get_node_strings, run_command, COMPONENTS

def info_command(args):
    """print info from a cluster or host"""
    if args.info_type in (None, 'basic'):
        return info_basic_command(args)
    else:
        if args.info_type == 'ubootenv':
            return info_ubootenv_command(args)
        return


def info_basic_command(args):
    """Print basic info"""
    tftp = get_tftp(args)
    nodes = get_nodes(args, tftp)
    if not args.quiet:
        print 'Getting info...'
    results, errors = run_command(args, nodes, 'get_versions')
    node_strings = get_node_strings(args, results, justify=False)
    for node in nodes:
        if node in results:
            result = results[node]
            components = COMPONENTS
            print '[ Info from %s ]' % node_strings[node]
            print 'Hardware version    : %s' % result.hardware_version
            print 'Firmware version    : %s' % result.firmware_version
            for var, string in components:
                if hasattr(result, var):
                    version = getattr(result, var)
                    print '%s: %s' % (string.ljust(20), version)

            print

    if not args.quiet and errors:
        print 'Some errors occured during the command.\n'
    return len(errors) > 0


def info_ubootenv_command(args):
    """Print uboot info"""
    tftp = get_tftp(args)
    nodes = get_nodes(args, tftp)
    if not args.quiet:
        print 'Getting u-boot environment...'
    results, errors = run_command(args, nodes, 'get_ubootenv')
    node_strings = get_node_strings(args, results, justify=False)
    for node in nodes:
        if node in results:
            ubootenv = results[node]
            print '[ U-Boot Environment from %s ]' % node_strings[node]
            for variable in ubootenv.variables:
                print '%s=%s' % (variable, ubootenv.variables[variable])

            print

    if not args.quiet and errors:
        print 'Some errors occured during the command.\n'
    return len(errors) > 0