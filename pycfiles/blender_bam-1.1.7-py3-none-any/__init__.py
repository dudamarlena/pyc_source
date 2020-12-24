# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: bam/__init__.py
# Compiled at: 2016-09-15 08:07:03
import sys
__version__ = '1.0'

def main(argv=sys.argv):
    from .cli import main
    sys.exit(main(argv[1:]))


if __name__ == '__main__':
    sys.exit(main(sys.argv))