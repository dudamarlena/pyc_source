# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asciigraphic/__main__.py
# Compiled at: 2018-11-16 14:05:26
# Size of source mod 2**32: 456 bytes
import asciichartpy

def main():
    list = [
     12, 12, 22, 12, 8, 4, 14]
    print(asciichartpy.plot(list))


if __name__ == '__main__':
    main()