# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/buttersink/btrfslist.py
# Compiled at: 2018-06-26 18:40:50
""" Utility program to list data about btrfs subvolumes.

Gives more information than "btrfs sub list", but doesn't filter or format.

Copyright (c) 2014 Ames Cornish.  All rights reserved.  Licensed under GPLv3.
"""
if True:
    import argparse, logging, pprint, sys, btrfs
theDisplayFormat = '%(message)s'
theDebugDisplayFormat = '%(levelname)7s:%(filename)s[%(lineno)d] %(funcName)s(): %(message)s'
logging.basicConfig(format=theDebugDisplayFormat, level='INFO')
logger = logging.getLogger(__name__)
command = argparse.ArgumentParser(description='List data about btrfs subvolumes.', epilog='\n\nCopyright (c) 2014 Ames Cornish.  All rights reserved.  Licensed under GPLv3.\nSee README.md and LICENSE.txt for more info.\n    ', formatter_class=argparse.RawDescriptionHelpFormatter)
command.add_argument('dir', metavar='<dir>', help='list subvolumes in this directory')

def main():
    """ Main program. """
    args = command.parse_args()
    with btrfs.FileSystem(args.dir) as (mount):
        fInfo = mount.FS_INFO()
        pprint.pprint(fInfo)
        vols = mount.subvolumes
        for vol in vols:
            print vol

    return 0


if __name__ == '__main__':
    sys.exit(main())