# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/revisor/Documents/Snapper/snapper/cli.py
# Compiled at: 2019-09-09 12:20:19
# Size of source mod 2**32: 2627 bytes
import argparse, logging
from pathlib import Path
import yaml, urllib3
from urllib3.exceptions import InsecureRequestWarning
from snapper import app
urllib3.disable_warnings(InsecureRequestWarning)

def build_parser() -> argparse.ArgumentParser:
    conf_parser = argparse.ArgumentParser(add_help=False)
    conf_parser.add_argument('-c', '--config', dest='config', action='store', help='Specify config file',
      metavar='FILE',
      default=(Path(__file__).parent / 'config.yaml'))
    args, remaining_argv = conf_parser.parse_known_args()
    defaults = {}
    if not args.config:
        raise Exception('Config file not specified (use -c/--config)')
    with open(args.config, 'r') as (file):
        defaults.update(yaml.safe_load(file))
    parser = argparse.ArgumentParser(parents=[conf_parser])
    (parser.set_defaults)(**defaults)
    parser.add_argument('-u', '--user-agent', action='store', dest='user_agent',
      type=str,
      help='The user agent used for requests')
    parser.add_argument('-o', '--output', action='store', dest='output_dir',
      type=str,
      help='Directory for output')
    parser.add_argument('-l', '--log_level', action='store', dest='log_level',
      type=str,
      help='Logging facility level')
    parser.add_argument('-t', '--timeout', action='store', dest='timeout',
      type=int,
      help='Number of seconds to try to resolve')
    parser.add_argument('-p', '--port', action='store', dest='port',
      type=int,
      default=(defaults['app']['port']),
      help='Port to run server on')
    parser.add_argument('-H', '--host', action='store', dest='host',
      type=str,
      default=(defaults['app']['host']),
      help='Host to run server on')
    parser.add_argument('-v', action='store_true', dest='verbose', help='Display console output for fetching each host')
    return parser


def main():
    args, remaining_argv = build_parser().parse_known_args()
    logging.getLogger('requests').setLevel(logging.WARNING)
    app.config.update(vars(args))
    app.run(host=(args.host), port=(args.port), debug=True)


if __name__ == '__main__':
    main()