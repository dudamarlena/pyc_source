# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tfnz/cli/tflocations.py
# Compiled at: 2018-05-18 20:34:30
# Size of source mod 2**32: 2115 bytes
"""A tiny utility to select from the location keys stored in ~/.20ft/"""
import os.path
from messidge import default_location
from tfnz.location import Location
from tfnz.cli import generic_cli, base_argparse

def main():
    parser = base_argparse('tflocations', location=False)
    subparsers = parser.add_subparsers(title='commands', dest='command')
    p_list = subparsers.add_parser('list', help='list locations with an account')
    p_token = subparsers.add_parser('select', help='select which location to use as default_location')
    p_token.add_argument('location', metavar='location.20ft.nz')
    generic_cli(parser, {'list':list_locations,  'select':select_location}, location=False)


def list_locations(location, args):
    dl = default_location('~/.20ft')
    for loc in Location.all_locations():
        print('%s %s' % (loc, '<== default' if dl == loc else ''))


def select_location(location, args):
    length = len(args.location)
    for loc in Location.all_locations():
        if loc[:length] == args.location:
            with open(os.path.expanduser('~/.20ft/default_location'), 'w') as (f):
                f.write(loc + '\n')
                return

    print('Could not find a location starting with: ' + args.location)
    exit(1)


if __name__ == '__main__':
    main()