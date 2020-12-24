# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\bulkrename\argpar.py
# Compiled at: 2018-08-20 04:47:53
# Size of source mod 2**32: 229 bytes
import argparse, sys

class Arguments(argparse.ArgumentParser):

    def error(self, message):
        raise RuntimeError(message)


def getarg():
    args = sys.argv
    args[0] = ''
    return ' '.join(args)