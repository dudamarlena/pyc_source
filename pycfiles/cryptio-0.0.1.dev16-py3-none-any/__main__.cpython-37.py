# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cryptiles/__main__.py
# Compiled at: 2019-04-06 13:05:37
# Size of source mod 2**32: 1073 bytes
import os, binascii
from .cryptile_parse import parse_args
from .cryptile import crypt_data

def main():
    """Main function to be called by the script cryptile."""
    args = parse_args()
    _crypt = crypt_data(args.key)
    if args.file:
        if os.path.exists(args.file):
            _file = open(args.file, 'r').read()
            with open(args.file, 'w') as (crypt_file):
                if args.encrypt:
                    crypt_file.write(_crypt.encrypt(_file).decode())
                if args.decrypt:
                    try:
                        crypt_file.write(_crypt.decrypt(_file).decode())
                    except binascii.Error:
                        print('This do not contaim a base64 data.')

    if args.string:
        if args.encrypt:
            print(_crypt.encrypt(args.string).decode())
        try:
            if args.decrypt:
                print(_crypt.decrypt(args.string).decode())
        except binascii.Error:
            print('This string is not a base64 string.')


if __name__ == '__main__':
    main()