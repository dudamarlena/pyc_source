# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dr/Documents/code/Python/vps-manager/web/main.py
# Compiled at: 2019-05-28 23:31:27
# Size of source mod 2**32: 477 bytes
import tornado.ioloop
from tornado.ioloop import IOLoop
from web.setting import appication, port
from qlib.io import GeneratorApi
import os

def main():
    args = GeneratorApi({'port': 'set port '})
    if args.port:
        port = int(args.port)
    appication.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()