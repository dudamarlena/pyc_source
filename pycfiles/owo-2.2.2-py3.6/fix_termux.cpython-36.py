# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/owo/fix_termux.py
# Compiled at: 2017-05-02 07:34:37
# Size of source mod 2**32: 309 bytes
"""
Used to fix termux shebangs
"""
import os

def main():
    os.system('termux-fix-shebang /data/data/com.termux/files/usr/bin/owo')
    os.system('termux-fix-shebang /data/data/com.termux/files/usr/bin/owo-bg')


if __name__ == '__main__':
    main()