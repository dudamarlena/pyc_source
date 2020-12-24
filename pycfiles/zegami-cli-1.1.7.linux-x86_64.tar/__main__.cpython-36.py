# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/zeg/__main__.py
# Compiled at: 2020-03-19 11:59:34
# Size of source mod 2**32: 4612 bytes
"""A command line interface for managing Zegami."""
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from textwrap import dedent
import pkg_resources
from . import auth, collections, datasets, http, imagesets, log

def main():
    """Zegami command line interface."""
    version = pkg_resources.require('zegami-cli')[0].version
    description = dedent("\n         ____                      _\n        /_  / ___ ___ ____ ___ _  (_)\n         / /_/ -_) _ `/ _ `/  ' \\/ /\n        /___/\\__/\\_, /\\_,_/_/_/_/_/\n                /___/  v{}\n\n        Visual data exploration.\n\n    A command line interface for managing Zegami.\n    ".format(version))
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
      description=description)
    parser.add_argument('--version',
      action='version',
      version=('%(prog)s {}'.format(version)))
    option_mapper = {'delete':{'help':'Delete a resource', 
      'resources':{'collections':collections.delete, 
       'dataset':datasets.delete, 
       'imageset':imagesets.delete}}, 
     'create':{'help':'Create a resource', 
      'resources':{'collections': collections.create}}, 
     'get':{'help':'Get a resource', 
      'resources':{'collections':collections.get, 
       'dataset':datasets.get, 
       'imageset':imagesets.get}}, 
     'publish':{'help':'Publish a resource', 
      'resources':{'collection': collections.publish}}, 
     'update':{'help':'Update a resource', 
      'resources':{'collections':collections.update, 
       'dataset':datasets.update, 
       'imageset':imagesets.update}}}
    subparsers = parser.add_subparsers()
    for action in option_mapper:
        action_parser = subparsers.add_parser(action,
          help=(option_mapper[action]['help']))
        action_parser.set_defaults(action=action)
        action_parser.add_argument('resource',
          choices=(option_mapper[action]['resources'].keys()),
          help='The name of the resource type.')
        if action != 'create':
            action_parser.add_argument('id',
              default=None,
              nargs='?',
              help='Resource identifier.')
        action_parser.add_argument('-c',
          '--config',
          help='Path to command configuration yaml.')
        action_parser.add_argument('-p',
          '--project',
          help='The id of the project.')
        _add_standard_args(action_parser)

    login_parser = subparsers.add_parser('login',
      help='Authenticate against the API and store a long lived token')
    login_parser.set_defaults(action='login')
    _add_standard_args(login_parser)
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    logger = log.Logger(args.verbose)
    token = auth.get_token(args)
    session = http.make_session(args.url, token)
    if args.action == 'login':
        auth.login(logger, session, args)
        return
    try:
        option_mapper[args.action]['resources'][args.resource](logger, session, args)
    except Exception as e:
        if args.verbose:
            raise e
        logger.error('Unhandled exception: {}'.format(e))
        sys.exit(1)


def _add_standard_args(parser):
    parser.add_argument('-t',
      '--token',
      default=None,
      help='Authentication token.')
    parser.add_argument('-u',
      '--url',
      default='https://zegami.com',
      help='Zegami server address.')
    parser.add_argument('-v',
      '--verbose',
      action='store_true',
      help='Enable verbose logging.')


if __name__ == '__main__':
    sys.exit(main())