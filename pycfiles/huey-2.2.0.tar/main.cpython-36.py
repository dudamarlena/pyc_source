# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/charles/code/huey/examples/simple/main.py
# Compiled at: 2019-03-18 22:37:34
# Size of source mod 2**32: 479 bytes
import os
if os.environ.get('WORKER_CLASS') in ('greenlet', 'gevent'):
    print('Monkey-patching for gevent.')
    from gevent import monkey
    monkey.patch_all()
import sys
from config import huey
from tasks import add
if __name__ == '__main__':
    if sys.version_info[0] == 2:
        input = raw_input
    print('Huey Demo -- adds two numbers.')
    a = int(input('a = '))
    b = int(input('b = '))
    result = add(a, b)
    print('Result:')
    print(result.get(True))