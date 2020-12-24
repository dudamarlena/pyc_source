# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /builds/krzyszti-software-funhouse/internal/sgi/venv/lib/python3.8/site-packages/sgi/command_line.py
# Compiled at: 2020-05-10 10:29:48
# Size of source mod 2**32: 442 bytes
import argparse
short_description = 'sgi - Super Git Ignore, tool for faster creation/modification of .gitignore files.'
parser = argparse.ArgumentParser(description=short_description)

def f(*args, **kwargs):
    """
    Purpose of this function is for tests to be executed
    """
    return 1


def main():
    args = parser.parse_args()
    f(args)
    print('It works!')