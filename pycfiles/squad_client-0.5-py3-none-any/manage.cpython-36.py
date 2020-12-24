# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chaws/linaro/src/linaro/squad_client/squad_client/manage.py
# Compiled at: 2020-04-16 07:50:41
# Size of source mod 2**32: 1589 bytes
import argparse, logging, os, sys
from squad_client.core.api import SquadApi, ApiException
from squad_client.core.command import SquadClientCommand
from squad_client.commands import *
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(levelname)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

def main():
    parser = argparse.ArgumentParser(prog='./manage.py')
    parser.add_argument('--debug', action='store_true', help='display debug messages')
    parser.add_argument('--squad-host', help='SQUAD host, example: https://qa-reports.linaro.org')
    parser.add_argument('--squad-token', help='SQUAD authentication token')
    subparser = parser.add_subparsers(help='available subcommands', dest='command')
    SquadClientCommand.add_commands(subparser)
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        return -1
    squad_host = args.squad_host or os.getenv('SQUAD_HOST')
    squad_token = args.squad_token or os.getenv('SQUAD_TOKEN')
    if squad_host is None:
        logger.error('Either --squad-host or SQUAD_HOST env variable are required')
        return -1
    try:
        SquadApi.configure(squad_host, token=squad_token)
    except ApiException as e:
        logger.error('Failed to configure squad api: %s' % e)
        return -1

    rc = SquadClientCommand.process(args)
    if rc is False:
        return 1
    else:
        if rc is True:
            return 0
        return -1


if __name__ == '__main__':
    sys.exit(main())