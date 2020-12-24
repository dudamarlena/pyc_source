# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mstolarczyk/Uczelnia/UVA/code/refgenieserver/refgenieserver/__main__.py
# Compiled at: 2020-01-16 15:33:49
# Size of source mod 2**32: 188 bytes
import sys
from .main import main
if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print('Program canceled by user')
        sys.exit(1)