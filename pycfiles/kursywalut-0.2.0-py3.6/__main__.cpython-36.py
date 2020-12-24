# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kursywalut/__main__.py
# Compiled at: 2018-12-20 11:59:26
# Size of source mod 2**32: 196 bytes
"""KursyWalut."""
import sys
from .interface import interface

def main():
    """Main function."""
    interface.run(sys.argv)


if __name__ == '__main__':
    main()