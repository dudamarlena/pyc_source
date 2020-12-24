# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sysconfig_chronyd.py
# Compiled at: 2019-05-16 13:41:33
from insights.tests import context_wrap
from insights.parsers.sysconfig import ChronydSysconfig
CHRONYD = ('\nOPTIONS="-d"\n#HIDE="me"\n').strip()

def test_sysconfig_chronyd():
    result = ChronydSysconfig(context_wrap(CHRONYD))
    assert result['OPTIONS'] == '-d'
    assert result.get('HIDE') is None
    return