# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\underverse\tests\speed_test.py
# Compiled at: 2012-02-16 10:47:35
from underverse import Underverse
from underverse.model import Document
from test_data_gen import Person
from time import clock
uv = Underverse()
test = uv.test

def load(collection, num):
    test.purge()
    ppl = [ Person().__dict__ for p in range(num) ]
    start = clock()
    for p in ppl:
        collection.add(p)

    return '%s - %0.5f elapsed' % (num, clock() - start)


def load_bulk(collection, num, buffer=150000):
    test.purge()
    data = []
    ppl = [ Person().__dict__ for p in range(num) ]
    start = clock()
    for p, d in enumerate(ppl):
        data.append(d)
        if p > 1 and p % buffer == 0:
            collection.add(data)
            print '%s - %0.5f elapsed' % (p, clock() - start)
            data = []

    collection.add(data)
    return '%s - %0.5f elapsed' % (num, clock() - start)


def timing(col, num, fast_only=False, buffer=150000):
    if not fast_only:
        print 'load:      ', load(col, num)
    print 'load_bulk: ', load_bulk(col, num, buffer)
    print


timing(test, 250)
uv.dump('speed_test_smaller.sql')