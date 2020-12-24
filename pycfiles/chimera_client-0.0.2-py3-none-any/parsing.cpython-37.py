# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/lib/chimera_cli/parsing.py
# Compiled at: 2019-12-26 07:34:45
# Size of source mod 2**32: 1227 bytes
import argparse
main_parser = argparse.ArgumentParser(description='Command line interface for chimera',
  usage='Use one of the subcommands')
subparsers = main_parser.add_subparsers(title='command',
  description='Command to send to chimera',
  dest='command',
  required=False)
parent_parser = argparse.ArgumentParser(add_help=False)
parent_parser.add_argument('--namespace',
  required=False,
  type=str,
  help='Namespace specification for chimera cluster')
parent_parser.add_argument('--name',
  required=False,
  type=str,
  help='Name for the deployment that will be sent')
subcommands = parent_parser.add_subparsers(title='subcommand',
  description='Subcommand to use',
  dest='subcommand',
  required=False)
subcommands.add_parser('pipeline')
subcommands.add_parser('channel')
DeployParser = subparsers.add_parser('deploy', parents=[
 parent_parser])
DeleteParser = subparsers.add_parser('delete', parents=[
 parent_parser])
if __name__ == '__main__':
    print(main_parser.parse_args())