# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/alpaca_trade_api_fixed/__main__.py
# Compiled at: 2020-02-14 14:55:34
# Size of source mod 2**32: 576 bytes
import argparse
from .rest import REST

def run(args):
    api = REST(**args)
    try:
        from IPython import embed
        embed()
    except ImportError:
        import code
        code.interact(locals=(locals()))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--key-id', help='APCA_API_KEY_ID')
    parser.add_argument('--secret-key', help='APCA_API_SECRET_KEY')
    parser.add_argument('--base-url')
    args = parser.parse_args()
    run({k:v for k, v in vars(args).items() if v is not None if v is not None})


if __name__ == '__main__':
    main()