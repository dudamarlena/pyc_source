# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pfigue/Workspace/hex2words/venv-3.4-setup/lib/python3.4/site-packages/hex2words/program.py
# Compiled at: 2015-08-17 05:11:57
# Size of source mod 2**32: 2184 bytes
"""
Main function lives here.
"""
from __future__ import absolute_import
from __future__ import print_function
import sys, argparse, logging
FORMAT = '%(asctime)s %(name)s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
from .input import process_input
from .version import __version__, __authors__, __license__, __program_name__, __short_description__, get_platform_id

def get_version_banner():
    """Returns an unicode object with a description of
the program and the platform"""
    banner = "{name} version {version}.\nPlatform: '{platform}'.\n\n{short_description}\n\nDistributed under {license}.\nAuthors: {authors}.\n"
    params = {'version': __version__, 
     'authors': ', '.join(__authors__), 
     'license': __license__, 
     'platform': get_platform_id(), 
     'name': __program_name__, 
     'short_description': __short_description__}
    banner = banner.format(**params)
    return banner


def main():
    """Main()."""
    parser = argparse.ArgumentParser(description=__short_description__, epilog=None)
    parser.add_argument('-V', '--version', help='Show version and platform', action='store_true')
    parser.add_argument('hexnumbers_l', metavar='hexnumbers', help='Hex number to convert. You can also pipe to stdin.', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.version:
        banner = get_version_banner()
        print(banner)
        sys.exit(0)
    if len(args.hexnumbers_l) == 0:
        source = sys.stdin
        input_lines = source.readlines()
    else:
        input_lines = args.hexnumbers_l
    output = process_input(input_lines)
    if output is None:
        sys.exit(1)
    output = output.strip()
    print(output)
    sys.exit(0)