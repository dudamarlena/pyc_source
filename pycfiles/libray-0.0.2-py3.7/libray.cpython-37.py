# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/libray/libray.py
# Compiled at: 2019-07-07 14:23:16
# Size of source mod 2**32: 1597 bytes
import argparse
try:
    from libray import core
except ImportError:
    import core

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A Libre (FLOSS) Python application for unencrypting, extracting, repackaging, and encrypting PS3 ISOs')
    parser.add_argument('-v', '--verbose', help='Increase verbosity', action='count')
    parser.add_argument('-o', '--output', dest='output', type=str, help='Output filename', default='output.iso')
    parser.add_argument('-k', '--ird', dest='ird', type=str, help='Path to .ird file', default='')
    required = parser.add_argument_group('required arguments')
    required.add_argument('-i', '--iso', dest='iso', type=str, help='Path to .iso file', required=True)
    args = parser.parse_args()
    core.decrypt(args)