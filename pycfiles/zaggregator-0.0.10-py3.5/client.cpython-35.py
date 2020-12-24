# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zaggregator/client.py
# Compiled at: 2018-07-20 17:07:06
# Size of source mod 2**32: 1302 bytes
import argparse, sys
from zaggregator import sqlite
from zaggregator.utils import discovery_json, eprint
from zaggregator.config import metrics as checks

def discover():
    """ Returns bundles list in Zabbix autodiscovery JSON format """
    print(discovery_json(sqlite.get_bundle_names()))


def check(opts):
    """ Returns value for specified bundle and check type """
    bname, check = opts
    if check not in checks:
        eprint("\tInvalid check argument: '{}'\n\tSupported options are: '{}'".format(check, "','".join(checks)))
        sys.exit(1)
    print(sqlite.get(bname, check))


def main(*args, **kwargs):
    """ main module """
    parser = argparse.ArgumentParser(description='Zabbix aggregator client.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-discover', action='store_true', help='Discover and print out list of bundles in Zabbix autodiscovery JSON format.')
    group.add_argument('-bundle', nargs=2, metavar=('<bundleName>', '<check>'), help='Bundle name to check stats on. Check can be one of: pcpu, rss, vms, ctxvol, ctxinvol')
    args = parser.parse_args()
    if args.discover:
        discover()
    if args.bundle:
        check(args.bundle)


if __name__ == '__main__':
    main()