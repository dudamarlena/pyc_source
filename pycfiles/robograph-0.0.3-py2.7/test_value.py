# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/robograph/datamodel/tests/test_value.py
# Compiled at: 2016-07-13 17:51:17
from robograph.datamodel.nodes.lib import value

def test_requirements():
    expected = [
     'value']
    instance = value.Value()
    assert instance.requirements == expected


def test_input():
    expected = '1234'
    instance = value.Value()
    instance.input(dict(value=expected))
    instance.set_output_label('any')
    assert instance.output() == expected


def test_output():
    expected = dict(expected='1234')
    instance = value.Value(value=expected)
    instance.set_output_label('any')
    assert instance.output() == expected