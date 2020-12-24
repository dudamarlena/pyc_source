# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_branch_info.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.branch_info import BranchInfo
from insights.tests import context_wrap
bi_conf_content = ('\n{"remote_branch": -1, "remote_leaf": -1}\n').strip()

def test_settings_yml():
    ctx = context_wrap(bi_conf_content)
    ctx.content = bi_conf_content
    result = BranchInfo(ctx)
    assert result.data['remote_branch'] == -1
    assert result.data['remote_leaf'] == -1