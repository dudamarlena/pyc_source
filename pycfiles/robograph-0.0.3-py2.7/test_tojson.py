# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/robograph/datamodel/tests/test_tojson.py
# Compiled at: 2016-07-13 17:51:17
from robograph.datamodel.nodes.lib import transcoders
DATA = dict(x=[1, 2, 3])
EXPECTED = '{"x": [1, 2, 3]}'

def test_requirements():
    expected = [
     'data']
    instance = transcoders.ToJSON()
    assert instance.requirements == expected


def test_input():
    instance = transcoders.ToJSON()
    instance.input(dict(data=DATA))
    instance.set_output_label('any')
    assert instance.output() == EXPECTED


def test_output():
    instance = transcoders.ToJSON(data=DATA)
    instance.set_output_label('any')
    assert instance.output() == EXPECTED