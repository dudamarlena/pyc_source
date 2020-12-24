# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/test/test_redis_queue.py
# Compiled at: 2010-12-02 22:02:41
from redis_simple_queue import *

def test_basic():
    delete_jobs('tasks')
    put('tasks', '42')
    assert 'tasks' in get_all_queues()
    assert queue_stats('tasks')['queue_size'] == 1
    assert reserve('tasks') == '42'
    assert queue_stats('tasks')['queue_size'] == 0


if __name__ == '__main__':
    test_basic()