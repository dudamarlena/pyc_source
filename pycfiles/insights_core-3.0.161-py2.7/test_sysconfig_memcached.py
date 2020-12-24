# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sysconfig_memcached.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.sysconfig import MemcachedSysconfig
from insights.tests import context_wrap
MEMCACHED_CONFIG = ('\nPORT="11211"\nUSER="memcached"\n# max connection 2048\nMAXCONN="2048"\n# set ram size to 2048 - 2GiB\nCACHESIZE="4096"\n# disable UDP and listen to loopback ip 127.0.0.1, for network connection use real ip e.g., 10.0.0.5\nOPTIONS="-U 0 -l 127.0.0.1"\n').strip()

def test_sysconfig_memcached():
    context = context_wrap(MEMCACHED_CONFIG, 'etc/sysconfig/memcached')
    conf = MemcachedSysconfig(context)
    assert 'OPTIONS' in conf
    assert 'FOO' not in conf
    assert conf.get('OPTIONS') == '-U 0 -l 127.0.0.1'
    assert conf.get('USER') == 'memcached'