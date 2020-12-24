# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_parser_continue_on_error.py
# Compiled at: 2019-11-14 13:57:46
from insights import dr, parser
from insights.core.plugins import component

@component()
def data():
    return [1, 2, 3, 4, 5]


@parser(data)
class Lax(object):
    count = 0

    def __init__(self, d):
        if Lax.count > 3:
            raise Exception('Lax')
        Lax.count += 1


@parser(data, continue_on_error=False)
class Boom(object):
    count = 0

    def __init__(self, d):
        if Boom.count > 3:
            raise Exception('Boom')
        Boom.count += 1


def test_dont_continue_on_error():
    Boom.count = 0
    broker = dr.run(Boom)
    assert Boom not in broker


def test_continue_on_error():
    Lax.count = 0
    broker = dr.run(Lax)
    assert len(broker[Lax]) == 4