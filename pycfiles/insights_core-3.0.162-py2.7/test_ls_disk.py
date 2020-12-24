# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ls_disk.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.ls_disk import LsDisk
from insights.tests import context_wrap
LS_DISK = '\n/dev/disk/by-path:\ntotal 0\ndrwxr-xr-x. 2 0 0 160 Sep 19 10:15 .\ndrwxr-xr-x. 5 0 0 100 Sep 19 10:15 ..\nlrwxrwxrwx. 1 0 0   9 Sep 19 10:15 pci-0000:00:01.1-scsi-1:0:0:0 -> ../../sr0\nlrwxrwxrwx. 1 0 0   9 Sep 19 10:15 pci-0000:00:0d.0-scsi-0:0:0:0 -> ../../sda\nlrwxrwxrwx. 1 0 0  10 Sep 19 10:15 pci-0000:00:0d.0-scsi-0:0:0:0-part1 -> ../../sda1\nlrwxrwxrwx. 1 0 0  10 Sep 19 10:15 pci-0000:00:0d.0-scsi-0:0:0:0-part2 -> ../../sda2\nlrwxrwxrwx. 1 0 0   9 Sep 19 10:15 pci-0000:00:0d.0-scsi-1:0:0:0 -> ../../sdb\nlrwxrwxrwx. 1 0 0  10 Sep 19 10:15 pci-0000:00:0d.0-scsi-1:0:0:0-part1 -> ../../sdb\n\n/dev/disk/by-uuid:\ntotal 0\nlrwxrwxrwx. 1 root root 10 Sep 19 10:15 3ab50b34-d0b9-4518-9f21-05307d895f81 -> ../../dm-1\nlrwxrwxrwx. 1 root root 10 Sep 19 10:15 51c5cf12-a577-441e-89da-bc93a73a1ba3 -> ../../sda1\nlrwxrwxrwx. 1 root root 10 Sep 19 10:15 7b0068d4-1399-4ce7-a54a-3e2fc1232299 -> ../../dm-0\n\n/dev/disk/by-id:\ntotal 0\nlrwxrwxrwx. 1 root root  9 Sep 19 10:15 ata-VBOX_CD-ROM_VB2-01700376 -> ../../sr0\nlrwxrwxrwx. 1 root root  9 Sep 19 10:15 ata-VBOX_HARDDISK_VB4c56cb04-26932e6a -> ../../sdb\nlrwxrwxrwx. 1 root root 10 Sep 19 10:15 ata-VBOX_HARDDISK_VB4c56cb04-26932e6a-part1 -> ../../sdb1\nlrwxrwxrwx. 1 root root  9 Sep 19 10:15 ata-VBOX_HARDDISK_VBdb3eca59-6c439fb7 -> ../../sda\nlrwxrwxrwx. 1 root root 10 Sep 19 10:15 ata-VBOX_HARDDISK_VBdb3eca59-6c439fb7-part1 -> ../../sda1\nlrwxrwxrwx. 1 root root 10 Sep 19 10:15 ata-VBOX_HARDDISK_VBdb3eca59-6c439fb7-part2 -> ../../sda2\nlrwxrwxrwx. 1 root root 10 Sep 19 10:15 dm-name-vg_yizhangrhel6-lv_root -> ../../dm-0\nlrwxrwxrwx. 1 root root 10 Sep 19 10:15 dm-name-vg_yizhangrhel6-lv_swap -> ../../dm-1\nlrwxrwxrwx. 1 root root 10 Sep 19 10:15 dm-uuid-LVM-vT3Sj2vOtGXyChqSzGvmps0qezNWEO7MI7atvuhelVCBetzJ3QPpOlIDyXSIt6cw -> ../../dm-1\nlrwxrwxrwx. 1 root root 10 Sep 19 10:15 dm-uuid-LVM-vT3Sj2vOtGXyChqSzGvmps0qezNWEO7MlJOewBrdU3NOoolrIVn99sdXojq9qIxd -> ../../dm-0\nlrwxrwxrwx. 1 root root 10 Sep 19 10:15 lvm-pv-uuid-1lI8Ef-9H35-HVlP-1UdC-XlgD-eedv-SRjC0i -> ../../sda2\nlrwxrwxrwx. 1 root root  9 Sep 19 10:15 scsi-SATA_VBOX_HARDDISK_VB4c56cb04-26932e6a -> ../../sdb\nlrwxrwxrwx. 1 root root 10 Sep 19 10:15 scsi-SATA_VBOX_HARDDISK_VB4c56cb04-26932e6a-part1 -> ../../sdb1\nlrwxrwxrwx. 1 root root  9 Sep 19 10:15 scsi-SATA_VBOX_HARDDISK_VBdb3eca59-6c439fb7 -> ../../sda\nlrwxrwxrwx. 1 root root 10 Sep 19 10:15 scsi-SATA_VBOX_HARDDISK_VBdb3eca59-6c439fb7-part1 -> ../../sda1\nlrwxrwxrwx. 1 root root 10 Sep 19 10:15 scsi-SATA_VBOX_HARDDISK_VBdb3eca59-6c439fb7-part2 -> ../../sda2\n\n/dev/disk/by-label:\ntotal 0\nlrwxrwxrwx. 1 root root 9 Sep 18 11:20 RHEL-7.2 Server.x86_64 -> ../../sr0\n'
BY_DISK = '/dev/disk/by-path'

def test_ls_disk():
    ls_disk = LsDisk(context_wrap(LS_DISK))
    assert ls_disk.listing_of('/dev/disk/by-uuid') == {'7b0068d4-1399-4ce7-a54a-3e2fc1232299': {'group': 'root', 'name': '7b0068d4-1399-4ce7-a54a-3e2fc1232299', 'links': 1, 
                                                'perms': 'rwxrwxrwx.', 'dir': '/dev/disk/by-uuid', 'raw_entry': 'lrwxrwxrwx. 1 root root 10 Sep 19 10:15 7b0068d4-1399-4ce7-a54a-3e2fc1232299 -> ../../dm-0', 
                                                'owner': 'root', 
                                                'link': '../../dm-0', 'date': 'Sep 19 10:15', 'type': 'l', 
                                                'size': 10}, 
       '3ab50b34-d0b9-4518-9f21-05307d895f81': {'group': 'root', 'name': '3ab50b34-d0b9-4518-9f21-05307d895f81', 'links': 1, 
                                                'perms': 'rwxrwxrwx.', 'dir': '/dev/disk/by-uuid', 'raw_entry': 'lrwxrwxrwx. 1 root root 10 Sep 19 10:15 3ab50b34-d0b9-4518-9f21-05307d895f81 -> ../../dm-1', 
                                                'owner': 'root', 
                                                'link': '../../dm-1', 'date': 'Sep 19 10:15', 'type': 'l', 
                                                'size': 10}, 
       '51c5cf12-a577-441e-89da-bc93a73a1ba3': {'group': 'root', 'name': '51c5cf12-a577-441e-89da-bc93a73a1ba3', 'links': 1, 
                                                'perms': 'rwxrwxrwx.', 'dir': '/dev/disk/by-uuid', 'raw_entry': 'lrwxrwxrwx. 1 root root 10 Sep 19 10:15 51c5cf12-a577-441e-89da-bc93a73a1ba3 -> ../../sda1', 
                                                'owner': 'root', 
                                                'link': '../../sda1', 'date': 'Sep 19 10:15', 'type': 'l', 
                                                'size': 10}}
    assert ls_disk.listings.get('/dev/disk/by-uuid')['files'] == ['3ab50b34-d0b9-4518-9f21-05307d895f81',
     '51c5cf12-a577-441e-89da-bc93a73a1ba3',
     '7b0068d4-1399-4ce7-a54a-3e2fc1232299']
    assert ls_disk.listings.get('/dev/disk/by-uuid')['entries']['3ab50b34-d0b9-4518-9f21-05307d895f81']['link'] == '../../dm-1'