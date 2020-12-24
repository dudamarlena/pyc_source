# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bpiwowar/development/datasets/datasets/__main__.py
# Compiled at: 2016-11-18 05:48:09
# Size of source mod 2**32: 3293 bytes
import argparse, sys, logging
try:
    from argcomplete import autocomplete
except:
    autocomplete = lambda x: None

share_dir = '/Users/bpiwowar/development/datasets/share'
parser = argparse.ArgumentParser(description='datasets manager')
parser.add_argument('--verbose', action='store_true', help='Be verbose')
parser.add_argument('--debug', action='store_true', help='Be even more verbose')
parser.add_argument('--configuration', help='Directory containing the configuration files', default=share_dir)
subparsers = parser.add_subparsers(help='sub-command help', dest='command')
subparsers.add_parser('info', help='Information about ircollections')
subparsers.add_parser('search', help='Search all the registered datasets')
prepare_parser = subparsers.add_parser('prepare', help='Prepare a dataset')
get_parser = subparsers.add_parser('get', help='Prepare a dataset')
for p in [prepare_parser, get_parser]:
    prepare_parser.add_argument('dataset', nargs=1, help='The dataset ID')
    prepare_parser.add_argument('args', nargs='*', help='Arguments for the preparation')

autocomplete(parser)
args = parser.parse_args()
if args.command is None:
    parser.print_help()
    sys.exit()
if args.verbose:
    logging.getLogger().setLevel(logging.INFO)
if args.debug:
    logging.getLogger().setLevel(logging.DEBUG)
import os
from os.path import join
import yaml

def readyaml(path):
    with open(path) as (f):
        return yaml.load(f)


def configpath(args):
    return join(args.configuration, 'config')


def datapath(args):
    return join(args.configuration, 'data')


def command_search(args):
    cpath = configpath(args)
    for root, dirs, files in os.walk(cpath, topdown=False):
        index = join(root, 'index.yaml')
        prefix = os.path.relpath(root, cpath)
        if os.path.exists(index):
            index = readyaml(index)
            if 'files' in index:
                for relpath in index['files']:
                    path = join(root, '%s.yaml' % relpath)
                    data = readyaml(path)
                    if data is not None and 'data' in data:
                        for d in data['data']:
                            if type(d['id']) == list:
                                for _id in d['id']:
                                    print('%s.%s' % (prefix, _id))

                            else:
                                print('%s.%s' % (prefix, d['id']))

                    else:
                        logging.warn('No data defined in %s' % path)


try:
    fname = 'command_%s' % args.command.replace('-', '_')
    f = globals()[fname]
    f(args)
except Exception as e:
    sys.stderr.write('Error while running command %s:\n' % args.command)
    sys.stderr.write(str(e))
    if args.debug:
        import traceback
        sys.stderr.write(traceback.format_exc())