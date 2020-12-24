# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_query.py
# Compiled at: 2019-05-16 13:41:33
""" Test the query tool. """
import inspect
from insights import dr
from insights.tests import InputData
from insights.tools.query import load_obj, get_source, get_pydoc

def test_load_obj():
    assert load_obj('insights.dr') is dr
    assert load_obj('insights.tests.InputData') is InputData
    assert load_obj('foo.bar') is None
    return


def test_get_source():
    assert get_source('insights.dr') == inspect.getsource(dr)
    assert get_source('insights.tests.InputData') == inspect.getsource(InputData)
    assert get_source('foo.bar') is None
    return


def test_get_pydoc():
    assert get_pydoc('insights.dr') is not None
    assert get_pydoc('insights.tests.InputData') is not None
    assert get_pydoc('foo.bar') is None
    return