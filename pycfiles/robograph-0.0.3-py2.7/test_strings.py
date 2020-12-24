# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/robograph/datamodel/tests/test_strings.py
# Compiled at: 2016-07-13 17:51:17
from robograph.datamodel.nodes.lib import strings

def test_templated_string():
    expected_requirements = [
     'template', 'parameters']
    expected_output = 'After 1 comes 2 but then there is three'
    instance = strings.TemplatedString(template='After {p1} comes {p2} but then there is {p3}')
    instance.input(dict(parameters=dict(p1=1, p2=2, p3='three')))
    assert instance.requirements == expected_requirements
    assert instance.output() == expected_output