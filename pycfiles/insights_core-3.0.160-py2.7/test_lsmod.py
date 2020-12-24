# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_lsmod.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import lsmod
from insights.tests import context_wrap
LSMODINFO = ('\nModule                  Size  Used by\nxt_CHECKSUM            12549  1\nipt_MASQUERADE         12678  3\nnf_nat_masquerade_ipv4    13412  1 ipt_MASQUERADE\ntun                    27141  3\nip6t_rpfilter          12546  1\nip6t_REJECT            12939  2\nipt_REJECT             12541  4\nxt_conntrack           12760  12\nebtable_nat            12807  0\nebtable_broute         12731  0\nbridge                119560  1 ebtable_broute\nstp                    12976  1 bridge\nllc                    14552  2 stp,bridge\nebtable_filter         12827  0\nebtables               30913  3 ebtable_broute,ebtable_nat,ebtable_filter\nip6table_nat           12864  1\n').strip()

def test_get_modules_info():
    mod_dict = lsmod.LsMod(context_wrap(LSMODINFO))
    assert len(mod_dict.data) == 16
    assert 'xt_CHECKSUM' in mod_dict
    assert mod_dict['tun'].get('depnum') == '3'
    assert mod_dict['llc'].get('deplist') == 'stp,bridge'
    assert mod_dict['ip6table_nat'].get('size') == '12864'