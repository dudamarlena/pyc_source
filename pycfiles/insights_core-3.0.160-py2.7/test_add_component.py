# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_add_component.py
# Compiled at: 2019-05-16 13:41:33
from insights import combiner
from insights.tests import archive_provider, InputData

@combiner()
def one():
    return 1


@combiner()
def two():
    return 2


@combiner(one, two)
def three(x, y):
    return x + y


@archive_provider(three)
def integration_tests():
    data = InputData()
    data.add_component(two, 5)
    yield (data, 6)