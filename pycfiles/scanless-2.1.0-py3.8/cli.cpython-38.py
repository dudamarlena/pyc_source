# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scanless/cli.py
# Compiled at: 2020-04-13 15:06:27
# Size of source mod 2**32: 3263 bytes
"""scanless.cli"""
import crayons, argparse
from random import choice
from scanless.core import Scanless
SCAN_LIST = '+----------------+--------------------------------------+\n| Scanner Name   | Website                              |\n+----------------|--------------------------------------+\n| hackertarget   | https://hackertarget.com             |\n| ipfingerprints | https://www.ipfingerprints.com       |\n| pingeu         | https://ping.eu                      |\n| spiderip       | https://spiderip.com                 |\n| standingtech   | https://portscanner.standingtech.com |\n| t1shopper      | http://www.t1shopper.com             |\n| viewdns        | https://viewdns.info                 |\n| yougetsignal   | https://www.yougetsignal.com         |\n+----------------+--------------------------------------+'
VERSION = '2.1.0'
sl = Scanless(cli_mode=True)

def get_parser():
    parser = argparse.ArgumentParser(description='scanless, an online port scan scraper.')
    parser.add_argument('-v',
      '--version', action='store_true',
      help='display the current version')
    parser.add_argument('-t',
      '--target', help='ip or domain to scan',
      type=str)
    parser.add_argument('-s',
      '--scanner', default='hackertarget',
      help='scanner to use (default: hackertarget)',
      type=str)
    parser.add_argument('-r',
      '--random', action='store_true',
      help='use a random scanner')
    parser.add_argument('-l',
      '--list', action='store_true',
      help='list scanners')
    parser.add_argument('-a',
      '--all', action='store_true',
      help='use all the scanners')
    parser.add_argument('-d',
      '--debug', action='store_true',
      help='turns cli mode off for debugging, shows network errors')
    return parser


def display(results):
    for line in results.split('\n'):
        if not line:
            continue
        elif 'tcp' in line or 'udp' in line:
            if 'open' in line:
                print(crayons.green(line))
            elif 'closed' in line:
                print(crayons.red(line))
            elif 'filtered' in line:
                print(crayons.yellow(line))
        else:
            print(line)


def main():
    parser = get_parser()
    args = vars(parser.parse_args())
    if args['version']:
        print(f"v{VERSION}")
        return None
    if args['list']:
        print(SCAN_LIST)
        return None
    if not args['target']:
        parser.print_help()
        return None
    if args['debug']:
        sl.cli_mode = False
    else:
        target = args['target']
        scanner = args['scanner'].lower()
        print(f"Running scanless v{VERSION}...\n")
        scanners = sl.scanners.keys()
        if args['all']:
            for s in scanners:
                print(f"{s}:")
                display(sl.scan(target, scanner=s)['raw'])
                print()
            else:
                return
                if args['random']:
                    scanner = choice(list(scanners))

            if scanner in scanners:
                print(f"{scanner}:")
                display(sl.scan(target, scanner=scanner)['raw'])
        else:
            print('Scanner not found, see --list to view all supported scanners.')