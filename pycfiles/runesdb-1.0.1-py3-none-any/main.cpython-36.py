# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\clement_besnier\PycharmProjects\old_norse_runes_db\runesdb\main.py
# Compiled at: 2019-09-20 10:57:29
# Size of source mod 2**32: 388 bytes
__version__ = '0.0.0.1'
import argparse
from runesdb import reader

def main(filename):
    return reader.read(filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='give an export file from RuneSDB')
    args = parser.parse_args()
    main(args.filename)