# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Auzzy\Documents\git\pyinq\examples\fixture_error.py
# Compiled at: 2013-10-27 20:36:12
from pyinq.tags import before, after, test
from pyinq.asserts import fail, assert_true

@before
def failing_fixture():
    raise Exception('Manual exception')


@test
def test():
    assert_true(4 == 4)


@after
def teardown_after():
    assert_true(True)