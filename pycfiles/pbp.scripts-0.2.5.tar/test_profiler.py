# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/MacDev/perso/atomisator.ziade.org/packages/pbp.scripts/pbp/scripts/tests/test_profiler.py
# Compiled at: 2008-08-19 04:53:13
from pbp.scripts import profiler
import time
from nose.tools import *
import random

def test_profile():

    @profiler.profile(name='tested')
    def tested():
        time.sleep(0.25)

    tested()
    res = profiler.stats['tested']
    assert res['stones'] < 600
    assert res['memory'] < 1000


def test_memory_grow():
    growing = []

    def stable():
        memory = []

        def _get_char():
            return chr(random.randint(97, 122))

        for i in range(100):
            size = random.randint(20, 150)
            data = [ _get_char() for i in range(size) ]
            memory.append(('').join(data))

        return ('\n').join(memory)

    def unstable():
        growing.append(stable())

    assert profiler.memory_grow(stable) <= 500
    assert profiler.memory_grow(unstable) > 850000