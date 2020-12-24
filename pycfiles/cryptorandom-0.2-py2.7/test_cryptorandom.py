# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/cryptorandom/tests/test_cryptorandom.py
# Compiled at: 2018-09-06 14:35:51
"""Unit tests for cryptorandom PRNG"""
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
from ..cryptorandom import SHA256, int_from_hash

def test_SHA256():
    """
    Test that SHA256 prng is instantiated correctly
    """
    r = SHA256(5)
    assert repr(r) == b'SHA256 PRNG with seed 5 and counter 0'
    assert str(r) == b'SHA256 PRNG with seed 5 and counter 0'
    assert r.getstate() == (5, 0)
    r.next()
    assert r.getstate() == (5, 1)
    r.jumpahead(5)
    assert r.getstate() == (5, 6)
    r.seed(22)
    assert r.getstate() == (22, 0)
    r.setstate(2345, 3)
    assert r.getstate() == (2345, 3)


def test_SHA256_random():
    """
    Test that SHA256 PRNs are correct.
    The following tests match the output of Ron's and Philip's implementations.
    """
    r = SHA256(12345678901234567890)
    r.next()
    expected = b'1\r\x95\x9c\xe6Tvdz>\xc90t\xbe\xff\n\xa6\xd7 \x94\x92\x07\xda\xf9\x15q/\xd5tcQe'
    assert r.nextRandom() == expected
    r = SHA256(12345678901234567890)
    r.next()
    e1 = b'1\r\x95\x9c\xe6Tvdz>\xc90t\xbe\xff\n\xa6\xd7 \x94\x92\x07\xda\xf9\x15q/\xd5tcQe'
    e2 = b'\x95\xa9\xe6,IEZ\xe0\xbf\xce\xa9\x84\x9fo\xf0\x96\x01Q$\xb8\xa0\xd7\xd0\xa9\xdf' + b'\xd4Q\xc5\xfa\xfa"\xb7'
    expected = np.array(int_from_hash([e1, e2])) * 8.636168555094445e-78
    assert (r.random(2) == expected).all()
    r = SHA256()
    r.setstate(12345678901234567890, 1)
    assert r.random() == expected[0]


def test_SHA256_randint():
    """
    Test that SHA256 random integers are correct.
    The tests for next() and randint_trunc() match the output of Ron's and Philip's implementations.
    """
    r = SHA256(12345678901234567890)
    fiverand = r.randint_trunc(1, 1001, 5)
    assert (fiverand == np.array([876, 766, 536, 423, 164])).all()
    r = SHA256(12345678901234567890)
    onerand = r.randint_trunc(1, 1001)
    assert onerand == fiverand[0]
    r = SHA256(12345678901234567890)
    s = SHA256(12345678901234567890)
    t = int_from_hash(s.nextRandom())
    v = np.array([0] * 5, dtype=int)
    inx = 0
    while inx < 5:
        u = t & int(1023)
        while u > 1000:
            t = t >> 10
            u = t & int(1023)

        v[inx] = int(u) + 1
        t = t >> 10
        inx = inx + 1

    fiverand = r.randint(1, 1001, 5)
    assert (fiverand == v).all()
    r = SHA256(12345678901234567890)
    onerand = r.randint(1, 1001)
    assert onerand == fiverand[0]


def test_SHA256_bits():
    """
    Test that SHA256 randint uses bits correctly
    """
    r = SHA256(12345678901234567890)
    s = SHA256(12345678901234567890)
    v = s.nextRandom()
    cumbits = 0
    for k in [10, 20, 30]:
        val = r.getrandbits(k)
        assert val == int_from_hash(v) >> cumbits & int(2 ** k - 1)
        cumbits = cumbits + k

    r = SHA256(12345678901234567890)
    s = SHA256(12345678901234567890)
    val = r.getrandbits(500)
    v = int_from_hash(s.nextRandom())
    w = int_from_hash(s.nextRandom())
    assert val == (w << 256 | v) & int(3273390607896141870013189696827599152216642046043064789483291368096133796404674554883270092325904157150886684127560071009217256545885393053328527589375)
    r = SHA256(12345678901234567890)
    val = r.randbelow_from_randbits(5)
    assert val == 3