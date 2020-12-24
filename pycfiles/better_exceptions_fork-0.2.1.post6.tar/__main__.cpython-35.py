# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/adrie/Desktop/Programmation/better-exceptions/better_exceptions/__main__.py
# Compiled at: 2018-01-24 17:26:56
# Size of source mod 2**32: 787 bytes
import argparse, imp, os
from better_exceptions import hook
from better_exceptions.repl import interact
hook()
parser = argparse.ArgumentParser(description='A Python REPL with better exceptions enabled', prog='python -m better_exceptions')
parser.add_argument('-q', '--quiet', help="don't show a banner", action='store_true')
parser.add_argument('-i', '--no-init', dest='no_init', help="don't load ~/.pyinit", action='store_true')
parser.add_argument('--banner', help='show a custom banner')
args = parser.parse_args()
startup_file = os.getenv('PYTHONSTARTUP')
if not args.no_init and startup_file is not None:
    with open(startup_file, 'r') as (fd):
        imp.load_module('pystartup', fd, startup_file, ('.py', 'r', imp.PY_SOURCE))
interact(args.quiet, args.banner)