# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_tags.py
# Compiled at: 2019-11-14 13:58:37
from insights.parsers.tags import Tags
from insights.tests import context_wrap
tags_json_content = ('\n{"zone": "east", "owner": "test", "exclude": "true", "group": "app-db-01"}\n').strip()

def test_tags_json():
    ctx = context_wrap(tags_json_content)
    ctx.content = tags_json_content
    result = Tags(ctx)
    assert result.data['zone'] == 'east'
    assert result.data['owner'] == 'test'
    assert result.data['exclude'] == 'true'
    assert result.data['group'] == 'app-db-01'