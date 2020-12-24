# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_limits_conf.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.limits_conf import LimitsConf
from insights.tests import context_wrap
LIMITS_CONF = ('\n#oracle soft nproc 2047\n#oracle hard nproc 16384\noracle soft nofile 1024\noracle hard nofile 65536\noracle soft stack 10240\noracle hard stack 3276\nroot       soft    nproc     unlimited\n').strip()
LIMITS_CONF_PATH = '/etc/security/limits.conf'
BAD_LIMITS_CONF = '\n\noracle\noracle soft\noracle soft nofile\nroot       soft    nproc     unlimitied\n'
FULL_OPTS_LIMITS_CONF = '\n# ** Domain variations **\n# 0: User domain\noracle      soft nofile 1024\n# 1: Group domain\n@dbadmins   soft nofile 1024\n# 2: Wildcard domain\n*           soft nofile 2048\n# 3: :maxuid - exact match\n:1001       soft nofile 3072\n# 4: minuid: - from that number up\n1000:       soft nofile 1536\n# 5: minuid:maxuid - range\n2000:2020   soft nofile 1600\n# 6: @:maxgid - exact match\n@:101       soft nofile 4096\n# 7: @mingid: - from that number up\n@100:       soft nofile 2560\n# 8: @minuid:maxuid - range\n@200:202    soft nofile 2800\n\n# ** Type variations **\n# 9: Hard type\noracle      hard nofile 8192\n# 10: Both types\nmanagers    -    nofile 10240\n'

def test_class_conf():
    ctx = context_wrap(LIMITS_CONF, path=LIMITS_CONF_PATH)
    data = LimitsConf(ctx)
    assert data.domains == sorted(['oracle', 'root'])


def test_class_bad():
    ctx = context_wrap(BAD_LIMITS_CONF, path=LIMITS_CONF_PATH)
    data = LimitsConf(ctx)
    assert data.domains == []
    bad_lines = BAD_LIMITS_CONF.strip().splitlines()
    assert data.bad_lines == bad_lines


def test_class_complete():
    ctx = context_wrap(FULL_OPTS_LIMITS_CONF, path=LIMITS_CONF_PATH)
    data = LimitsConf(ctx)
    assert data.domains == sorted([
     'oracle', '@dbadmins', '*', ':1001', '1000:', '2000:2020',
     '@:101', '@100:', '@200:202', 'managers'])
    assert data.rules[0] == {'domain': 'oracle', 'type': 'soft', 'item': 'nofile', 'value': 1024, 'file': LIMITS_CONF_PATH}
    assert data.find_all(domain='oracle') == [ data.rules[x] for x in [0, 2, 9] ]
    assert data.find_all(domain='@dbadmins') == [ data.rules[x] for x in [1, 2] ]
    assert data.find_all(domain=1001) == [ data.rules[x] for x in [2, 3, 4] ]
    assert data.find_all(domain=1002) == [ data.rules[x] for x in [2, 4] ]
    assert data.find_all(domain=2001) == [ data.rules[x] for x in [2, 4, 5] ]
    assert data.find_all(domain='@101') == [ data.rules[x] for x in [2, 6, 7] ]
    assert data.find_all(domain='@102') == [ data.rules[x] for x in [2, 7] ]
    assert data.find_all(domain='@201') == [ data.rules[x] for x in [2, 7, 8] ]
    assert data.find_all(type='soft') == [ data.rules[x] for x in [0, 1, 2, 3, 4, 5, 6, 7, 8, 10] ]
    assert data.find_all(type='hard') == [ data.rules[x] for x in [9, 10] ]
    assert data.find_all(domain='postgres', type='hard') == []
    assert data.find_all() == []