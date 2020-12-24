# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: py-build/2.7/bdist.linux-x86_64/egg/riak/tests/pool-grinder.py
# Compiled at: 2016-11-17 13:57:20
"""
Copyright 2015 Basho Technologies, Inc.

This file is provided to you under the Apache License,
Version 2.0 (the "License"); you may not use this file
except in compliance with the License.  You may obtain
a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""
from __future__ import print_function
from six import PY2
from threading import Thread
import sys
from pool import Pool
from random import SystemRandom
from time import sleep
if PY2:
    from Queue import Queue
else:
    from queue import Queue
sys.path.append('../transports/')

class SimplePool(Pool):

    def __init__(self):
        self.count = 0
        Pool.__init__(self)

    def create_resource(self):
        self.count += 1
        return [self.count]

    def destroy_resource(self, resource):
        del resource[:]


class EmptyListPool(Pool):

    def create_resource(self):
        return []


def test():
    started = Queue()
    n = 1000
    threads = []
    touched = []
    pool = EmptyListPool()
    rand = SystemRandom()

    def _run():
        psleep = rand.uniform(0.05, 0.1)
        with pool.transaction() as (a):
            started.put(1)
            started.join()
            a.append(rand.uniform(0, 1))
            if psleep > 1:
                print(psleep)
            sleep(psleep)

    for i in range(n):
        th = Thread(target=_run)
        threads.append(th)
        th.start()

    for i in range(n):
        started.get()
        started.task_done()

    for element in pool:
        touched.append(element)

    for thr in threads:
        thr.join()

    if set(pool.elements) != set(touched):
        print(set(pool.elements) - set(touched))
        return False
    else:
        return True


ret = True
count = 0
while ret:
    ret = test()
    count += 1
    print(count)