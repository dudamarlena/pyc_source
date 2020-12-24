# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_dmsetup_info.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.dmsetup import DmsetupInfo
from insights.tests import context_wrap
DMSETUP_INFO_1 = ('\nName               Maj Min Stat Open Targ Event  UUID\nVG00-tmp           253   8 L--w    1    1      0 LVM-gy9uAwD7LuTIApplr2sogbOx5iS0FTax6lLmBji2ueSbX49gxcV76M29cmukQiw4\nVG00-var_tmp       253   4 L--w    1    1      0 LVM-gy9uAwD7LuTIApplr2sogbOx5iS0FTaxXOT2ZNHpEmJy2g2FpmXfAH1chG4Utm4Q\nVG00-home          253   3 L--w    1    1      0 LVM-gy9uAwD7LuTIApplr2sogbOx5iS0FTaxCqXOnbGe2zjhX923dFiIdl1oi7mO9tXp\nVG00-var_log       253   9 L--w    1    1      0 LVM-gy9uAwD7LuTIApplr2sogbOx5iS0FTaxlycWK5qprImfYnbkZLNiFZ5Lc6rJq04Z\nVG00-usr           253   2 L--w    1    1      0 LVM-gy9uAwD7LuTIApplr2sogbOx5iS0FTaxJqQ6DLofdR0uWkTnlpkRnFShO3PgqhCT\nVG00-var           253   6 L--w    1    2      0 LVM-gy9uAwD7LuTIApplr2sogbOx5iS0FTaxicvyvt67113nTb8vMlGfgdEjDx0LKT2O\nVG00-swap          253   1 L--w    2    1      0 LVM-gy9uAwD7LuTIApplr2sogbOx5iS0FTax3Ll2XhOYZkylx1CjOQi7G4yHgrIOsyqG\nVG00-root          253   0 L--w    1    1      0 LVM-gy9uAwD7LuTIApplr2sogbOx5iS0FTaxKpnAKYhrYMYMNMwjegkW965bUgtJFTRY\nVG00-var_log_audit 253   5 L--w    1    1      0 LVM-gy9uAwD7LuTIApplr2sogbOx5iS0FTaxwQ8R0XWJRm86QX3befq1cHRy47Von6ZW\nVG_DB-vol01        253  10 L--w    1    2      0 LVM-dgoBx4rat9aLu3sg1k95D7YwUT7YnFddgcZSaU2sjHZMVBlwcNwDjmmGGtfXeIZs\nVG00-opt           253   7 L--w    1    4      0 LVM-gy9uAwD7LuTIApplr2sogbOx5iS0FTaxIiCYm5hcvgQdXynPGBfHQLrtE3sqUKT2\n').strip()

def test_dmsetup_info():
    r = DmsetupInfo(context_wrap(DMSETUP_INFO_1))
    assert len(r) == 11
    assert len(r[0]) == 8
    assert r[0]['UUID'] == 'LVM-gy9uAwD7LuTIApplr2sogbOx5iS0FTax6lLmBji2ueSbX49gxcV76M29cmukQiw4'
    assert r[(-1)]['Stat'] == 'L--w'
    assert r.names == ['VG00-tmp', 'VG00-var_tmp', 'VG00-home', 'VG00-var_log',
     'VG00-usr', 'VG00-var', 'VG00-swap', 'VG00-root',
     'VG00-var_log_audit', 'VG_DB-vol01', 'VG00-opt']
    assert r.names == [ dm['Name'] for dm in r ]
    assert len(r.by_uuid) == 11