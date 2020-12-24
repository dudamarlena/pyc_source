# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/test.py
# Compiled at: 2014-08-17 14:49:28
__doc__ = '\nThis module is the test command of bowl.\n\nCreated on 11 August 2014\n@author: Charlie Lewis\n'
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