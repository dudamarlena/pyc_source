# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gridtest/client/gridview.py
# Compiled at: 2020-05-07 19:46:42
# Size of source mod 2**32: 1171 bytes
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from gridtest.main.test import GridRunner, GridTest
import os, json, sys

def main(args, extra):
    if not args.input:
        args.input = [
         'grids.yml']
    else:
        input_file = args.input.pop(0)
        if not os.path.exists(input_file):
            sys.exit(f"{input_file} does not exist.")
        else:
            runner = GridRunner(input_file)
            grids = runner.get_grids()
            if args.input:
                name = args.input[0]
                if name in grids:
                    content = grids[name]
                else:
                    sys.exit(f"{name} is not a valid grid name in {input_file}")
            else:
                content = grids
            if args.count:
                print(f"{len(content)} lists produced.")
            else:
                if args.list:
                    print('\n'.join(grids.keys()))
                else:
                    if args.compact:
                        print(content)
                    else:
                        print(json.dumps(content, indent=4))