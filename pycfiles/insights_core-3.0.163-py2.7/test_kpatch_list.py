# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_kpatch_list.py
# Compiled at: 2020-03-25 13:10:41
import pytest, doctest
from insights.tests import context_wrap
from insights.parsers import kpatch_list, SkipException
NORMAL_OUTPUT = ('\nLoaded patch modules:\nkpatch_3_10_0_1062_1_1_1_4 [enabled]\n\nInstalled patch modules:\nkpatch_3_10_0_1062_1_1_1_4 (3.10.0-1062.1.1.el7.x86_64)\n').strip()
MULTILINE_OUTPUT = ('\nLoaded patch modules:\nkpatch_3_10_0_1062_1_1_1_4 [enabled]\nkpatch_3_10_0_1062_1_1_1_5 [enabled]\n\nInstalled patch modules:\nkpatch_3_10_0_1062_1_1_1_4 (3.10.0-1062.1.1.el7.x86_64)\nkpatch_3_10_0_1062_1_1_1_5 (3.10.0-1062.1.2.el7.x86_64)\n').strip()
BAD_OUTPUT1 = ''
BAD_OUTPUT2 = ('\nLoaded patch modules:\nkpatch_3_10_0_1062_1_1_1_4 [enabled]\nkpatch_3_10_0_1062_1_1_1_5\n\nInstalled patch modules:\nkpatch_3_10_0_1062_1_1_1_4 (3.10.0-1062.1.1.el7.x86_64)\n(3.10.0-1062.1.2.el7.x86_64)\n').strip()

def test_doc_examples():
    env = {'kpatchs': kpatch_list.KpatchList(context_wrap(NORMAL_OUTPUT))}
    failed, total = doctest.testmod(kpatch_list, globs=env)
    assert failed == 0


def test_kpatch_list():
    kpatchs = kpatch_list.KpatchList(context_wrap(MULTILINE_OUTPUT))
    assert len(kpatchs.loaded) > 0
    assert len(kpatchs.installed) > 0
    assert kpatchs.loaded.get('kpatch_3_10_0_1062_1_1_1_4') == 'enabled'
    assert kpatchs.installed.get('kpatch_3_10_0_1062_1_1_1_4') == '3.10.0-1062.1.1.el7.x86_64'
    assert kpatchs.loaded.get('kpatch_3_10_0_1062_1_1_1_5') == 'enabled'
    assert kpatchs.installed.get('kpatch_3_10_0_1062_1_1_1_5') == '3.10.0-1062.1.2.el7.x86_64'
    kpatchs = kpatch_list.KpatchList(context_wrap(BAD_OUTPUT2))
    assert len(kpatchs.loaded) == 2
    assert len(kpatchs.installed) == 1
    assert kpatchs.loaded.get('kpatch_3_10_0_1062_1_1_1_4') == 'enabled'
    assert kpatchs.installed.get('kpatch_3_10_0_1062_1_1_1_4') == '3.10.0-1062.1.1.el7.x86_64'
    assert kpatchs.loaded.get('kpatch_3_10_0_1062_1_1_1_5') == ''


def test_fail():
    with pytest.raises(SkipException) as (e):
        kpatch_list.KpatchList(context_wrap(BAD_OUTPUT1))
    assert 'No Data from command: /usr/sbin/kpatch list' in str(e)