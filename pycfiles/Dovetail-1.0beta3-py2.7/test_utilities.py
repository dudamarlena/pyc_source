# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/dovetail/util/test_utilities.py
# Compiled at: 2012-08-01 03:51:57
"""py.test test script for utilities.py"""
from utilities import enum
import pytest

class TestEnum:
    enumeration = enum(ONE=1, TWO=2, THREE=3, FOUR='four')

    def test_basics(self):
        assert 1 == TestEnum.enumeration.ONE
        assert 2 == TestEnum.enumeration.TWO
        assert 3 == TestEnum.enumeration.THREE
        assert 'four' == TestEnum.enumeration.FOUR

    def test_as_str(self):
        assert 'ONE' == TestEnum.enumeration.as_str(TestEnum.enumeration.ONE)
        assert 'TWO' == TestEnum.enumeration.as_str(TestEnum.enumeration.TWO)
        assert 'THREE' == TestEnum.enumeration.as_str(TestEnum.enumeration.THREE)
        assert 'FOUR' == TestEnum.enumeration.as_str(TestEnum.enumeration.FOUR)

    def test_lookup(self):
        assert TestEnum.enumeration.ONE == TestEnum.enumeration.lookup('ONE')
        assert TestEnum.enumeration.TWO == TestEnum.enumeration.lookup('TWO')
        assert TestEnum.enumeration.THREE == TestEnum.enumeration.lookup('THREE')
        assert TestEnum.enumeration.FOUR == TestEnum.enumeration.lookup('FOUR')

    def test_lookup_miss(self):
        with pytest.raises(KeyError):
            TestEnum.enumeration.lookup('NOT_HERE')

    def test_as_str_miss(self):
        with pytest.raises(KeyError):
            TestEnum.enumeration.as_str('NOT_HERE')

    def test_names(self):
        assert set(TestEnum.enumeration.names()) == {'ONE', 'TWO', 'THREE', 'FOUR'}