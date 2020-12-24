# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pytest_board/__main__.py
# Compiled at: 2018-12-29 09:34:03
# Size of source mod 2**32: 151 bytes
import os, sys
if __name__ == '__main__':
    sys.path.append(os.path.dirname(__file__))
    from pytest_board.command import main
    main()