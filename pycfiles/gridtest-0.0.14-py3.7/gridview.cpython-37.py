# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gridtest/client/gridview.py
# Compiled at: 2020-05-12 15:34:00
# Size of source mod 2**32: 1796 bytes
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from gridtest.main.test import GridRunner, GridTest
from gridtest.utils import write_json
import os, json, sys

def main(args, extra):
    if not args.input:
        args.input = [
         'grids.yml']
    input_file = args.input.pop(0)
    if not os.path.exists(input_file):
        sys.exit(f"{input_file} does not exist.")
    runner = GridRunner(input_file)
    grids = runner.get_grids()
    if args.input:
        name = args.input[0]
        if name in grids:
            grid = grids[name]
        else:
            sys.exit(f"{name} is not a valid grid name in {input_file}")
        if args.arg:
            if args.arg not in grid.args:
                sys.exit(f"{args.arg} is not an argument in grid {grid}.")
        if args.count and args.arg:
            try:
                print(f"Variable {args.arg} has length {len(grid.args[args.arg])}.")
            except:
                print((f"{grid.args[args.arg]}"))

        else:
            if args.count:
                print(f"{len(list(grid))} argument sets produced.")
            else:
                if args.arg:
                    print(grid.args[args.arg])
                else:
                    if args.export:
                        grids = list(grid)
                        write_json(grids, args.export)
                    else:
                        for argset in grid:
                            print(argset)

    else:
        print('\n'.join(list(grids.keys())))