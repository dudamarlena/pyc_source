# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/tests.py
# Compiled at: 2017-09-08 18:43:17
# Size of source mod 2**32: 409 bytes
import re, hypothesis.strategies as st
from hypothesis import given
from luxinema.luxinema import get_movie_id

@given(st.sampled_from(('Thelma & Louise', 'Apocalypse Now!', 'De Boezemvriend', 'Fack ju Göhte')))
def test_get_movie_id(s):
    movie_id = get_movie_id(s)
    assert re.search('tt\\d{7}', movie_id)