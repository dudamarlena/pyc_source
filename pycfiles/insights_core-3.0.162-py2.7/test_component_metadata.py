# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_component_metadata.py
# Compiled at: 2019-05-16 13:41:33
from insights.core import dr

class stage(dr.ComponentType):
    metadata = {'description': 'A processing stage.'}


@stage()
def report():
    return 'this is a regular report'


@stage(metadata={'description': 'Reports stuff about things.'})
def special_report():
    return 'this is a special report'


def test_component_metadata():
    msg = 'A processing stage.'
    special_msg = 'Reports stuff about things.'
    assert dr.get_metadata(report).get('description') == msg
    assert dr.get_metadata(special_report).get('description') == special_msg