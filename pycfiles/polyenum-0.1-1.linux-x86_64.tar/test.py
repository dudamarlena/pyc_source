# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/polyenum/test.py
# Compiled at: 2014-09-13 20:47:09
from enumerators import InscribedTreeEnumerator, InscribedSnakeEnumerator, PolyominoesEnumerator

def test_snakes():
    import time
    print 'Initial test'
    start = time.time()
    it = InscribedSnakeEnumerator(33, 7, 7)
    s = 0
    while it.has_next():
        print it.next_obj().ascii()
        s += 1

    print 'Number of snakes: %s' % s
    end = time.time()
    print 'Time elapsed: %s seconds' % (end - start)


def test_trees():
    import time
    print 'Initial test'
    start = time.time()
    it = InscribedTreeEnumerator(7, 3, 3)
    s = 0
    while it.has_next():
        print it.next_obj().ascii()
        s += 1

    print 'Number of trees: %s' % s
    end = time.time()
    print 'Time elapsed: %s seconds' % (end - start)


def test_polyomino():
    import time
    print 'Initial test'
    it = PolyominoesEnumerator(4)
    while it.has_next():
        print it.next_obj()

    start = time.time()
    for area in range(1, 11):
        it = PolyominoesEnumerator(area)
        s = 0
        while it.has_next():
            it.next_obj()
            s += 1

        print area, s

    end = time.time()
    print 'Time elapsed: %s seconds' % (end - start)