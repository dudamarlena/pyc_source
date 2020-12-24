# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\responder3\__main__.py
# Compiled at: 2019-08-15 18:46:23
# Size of source mod 2**32: 514 bytes
import sys, asyncio
from responder3.core.responder3 import Responder3

def main():
    loop = asyncio.get_event_loop()
    parser = Responder3.get_argparser()
    if len(sys.argv) < 2:
        parser.print_usage()
        return
    responder3 = Responder3.from_args(parser.parse_args())
    if responder3:
        loop.run_until_complete(responder3.run())
        print('Responder finished!')


if __name__ == '__main__':
    main()