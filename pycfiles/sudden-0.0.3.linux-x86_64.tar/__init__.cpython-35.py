# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/raony/dev/venv/lib/python3.5/site-packages/sudden/__init__.py
# Compiled at: 2017-12-16 21:30:43
# Size of source mod 2**32: 420 bytes
import argparse
from sudden.main import Sudden
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--update', dest='update', action='store_true')
parser.add_argument('-i', dest='tool', required=False, nargs='+', metavar='conda', help='any tool to be installed')
args = parser.parse_args()
print(args)
s = Sudden()
if args.update:
    s.update()
if args.tool:
    s.install(args.tool)