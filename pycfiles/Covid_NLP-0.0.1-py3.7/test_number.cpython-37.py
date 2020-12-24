# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/tests/test_number.py
# Compiled at: 2020-03-05 06:05:09
# Size of source mod 2**32: 355 bytes
import sys, pytest
from typing import Dict, List
from covid_nlp import number

def test_get_country():
    country = number.get_unique_country()
    assert isinstance(country, List)
    assert len(country) > 0


def test_get_confirmed_country():
    country = number.get_confirmed_country()
    assert isinstance(country, Dict)