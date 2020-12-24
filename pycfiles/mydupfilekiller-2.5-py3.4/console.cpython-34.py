# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mydupfilekiller\console.py
# Compiled at: 2014-07-03 04:09:25
# Size of source mod 2**32: 779 bytes
import argparse
from mydupfilekiller import __version__
from mydupfilekiller.core import *
__all__ = [
 'main']

def main():
    """
    Simple console version for the module.
    :return: None
    """
    parser = argparse.ArgumentParser(description='My Duplicate File Killer.')
    parser.add_argument('-l', '--list', default=False, action='store_true', help='List duplicate files only.')
    parser.add_argument('--version', action='version', version='My Duplicate File Killer v%s' % __version__)
    parser.add_argument('paths', nargs='+')
    ns = parser.parse_args()
    if not ns.list:
        find_and_delete(ns.paths, output=True)
    else:
        find(ns.paths, output=True)


if __name__ == '__main__':
    main()