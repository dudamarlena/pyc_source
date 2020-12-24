# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymysqlbatchimport/__main__.py
# Compiled at: 2018-06-13 23:34:05
# Size of source mod 2**32: 743 bytes
import argparse
from .run import App

def run(args):
    App.run(args.config)


def prepare(args):
    App.prepare()


arg_parser = argparse.ArgumentParser(description='A MySQL csv import tool')
sub_parsers = arg_parser.add_subparsers(help='sub-command help')
run_parser = sub_parsers.add_parser('run', help='run help')
run_parser.set_defaults(func=run)
run_parser.add_argument('-c', '--config', default=(App.DEFAULT_CONFIG_FILE),
  help='Configuration file')
prepare_parser = sub_parsers.add_parser('prepare', help='prepare help')
prepare_parser.set_defaults(func=prepare)
args = arg_parser.parse_args()
if 'func' in args:
    args.func(args)
else:
    arg_parser.parse_args(['--help'])