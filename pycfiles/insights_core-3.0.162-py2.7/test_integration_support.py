# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_integration_support.py
# Compiled at: 2020-03-25 13:10:41
from insights.plugins.ps_rule_fakes import psaux_no_filter, psauxww_ds_filter, psalxwww_parser_filter
from insights.specs import Specs
from . import InputData, run_test
import pytest

def test_run_test_missing_filters_exception():
    """
    The rule underlying datasource requires a filter,
    an exception should be raised because filter was not
    added in the rule module.
    """
    input_data = InputData('fake_input')
    input_data.add(Specs.ps_aux, 'FAKE_CONTENT')
    with pytest.raises(Exception):
        run_test(psaux_no_filter, input_data, None)
    return


def test_run_test_no_missing_filters_using_datasource():
    """
    Required filter was added directly to the datasouce,
    ``run_test`` should complete without any exceptions.
    """
    input_data = InputData('fake_input')
    input_data.add(Specs.ps_auxww, 'FAKE_CONTENT')
    result = run_test(psauxww_ds_filter, input_data, None)
    assert result
    return


def test_run_test_no_missing_filters_using_parser():
    """
    Required filter was added to using the parser,
    ``run_test`` should complete without any exceptions.
    """
    input_data = InputData('fake_input')
    input_data.add(Specs.ps_alxwww, 'FAKE_CONTENT')
    result = run_test(psalxwww_parser_filter, input_data, None)
    assert result
    return