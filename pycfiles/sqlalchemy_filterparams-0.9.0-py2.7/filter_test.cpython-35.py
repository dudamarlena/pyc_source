# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cbrand/projects/python-sqlalchemy-filterparams/build/lib/sqlalchemy_filterparams_tests/filter_test.py
# Compiled at: 2016-02-20 19:16:16
# Size of source mod 2**32: 682 bytes
from expects import *
from sqlalchemy import Integer
from sqlalchemy_filterparams.filters import EqFilter, NeqFilter

def test_identification_by_str():
    expect(EqFilter(None)).to(equal('eq'))


def test_negative_identification_by_str():
    expect(EqFilter(None)).to_not(equal('neq'))


def test_identification_by_obj():
    expect(EqFilter(None)).to(equal(EqFilter(None)))


def test_negative_identification_by_obj():
    expect(EqFilter(None)).to_not(equal(NeqFilter(None)))


def test_negative_identification_by_other():
    expect(EqFilter(None)).to_not(equal(1))


def test_apply_with_type():
    EqFilter(None).apply(Integer, '1')