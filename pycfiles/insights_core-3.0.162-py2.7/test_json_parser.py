# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_json_parser.py
# Compiled at: 2019-11-14 13:57:46
import pytest
from insights.core import JSONParser, ParseException
from insights.tests import context_wrap

class MyJsonParser(JSONParser):
    pass


json_test_strings = {'{"a": "1", "b": "2"}': {'a': '1', 'b': '2'}, '[{"a": "1", "b": "2"},{"a": "3", "b": "4"}]': [{'a': '1', 'b': '2'}, {'a': '3', 'b': '4'}]}

def test_json_parser_success():
    for jsonstr in json_test_strings:
        ctx = context_wrap(jsonstr)
        assert MyJsonParser(ctx).data == json_test_strings[jsonstr]


def test_json_parser_failure():
    ctx = context_wrap('boom')
    with pytest.raises(ParseException) as (ex):
        MyJsonParser(ctx)
    assert 'MyJsonParser' in ex.value.args[0]