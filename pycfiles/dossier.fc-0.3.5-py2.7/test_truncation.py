# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dossier/fc/tests/test_truncation.py
# Compiled at: 2015-09-05 21:22:50
"""dossier.fc Feature Collections

.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2015 Diffeo, Inc.

"""
from __future__ import absolute_import, division, print_function
try:
    from collections import Counter
except ImportError:
    from backport_collections import Counter

from operator import itemgetter
from dossier.fc.tests import counter_type

def test_truncation(counter_type):
    num = 100
    data = {}
    for x in xrange(num):
        data[str(x)] = x + 1

    counter = counter_type(data)
    assert len(counter) == num
    truncation_length = 10
    counter.truncate_most_common(truncation_length)
    assert len(counter) == truncation_length
    most_common = Counter(data).most_common(truncation_length)
    from_counter = map(itemgetter(1), counter.most_common(truncation_length))
    expected = map(itemgetter(1), most_common)
    from_counter = map(abs, from_counter)
    assert from_counter == expected
    assert set(counter_type(dict(most_common)).items()) == set(counter.items())
    expected = {}
    for x in xrange(90, 100):
        expected[str(x)] = x + 1

    should_be_counter = counter_type(expected)
    assert should_be_counter == counter