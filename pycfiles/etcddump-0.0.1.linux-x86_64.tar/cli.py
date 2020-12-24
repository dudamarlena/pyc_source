# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/etcddump/cli.py
# Compiled at: 2014-01-21 04:34:11
from . import operations
import argparse

def main(**kw):
    parser = argparse.ArgumentParser(**kw)
    parser.add_argument('--file', default=None, help='File where the dump is located')
    parser.add_argument('--preserve-indexes', dest='preserve_indexes', action='store_true', help='Try to keep the same indexes as before.')
    parser.add_argument('action', help='What to do: dump or restore')
    parser.add_argument('host', default='http://localhost:4001', help='full url of the etcd host to act upon')
    args = parser.parse_args()
    if args.action == 'dump':
        cl = operations.Dumper(url=args.host)
        cl.dump(filename=args.file)
    elif args.action == 'restore':
        cl = operations.Restorer(url=args.host)
        cl.restore(filename=args.file, preserve_indexes=args.preserve_indexes)
    return