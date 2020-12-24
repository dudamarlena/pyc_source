# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_mssql_conf.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import mssql_conf
from insights.tests import context_wrap
MSSQL_CONF = ('\n[sqlagent]\nenabled = false\n\n[EULA]\naccepteula = Y\n\n[memory]\nmemorylimitmb = 3328\n').strip()

def test_mssql_conf():
    conf = mssql_conf.MsSQLConf(context_wrap(MSSQL_CONF))
    assert conf.has_option('memory', 'memorylimitmb') is True
    assert conf.get('memory', 'memorylimitmb') == '3328'


def test_documentation():
    env = {'conf': mssql_conf.MsSQLConf(context_wrap(MSSQL_CONF))}
    failed_count, tests = doctest.testmod(mssql_conf, globs=env)
    assert failed_count == 0