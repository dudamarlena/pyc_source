# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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