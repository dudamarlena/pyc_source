# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tfnz/cli/tfvolumes.py
# Compiled at: 2018-08-12 21:56:11
# Size of source mod 2**32: 1925 bytes
import sys
from tfnz.cli import generic_cli, base_argparse

def main():
    parser = base_argparse('tfvolumes')
    subparsers = parser.add_subparsers(title='commands', dest='command')
    p_list = subparsers.add_parser('list', help='list available volumes')
    p_create = subparsers.add_parser('create', help='create a volume')
    p_create.add_argument('--sync', action='store_true', help='force synchronous updates')
    p_create.add_argument('tag', nargs='?', help='give the volume a tag')
    p_delete = subparsers.add_parser('destroy', help='destroy a volume')
    p_delete.add_argument('uuid')
    generic_cli(parser, {'list':list_vol,  'create':create_vol,  'destroy':destroy_vol})


def list_vol(location, args):
    for vol in location.all_volumes():
        print(vol.display_name())


def create_vol(location, args):
    vol = location.create_volume(tag=(args.tag), asynchronous=(not args.sync))
    print(vol.display_name())


def destroy_vol(location, args):
    try:
        vol = location.volumes.get((location.user_pk), key=(args.uuid))
        location.destroy_volume(vol)
    except KeyError:
        print("Can't find volume: " + args.uuid)
        exit(1)


if __name__ == '__main__':
    main()