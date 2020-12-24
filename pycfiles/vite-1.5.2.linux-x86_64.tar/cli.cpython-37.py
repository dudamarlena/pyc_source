# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/icy/code/vite/.env/lib/python3.7/site-packages/vite/cli.py
# Compiled at: 2019-10-02 11:57:00
# Size of source mod 2**32: 1351 bytes
import argparse, sys
from vite import vite
from huepy import *
from vite import __version__

def main():
    desc = green('A simple and minimal static site generator.')
    usage = lightblue('vite') + ' [options]'
    parser = argparse.ArgumentParser(description=desc, usage=usage)
    parser.add_argument('-v', '--version', action='version', version='{version}'.format(version=__version__))
    sp = parser.add_subparsers(dest='cmd', help='Options to help create, build and serve your project.')
    sp_init = sp.add_parser('init')
    sp_new = sp.add_parser('new')
    for cmd in ('build', 'serve'):
        sp.add_parser(cmd)

    sp_init.add_argument('path')
    sp_new.add_argument('path')
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    else:
        if args.cmd == 'init':
            if args.path:
                vite.create_project(args.path)
            else:
                parser.print_help()
        else:
            if args.cmd == 'new':
                if args.path:
                    vite.import_config()
                    vite.create_path(args.path)
                else:
                    parser.print_help()
            else:
                if args.cmd == 'build':
                    vite.import_config()
                    vite.builder()
                else:
                    if args.cmd == 'serve':
                        vite.import_config()
                        vite.server()
                    else:
                        parser.print_help()