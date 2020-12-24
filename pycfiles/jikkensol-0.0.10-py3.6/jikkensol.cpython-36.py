# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jikkensol/jikkensol.py
# Compiled at: 2017-12-10 23:29:59
# Size of source mod 2**32: 135 bytes
from jikkensol import hello

def main():
    h = hello.Hello('太郎')
    h.say()
    h.song()


if __name__ == '__main__':
    main()