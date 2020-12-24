# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\diskspace\argpar.py
# Compiled at: 2019-01-14 13:08:50
# Size of source mod 2**32: 229 bytes
import argparse, sys

class Arguments(argparse.ArgumentParser):

    def error(self, message):
        raise RuntimeError(message)


def getarg():
    args = sys.argv
    args[0] = ''
    return ' '.join(args)