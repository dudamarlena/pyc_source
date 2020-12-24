# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kvlayer/tests/test_snowflake.py
# Compiled at: 2015-07-31 13:31:44
"""Tests for :mod:`kvlayer.snowflake`.

.. This software is released under an MIT/X11 open source license.
   Copyright 2015 Diffeo, Inc.

"""
from __future__ import absolute_import, division, print_function
import random, time, pytest
from kvlayer.encoders.packed import PackedEncoder
from kvlayer._local_memory import LocalStorage
from kvlayer.snowflake import Snowflake

@pytest.fixture
def client():
    c = LocalStorage()
    c._data = {}
    c.setup_namespace({'t': (long,)})
    return c


def test_snowflake_explicit():
    s = Snowflake(identifier=1, sequence=0)
    assert s(now=305419896) == 7911603571987120128
    assert s(now=305419896) == 7911603571987120129
    assert s(now=305419897) == 7911603567692152834


def test_snowflake_implicit(monkeypatch):
    monkeypatch.setattr(random, 'randint', lambda lo, hi: 17)
    monkeypatch.setattr(time, 'time', lambda : 305419896)
    s = Snowflake()
    assert s() == 7911603571988168721
    assert s() == 7911603571988168722
    assert s() == 7911603571988168723


def test_snowflake_wraparound():
    s = Snowflake(identifier=0, sequence=65535)
    assert s(now=305419896) == 7911603571987120127
    assert s(now=305419896) == 7911603571987054592


def test_snowflake_scan(client):
    s = Snowflake(identifier=0, sequence=0)
    client.put('t', ((s(now=305419896),), 'older'))
    client.put('t', ((s(now=305419897),), 'newer'))
    assert [ v for k, v in client.scan('t') ] == ['newer', 'older']


def test_snowflake_scan_wraparound(client):
    s = Snowflake(identifier=65535, sequence=65535)
    client.put('t', ((s(now=305419896),), 'older'))
    client.put('t', ((s(now=305419897),), 'newer'))
    assert [ v for k, v in client.scan('t') ] == ['newer', 'older']


def test_snowflake_scan_sequence(client):
    s = Snowflake(identifier=0, sequence=0)
    client.put('t', ((s(now=305419896),), 'oldest'))
    client.put('t', ((s(now=305419896),), 'older'))
    client.put('t', ((s(now=305419897),), 'newer'))
    client.put('t', ((s(now=305419897),), 'newest'))
    assert [ v for k, v in client.scan('t') ] == [
     'newer', 'newest', 'oldest', 'older']


def test_snowflake_fits_packed_encoder():
    encoder = PackedEncoder()
    s = Snowflake(identifier=0, sequence=0)
    skey = s(now=305419896)
    dbkey = encoder.serialize((skey,), (long,))
    assert dbkey == b'\xed\xcb\xa9\x88\x00\x00\x00\x00'
    kvlkey = encoder.deserialize(dbkey, (long,))
    assert kvlkey == (skey,)