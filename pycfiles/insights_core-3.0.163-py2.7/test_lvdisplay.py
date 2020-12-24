# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_lvdisplay.py
# Compiled at: 2019-05-16 13:41:33
from insights.tests import context_wrap
from insights.parsers.lvdisplay import LvDisplay
LV_DISPLAY = '\n      Adding lvsapp01ap01:0 as an user of lvsapp01ap01_mlog\n  --- Volume group ---\n  VG Name               vgp01app\n  Format                lvm2\n  Metadata Areas        4\n  Metadata Sequence No  56\n  VG Access             read/write\n  VG Status             resizable\n  Clustered             yes\n  Shared                no\n  MAX LV                0\n  Cur LV                4\n  Open LV               1\n  Max PV                0\n  Cur PV                4\n  Act PV                4\n  VG Size               399.98 GiB\n  PE Size               4.00 MiB\n  Total PE              102396\n  Alloc PE / Size       82435 / 322.01 GiB\n  Free  PE / Size       19961 / 77.97 GiB\n  VG UUID               JVgCxE-UY84-C0Gk-8Cmn-UGXu-UHo0-9Qa4Re\n\n  --- Logical volume ---\n      global/lvdisplay_shows_full_device_path not found in config: defaulting to 0\n  LV Path                /dev/vgp01app/lvsapp01ap01-old\n  LV Name                lvsapp01ap01-old\n  VG Name                vgp01app\n  LV UUID                eLjsoG-Gvnh-zEbV-zFwD-HyQT-1zEs-VN4W2D\n  LV Write Access        read/write\n  LV Creation host, time lvn-itm-099, 2015-02-24 09:19:54 +0100\n  LV Status              available\n  # open                 0\n  LV Size                64.00 GiB\n  Current LE             16384\n  Segments               4\n  Allocation             inherit\n  Read ahead sectors     auto\n  - currently set to     256\n  Block device           253:50\n\n  --- Logical volume ---\n      global/lvdisplay_shows_full_device_path not found in config: defaulting to 0\n  LV Path                /dev/vgp01app/lvsapp01ap02\n  LV Name                lvsapp01ap02\n  VG Name                vgp01app\n  LV UUID                tFGsSW-nimQ-4JUL-4Fw0-IJn0-Jcoo-Szgfgz\n  LV Write Access        read/write\n  LV Creation host, time lvn-itm-099, 2015-02-24 15:24:52 +0100\n  LV Status              available\n  # open                 0\n  LV Size                64.00 GiB\n  Current LE             16384\n  Mirrored volumes       2\n  Segments               1\n  Allocation             inherit\n  Read ahead sectors     auto\n  - currently set to     256\n  Block device           253:54\n'

def test_lvdisplay():
    lvs = LvDisplay(context_wrap(LV_DISPLAY))
    assert 'vgp01app' == lvs.get('volumes')['Volume group'][0]['VG Name']
    assert '399.98 GiB' == lvs.get('volumes')['Volume group'][0]['VG Size']
    assert 'vgp01app' == lvs.get('volumes')['Logical volume'][1]['VG Name']
    assert 'vgp01app' in lvs.vgs
    assert lvs.vgs['vgp01app'] == lvs.get('volumes')['Volume group'][0]
    assert 'lvsapp01ap02' in lvs.lvs
    assert lvs.lvs['lvsapp01ap02'] == lvs.get('volumes')['Logical volume'][1]