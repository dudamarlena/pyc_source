# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_yaml_parser.py
# Compiled at: 2020-03-25 13:10:41
import datetime, pytest
from insights.core import YAMLParser, ParseException, SkipException
from insights.tests import context_wrap
bi_conf_content = ('\n{"remote_branch": -1, "remote_leaf": -1}\n').strip()
yaml_test_strings = {'\ntype:        Acquisition\ndate:        2019-07-09\n': {'type': 'Acquisition', 'date': datetime.date(2019, 7, 9)}, '\n- Hesperiidae\n- Papilionidae\n- Apatelodidae\n- Epiplemidae\n': [
                                                                      'Hesperiidae', 'Papilionidae', 'Apatelodidae', 'Epiplemidae']}
empty_yaml_content = ('\n---\n# This YAML file is empty\n').strip()
wrong_yaml_content = ('\n"unbalanced blackets: ]["\n').strip()

class FakeYamlParser(YAMLParser):
    """ Class for parsing the content of ``branch_info``."""
    pass


class MyYamlParser(YAMLParser):
    pass


def test_yaml_parser_success():
    for ymlstr in yaml_test_strings:
        ctx = context_wrap(ymlstr)
        assert FakeYamlParser(ctx).data == yaml_test_strings[ymlstr]


def test_yaml_parser_failure():
    ctx = context_wrap('boom /')
    with pytest.raises(ParseException) as (ex):
        FakeYamlParser(ctx)
    assert 'FakeYamlParser' in ex.value.args[0]


def test_settings_yml():
    ctx = context_wrap(bi_conf_content)
    ctx.content = bi_conf_content
    result = FakeYamlParser(ctx)
    assert result.data['remote_branch'] == -1
    assert result.data['remote_leaf'] == -1


def test_settings_yml_list():
    ctx = context_wrap(bi_conf_content)
    result = FakeYamlParser(ctx)
    assert result.data['remote_branch'] == -1
    assert result.data['remote_leaf'] == -1


def test_empty_content():
    ctx = context_wrap(empty_yaml_content)
    with pytest.raises(SkipException) as (ex):
        FakeYamlParser(ctx)
    assert 'There is no data' in ex.value.args[0]