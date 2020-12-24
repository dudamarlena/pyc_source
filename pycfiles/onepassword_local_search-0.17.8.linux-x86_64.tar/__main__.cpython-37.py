# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_local_search/__main__.py
# Compiled at: 2019-05-24 16:38:48
# Size of source mod 2**32: 191 bytes
import sys
import onepassword_local_search.CliSimple as CliSimple

def start():
    cli = CliSimple(*sys.argv)
    cli.run()


if __name__ == '__main__':
    start()