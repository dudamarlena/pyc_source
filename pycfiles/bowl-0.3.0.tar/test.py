# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/test.py
# Compiled at: 2014-08-17 14:49:28
"""
This module is the test command of bowl.

Created on 11 August 2014
@author: Charlie Lewis
"""
import os

class test(object):
    """
    This class is responsible for the test command of the cli.
    """

    @classmethod
    def main(self, args):
        print args
        if args.f:
            pass
        else:
            cmd = 'py.test -v --cov bowl --cov-report term-missing -x ' + args.path
            out = os.popen(cmd).read()
            print out
            if args.c:
                cmd = 'coveralls --base_dir ' + args.path
                out = os.popen(cmd).read()
                print out