# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /evtfs/home/rcarney/Dropbox/projects/dploy/master/dploy/__main__.py
# Compiled at: 2017-10-14 18:30:09
# Size of source mod 2**32: 327 bytes
"""
The entry point when dploy is called as a module
"""
import sys
assert sys.version_info >= (3, 3), 'Requires Python 3.3 or Greater'
import dploy.cli as cli

def main():
    """
    main entry point when using dploy from the command line
    """
    cli.run()


if __name__ == '__main__':
    main()