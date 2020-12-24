# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/robograph/datamodel/tests/test_ifthenapply.py
# Compiled at: 2016-07-13 17:51:17
import math
from robograph.datamodel.nodes.lib import branching

def test_requirements():
    expected = [
     'data', 'condition', 'function_true', 'function_false']
    instance = branching.IfThenApply()
    assert instance.requirements == expected


def test_input():
    data = 7
    condition = lambda x: x >= 0
    function_true = lambda x: math.sqrt(x)
    function_false = lambda x: 0
    instance = branching.IfThenApply()
    instance.input(dict(data=data, condition=condition, function_true=function_true, function_false=function_false))
    instance.set_output_label('any')
    assert instance.output() == math.sqrt(data)
    data = -34
    instance.reset()
    instance.input(dict(data=data, condition=condition, function_true=function_true, function_false=function_false))
    instance.set_output_label('any')
    assert instance.output() == 0


def test_output():
    data = 7
    condition = lambda x: x >= 0
    function_true = lambda x: math.sqrt(x)
    function_false = lambda x: 0
    instance = branching.IfThenApply(data=data, condition=condition, function_true=function_true, function_false=function_false)
    instance.set_output_label('any')
    assert instance.output() == math.sqrt(data)
    data = -34
    instance = branching.IfThenApply(data=data, condition=condition, function_true=function_true, function_false=function_false)
    instance.set_output_label('any')
    assert instance.output() == 0