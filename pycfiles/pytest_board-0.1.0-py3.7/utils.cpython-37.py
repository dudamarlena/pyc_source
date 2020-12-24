# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pytest_board/utils.py
# Compiled at: 2018-12-29 09:34:03
# Size of source mod 2**32: 128 bytes
from queue import Empty

def flush_q(q):
    try:
        while True:
            q.get_nowait()

    except Empty:
        pass