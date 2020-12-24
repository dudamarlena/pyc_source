# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_vgdisplay.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import vgdisplay
from insights.tests import context_wrap
VGDISPLAY = ("\nCouldn't find device with uuid VVLmw8-e2AA-ECfW-wDPl-Vnaa-0wW1-utv7tV.\n  There are 1 physical volumes missing.\n    Couldn't find device with uuid VVLmw8-e2AA-ECfW-wDPl-Vnaa-0wW1-utv7tV.\n  There are 1 physical volumes missing.\n  --- Volume group ---\n  VG Name               rhel_hp-dl160g8-3\n  Format                lvm2\n  System ID\n  Metadata Areas        1\n  Metadata Sequence No  5\n  VG Access             read/write\n  Total PE              119109\n  Alloc PE / Size       119098 / 465.23 GiB\n  Free  PE / Size       11 / 44.00 MiB\n  VG UUID               by0Dl3-0lpB-MxEz-f6GO-9LYO-YRAQ-GufNZD\n\n  VG Name               rhel_hp-dl260g7-4\n  Format                lvm2\n  System ID\n  VG Access             read/write\n  Alloc PE / Size       119098 / 465.23 GiB\n  Free  PE / Size       11 / 44.00 MiB\n  VG UUID               by0Dl3-0lpB-MxEz-f6GO-9LYO-YRAQ-GufNZN\n").strip()
VGDISPLAY_VV = '\n      Setting activation/monitoring to 1\n      Setting global/locking_type to 1\n      Setting global/wait_for_locks to 1\n      File-based locking selected.\n      Setting global/prioritise_write_locks to 1\n      Setting global/locking_dir to /run/lock/lvm\n      Setting global/use_lvmlockd to 0\n      Setting response to OK\n      Setting token to filter:3239235440\n      Setting daemon_pid to 856\n      Setting response to OK\n      Setting global_disable to 0\n      Setting response to OK\n      Setting response to OK\n      Setting response to OK\n      Setting name to RHEL7CSB\n      report/output_format not found in config: defaulting to basic\n      log/report_command_log not found in config: defaulting to 0\n      Processing VG RHEL7CSB aeMrAJ-QkAe-llvW-oAoE-CWLF-MnUd-edD1tI\n      Locking /run/lock/lvm/V_RHEL7CSB RB\n      Reading VG RHEL7CSB aeMrAJQkAellvWoAoECWLFMnUdedD1tI\n      Setting response to OK\n      Setting response to OK\n      Setting response to OK\n      Setting name to RHEL7CSB\n      Setting metadata/format to lvm2\n      Setting id to EfWV9V-03CX-E6zc-JkMw-yQae-wdzp-Je1KUn\n      Setting format to lvm2\n      Setting device to 64768\n      Setting dev_size to 970475520\n      Setting label_sector to 1\n      Setting ext_flags to 0\n      Setting ext_version to 1\n      Setting size to 1044480\n      Setting start to 4096\n      Setting ignore to 0\n      Setting response to OK\n      Setting response to OK\n      Setting response to OK\n      /dev/mapper/luks-96c66446-77fd-4431-9508-f6912bd84194: size is 970475520 sectors\n      Process single VG RHEL7CSB\n  --- Volume group ---\n  VG Name               RHEL7CSB\n  System ID\n  Format                lvm2\n  Metadata Areas        1\n  Metadata Sequence No  13\n  VG Access             read/write\n  VG Status             resizable\n  MAX LV                0\n  Cur LV                7\n  Open LV               6\n  Max PV                0\n  Cur PV                2\n  Act PV                1\n  VG Size               462.76 GiB\n  PE Size               4.00 MiB\n  Total PE              118466\n  Alloc PE / Size       114430 / 446.99 GiB\n  Free  PE / Size       4036 / 15.77 GiB\n  VG UUID               aeMrAJ-QkAe-llvW-oAoE-CWLF-MnUd-edD1tI\n\n      Adding RHEL7CSB/Home to the list of LVs to be processed.\n      Adding RHEL7CSB/Root to the list of LVs to be processed.\n      Adding RHEL7CSB/Swap to the list of LVs to be processed.\n      Adding RHEL7CSB/VMs_lv to the list of LVs to be processed.\n      Adding RHEL7CSB/NotBackedUp_lv to the list of LVs to be processed.\n      Adding RHEL7CSB/ISOs_lv to the list of LVs to be processed.\n      Adding RHEL7CSB/RHEL6-pg-pgsql-lv to the list of LVs to be processed.\n      Processing LV Home in VG RHEL7CSB.\n  --- Logical volume ---\n      global/lvdisplay_shows_full_device_path not found in config: defaulting to 0\n  LV Path                /dev/RHEL7CSB/Home\n  LV Name                Home\n  VG Name                RHEL7CSB\n  LV UUID                IdRMoU-JorV-ChPg-F1zb-6np9-yc08-qxj08f\n  LV Write Access        read/write\n  LV Creation host, time localhost, 2015-04-16 00:02:47 +1000\n  LV Status              available\n  # open                 1\n  LV Size                100.00 GiB\n  Current LE             25600\n  Segments               1\n  Allocation             inherit\n  Read ahead sectors     auto\n  - currently set to     256\n  Block device           253:3\n\n      Processing LV Root in VG RHEL7CSB.\n  --- Logical volume ---\n      global/lvdisplay_shows_full_device_path not found in config: defaulting to 0\n  LV Path                /dev/RHEL7CSB/Root\n  LV Name                Root\n  VG Name                RHEL7CSB\n  LV UUID                lXBbNv-u1r6-qCo1-682K-w5hW-ED8A-Sl4gvf\n  LV Write Access        read/write\n  LV Creation host, time localhost, 2015-04-16 00:02:50 +1000\n  LV Status              available\n  # open                 1\n  LV Size                29.30 GiB\n  Current LE             7500\n  Segments               1\n  Allocation             inherit\n  Read ahead sectors     auto\n  - currently set to     256\n  Block device           253:1\n\n      Processing LV Swap in VG RHEL7CSB.\n  --- Logical volume ---\n      global/lvdisplay_shows_full_device_path not found in config: defaulting to 0\n  LV Path                /dev/RHEL7CSB/Swap\n  LV Name                Swap\n  VG Name                RHEL7CSB\n  LV UUID                R2ErFM-Rrql-L0tH-VIbm-F0Km-P7uW-4hk3rl\n  LV Write Access        read/write\n  LV Creation host, time localhost, 2015-04-15 14:02:52 +1000\n  LV Status              available\n  # open                 2\n  LV Size                7.70 GiB\n  Current LE             1970\n  Segments               1\n  Allocation             inherit\n  Read ahead sectors     auto\n  - currently set to     256\n  Block device           253:2\n\n      Processing LV VMs_lv in VG RHEL7CSB.\n  --- Logical volume ---\n      global/lvdisplay_shows_full_device_path not found in config: defaulting to 0\n  LV Path                /dev/RHEL7CSB/VMs_lv\n  LV Name                VMs_lv\n  VG Name                RHEL7CSB\n  LV UUID                iXOy1p-wczA-WEEy-mawN-EPOh-YZGy-KIpTls\n  LV Write Access        read/write\n  LV Creation host, time localhost.localdomain, 2015-04-15 15:52:53 +1000\n  LV Status              available\n  # open                 1\n  LV Size                120.00 GiB\n  Current LE             30720\n  Segments               2\n  Allocation             inherit\n  Read ahead sectors     auto\n  - currently set to     256\n  Block device           253:4\n\n      Processing LV NotBackedUp_lv in VG RHEL7CSB.\n  --- Logical volume ---\n      global/lvdisplay_shows_full_device_path not found in config: defaulting to 0\n  LV Path                /dev/RHEL7CSB/NotBackedUp_lv\n  LV Name                NotBackedUp_lv\n  VG Name                RHEL7CSB\n  LV UUID                8SI5e4-O5uA-TbNC-bZeY-1WPg-Zf3P-H63Xsi\n  LV Write Access        read/write\n  LV Creation host, time pwayper.remote.csb, 2015-04-15 16:30:00 +1000\n  LV Status              available\n  # open                 1\n  LV Size                100.00 GiB\n  Current LE             25600\n  Segments               1\n  Allocation             inherit\n  Read ahead sectors     auto\n  - currently set to     256\n  Block device           253:5\n\n      Processing LV ISOs_lv in VG RHEL7CSB.\n  --- Logical volume ---\n      global/lvdisplay_shows_full_device_path not found in config: defaulting to 0\n  LV Path                /dev/RHEL7CSB/ISOs_lv\n  LV Name                ISOs_lv\n  VG Name                RHEL7CSB\n  LV UUID                YVI2nw-7LOu-mseA-vQkC-HpcK-Xabx-WK23yM\n  LV Write Access        read/write\n  LV Creation host, time pwayper.remote.csb, 2015-04-15 16:30:52 +1000\n  LV Status              available\n  # open                 1\n  LV Size                50.00 GiB\n  Current LE             12800\n  Segments               1\n  Allocation             inherit\n  Read ahead sectors     auto\n  - currently set to     256\n  Block device           253:6\n\n      Processing LV RHEL6-pg-pgsql-lv in VG RHEL7CSB.\n  --- Logical volume ---\n      global/lvdisplay_shows_full_device_path not found in config: defaulting to 0\n  LV Path                /dev/RHEL7CSB/RHEL6-pg-pgsql-lv\n  LV Name                RHEL6-pg-pgsql-lv\n  VG Name                RHEL7CSB\n  LV UUID                USkJVW-ALIP-kcpt-Av5e-Vf2u-GqXr-1VXhb1\n  LV Write Access        read/write\n  LV Creation host, time pwayper.remote.csb, 2015-04-19 15:36:34 +1000\n  LV Status              available\n  # open                 0\n  LV Size                40.00 GiB\n  Current LE             10240\n  Segments               1\n  Allocation             inherit\n  Read ahead sectors     auto\n  - currently set to     256\n  Block device           253:7\n\n  --- Physical volumes ---\n  PV Name               /dev/mapper/luks-96c66446-77fd-4431-9508-f6912bd84194\n  PV UUID               EfWV9V-03CX-E6zc-JkMw-yQae-wdzp-Je1KUn\n  PV Status             allocatable\n  Total PE / Free PE    118466 / 4036\n\n  PV Name               /dev/sde\n  PV UUID               bh4MbE-USrx-6Xd0-3biH-8v5o-Ztzn-XvKUkX\n  PV Status             allocatable\n  Total PE / Free PE    715396 / 212932\n\n      Unlocking /run/lock/lvm/V_RHEL7CSB\n      Setting global/notify_dbus to 1\n'

class TestVGdisplay:

    def test_VgDisplay(self):
        vg_info = vgdisplay.VgDisplay(context_wrap(VGDISPLAY))
        assert hasattr(vg_info, 'vg_list')
        assert vg_info.vg_list[0].get('VG Name') == 'rhel_hp-dl160g8-3'
        assert vg_info.vg_list[0].get('Metadata Sequence No') == '5'
        assert vg_info.vg_list[1].get('VG UUID') == 'by0Dl3-0lpB-MxEz-f6GO-9LYO-YRAQ-GufNZN'
        assert hasattr(vg_info, 'debug_info')
        assert vg_info.debug_info[0] == "Couldn't find device with uuid VVLmw8-e2AA-ECfW-wDPl-Vnaa-0wW1-utv7tV."
        assert vg_info.debug_info[1] == 'There are 1 physical volumes missing.'

    def test_vgdisplay_vv(self):
        vg_info = vgdisplay.VgDisplay(context_wrap(VGDISPLAY_VV))
        assert hasattr(vg_info, 'vg_list')
        vgdata = vg_info.vg_list
        assert isinstance(vgdata, list)
        assert len(vgdata) == 1
        vg = vgdata[0]
        assert isinstance(vg, dict)
        assert sorted(vg.keys()) == sorted([
         'VG Name', 'Format', 'Metadata Areas', 'Metadata Sequence No',
         'VG Access', 'VG Status', 'MAX LV', 'Cur LV', 'Open LV',
         'Max PV', 'Cur PV', 'Act PV', 'VG Size', 'PE Size', 'Total PE',
         'Alloc PE / Size', 'Free  PE / Size', 'VG UUID',
         'Logical Volumes', 'Physical Volumes'])
        assert vg['VG Name'] == 'RHEL7CSB'
        assert vg['Format'] == 'lvm2'
        assert vg['Metadata Areas'] == '1'
        assert vg['Metadata Sequence No'] == '13'
        assert vg['VG Access'] == 'read/write'
        assert vg['VG Status'] == 'resizable'
        assert vg['MAX LV'] == '0'
        assert vg['Cur LV'] == '7'
        assert vg['Open LV'] == '6'
        assert vg['Max PV'] == '0'
        assert vg['Cur PV'] == '2'
        assert vg['Act PV'] == '1'
        assert vg['VG Size'] == '462.76 GiB'
        assert vg['PE Size'] == '4.00 MiB'
        assert vg['Total PE'] == '118466'
        assert vg['Alloc PE / Size'] == '114430 / 446.99 GiB'
        assert vg['Free  PE / Size'] == '4036 / 15.77 GiB'
        assert vg['VG UUID'] == 'aeMrAJ-QkAe-llvW-oAoE-CWLF-MnUd-edD1tI'
        assert isinstance(vg['Logical Volumes'], dict)
        assert len(vg['Logical Volumes']) == 7
        assert sorted(vg['Logical Volumes'].keys()) == sorted([
         '/dev/RHEL7CSB/Home', '/dev/RHEL7CSB/ISOs_lv',
         '/dev/RHEL7CSB/NotBackedUp_lv', '/dev/RHEL7CSB/RHEL6-pg-pgsql-lv',
         '/dev/RHEL7CSB/Root', '/dev/RHEL7CSB/Swap', '/dev/RHEL7CSB/VMs_lv'])
        lvhome = vg['Logical Volumes']['/dev/RHEL7CSB/Home']
        assert isinstance(lvhome, dict)
        assert sorted(lvhome.keys()) == sorted([
         'LV Path', 'LV Name', 'VG Name', 'LV UUID', 'LV Write Access',
         'LV Creation host, time', 'LV Status', '# open', 'LV Size',
         'Current LE', 'Segments', 'Allocation', 'Read ahead sectors',
         '- currently set to', 'Block device'])
        assert lvhome['LV Path'] == '/dev/RHEL7CSB/Home'
        assert lvhome['LV Name'] == 'Home'
        assert lvhome['VG Name'] == 'RHEL7CSB'
        assert lvhome['LV UUID'] == 'IdRMoU-JorV-ChPg-F1zb-6np9-yc08-qxj08f'
        assert lvhome['LV Write Access'] == 'read/write'
        assert lvhome['LV Creation host, time'] == 'localhost, 2015-04-16 00:02:47 +1000'
        assert lvhome['LV Status'] == 'available'
        assert lvhome['# open'] == '1'
        assert lvhome['LV Size'] == '100.00 GiB'
        assert lvhome['Current LE'] == '25600'
        assert lvhome['Segments'] == '1'
        assert lvhome['Allocation'] == 'inherit'
        assert lvhome['Read ahead sectors'] == 'auto'
        assert lvhome['- currently set to'] == '256'
        assert lvhome['Block device'] == '253:3'
        assert isinstance(vg['Physical Volumes'], dict)
        assert len(vg['Physical Volumes']) == 2
        assert '/dev/mapper/luks-96c66446-77fd-4431-9508-f6912bd84194' in vg['Physical Volumes']
        pvluks = vg['Physical Volumes']['/dev/mapper/luks-96c66446-77fd-4431-9508-f6912bd84194']
        assert sorted(pvluks.keys()) == sorted([
         'PV Name', 'PV UUID', 'PV Status', 'Total PE / Free PE'])
        assert pvluks['PV Name'] == '/dev/mapper/luks-96c66446-77fd-4431-9508-f6912bd84194'
        assert pvluks['PV UUID'] == 'EfWV9V-03CX-E6zc-JkMw-yQae-wdzp-Je1KUn'
        assert pvluks['PV Status'] == 'allocatable'
        assert pvluks['Total PE / Free PE'] == '118466 / 4036'
        assert hasattr(vg_info, 'debug_info')
        assert isinstance(vg_info.debug_info, list)
        assert vg_info.debug_info == []