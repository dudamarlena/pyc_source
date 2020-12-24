# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sysconfig_mongod.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.sysconfig import MongodSysconfig
from insights.tests import context_wrap
SYSCONFIG_MONGOD = '\nOPTIONS="--quiet -f /etc/mongod.conf"\nOPTIONS_EMPTY=""\n'

def test_sysconfig_mongod():
    context = context_wrap(SYSCONFIG_MONGOD, 'etc/sysconfig/mongod')
    sysconf = MongodSysconfig(context)
    assert 'OPTIONS' in sysconf
    assert sysconf.get('OPTIONS') == '--quiet -f /etc/mongod.conf'
    assert sysconf.get('OPTIONS_EMPTY') == ''
    assert sysconf.get('not_exist') is None
    return