# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/robograph/datamodel/tests/test_apply.py
# Compiled at: 2016-07-13 17:51:17
from robograph.datamodel.nodes.lib import apply

def test_requirements():
    expected = [
     'function', 'argument']
    instance = apply.Apply()
    assert instance.requirements == expected


def test_input():
    method = lambda x: x + 1
    data = 7
    instance = apply.Apply()
    instance.input(dict(function=method, argument=data))
    instance.set_output_label('any')
    assert instance.output() == 8


def test_output():
    data = [
     4, 6, 9]
    instance = apply.Apply(function=sum, argument=data)
    instance.set_output_label('any')
    assert instance.output() == 19