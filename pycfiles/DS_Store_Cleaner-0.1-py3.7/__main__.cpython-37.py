# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/DS_Store_Cleaner/__main__.py
# Compiled at: 2020-01-13 11:16:07
# Size of source mod 2**32: 263 bytes
import sys
from .DS_Store_Cleaner import *

def main():
    if len(sys.argv) > 1:
        files = all_file(sys.argv[1])
        remove_file(files)
    else:
        files = all_file(os.getcwd())
        remove_file(files)


if __name__ == '__main__':
    main()