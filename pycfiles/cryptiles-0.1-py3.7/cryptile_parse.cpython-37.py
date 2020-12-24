# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cryptiles/cryptile_parse.py
# Compiled at: 2019-04-06 11:45:00
# Size of source mod 2**32: 1100 bytes
from argparse import ArgumentParser

def parse_args():
    """Define some args for cryptile."""
    _parser = ArgumentParser(add_help=True, description='\n  Cryptile returns a string or file encrypted with a key.\n\n  USAGE: cryptile [-f|-s] [string|path] -k passkey.\n  Cryptile encrypt a file or string by time, do not use -f and -s together.\n  ')
    _parser.add_argument('-f', '--file', action='store', required=False, help='Get the file path to encrypt.')
    _parser.add_argument('-s', '--string', action='store', required=False, help='Get the string to encrypt.')
    _parser.add_argument('-k', '--key', action='store', required=True, help='Get a string key to encrypt data.')
    _parser.add_argument('-e', '--encrypt', action='store_true', required=False, help='Encrypt data.')
    _parser.add_argument('-d', '--decrypt', action='store_true', required=False, help='Decrypt data.')
    return _parser.parse_args()