# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gridtest/client/shell.py
# Compiled at: 2020-04-29 17:34:32
# Size of source mod 2**32: 2651 bytes
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from gridtest.main.test import GridRunner, GridTest
import os, sys

def main(args, extra):
    lookup = {'ipython':ipython, 
     'python':python,  'bpython':bpython}
    shells = ['ipython', 'python', 'bpython']
    import gridtest.defaults as shell
    shell = shell.lower()
    if shell in lookup:
        try:
            return lookup[shell](args)
        except ImportError:
            pass

    for shell in shells:
        try:
            return lookup[shell](args)
        except ImportError:
            pass


def get_runner(args):
    """if the user provides a gridtest file to load, return a runner
    """
    runner = None
    if args.input is not None:
        if not os.path.exists(args.input):
            sys.exit(f"Input file {args.input} does not exist.")
        try:
            runner = GridRunner(args.input)
        except:
            sys.exit('Error creating GridRunner, try running shell without test yaml file to debug.')

    return runner


def print_runner(runner, testfile):
    """If a runner is provided, print instructions for using it. Otherwise
       show instructions for adding a test file.
    """
    print('\n\x1b[1mGridtest Interactive Shell\x1b[0m')
    if testfile:
        print(f"testfile: {testfile}")
    if runner:
        print(f"  runner: {runner}")
    else:
        if not runner:
            if testfile:
                print('runner = GridRunner({testfile})')
        if not runner:
            if not testfile:
                print("runner = GridRunner('tests.yml')")


def ipython(args):
    """give the user an ipython shell, optionally with an endpoint of choice.
    """
    from gridtest.main.test import GridRunner, GridTest
    testfile = args.input
    runner = get_runner(args)
    print_runner(runner, testfile)
    import IPython
    IPython.embed()


def bpython(args):
    from gridtest.main.test import GridRunner, GridTest
    import bpython
    runner = get_runner(args)
    print_runner(runner, args.input)
    bpython.embed(locals_={'runner':runner,  'testfile':args.input})


def python(args):
    from gridtest.main.test import GridRunner, GridTest
    import code
    runner = get_runner(args)
    print_runner(runner, args.input)
    code.interact(local={'runner':runner,  'testfile':args.input})