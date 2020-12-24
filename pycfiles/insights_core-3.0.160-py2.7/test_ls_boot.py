# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ls_boot.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.ls_boot import LsBoot
from insights.tests import context_wrap
LS_BOOT = '\n/boot:\ntotal 187380\ndr-xr-xr-x.  3 0 0     4096 Mar  4 16:19 .\ndr-xr-xr-x. 19 0 0     4096 Jul 14 09:10 ..\n-rw-r--r--.  1 0 0   123891 Aug 25  2015 config-3.10.0-229.14.1.el7.x86_64\ndrwxr-xr-x.  6 0 0      111 Jun 15 09:51 grub2\n\n/boot/grub2:\ntotal 36\ndrwxr-xr-x. 6 0 0  104 Mar  4 16:16 .\ndr-xr-xr-x. 3 0 0 4096 Mar  4 16:19 ..\nlrwxrwxrwx. 1 0 0   11 Aug  4  2014 menu.lst -> ./grub.cfg\n-rw-r--r--. 1 0 0   64 Sep 18  2015 device.map\n-rw-r--r--. 1 0 0 7040 Mar 29 13:30 grub.cfg\n'
LS_BOOT_LINKS = '\n/boot:\ntotal 187380\n-rw-------.  1 root root 19143244 Mar  3 14:31 initramfs-2.6.32-504.el6.x86_64.img\nlrwxrwxrwx.  1 root root       40 May 11 11:00 initrd -> initramfs-2.6.32-504.12.2.el6.x86_64.img\nlrwxrwxrwx.  1 root root       34 May 11 11:00 vmlinuz -> vmlinuz-2.6.32-504.12.2.el6.x86_64\n-rwxr-xr-x.  1 root root  4153904 Sep 16  2014 vmlinuz-2.6.32-504.el6.x86_64\n'

def test_ls_boot():
    ls_boot = LsBoot(context_wrap(LS_BOOT))
    assert '/boot' in ls_boot
    assert '/boot/grub2' in ls_boot
    assert ls_boot.dirs_of('/boot') == ['.', '..', 'grub2']
    grub2_files = ls_boot.files_of('/boot/grub2')
    assert 'menu.lst' in grub2_files
    assert 'device.map' in grub2_files
    assert 'grub.cfg' in grub2_files
    assert len(grub2_files) == 3
    boot_files = ls_boot.files_of('/boot')
    assert 'config-3.10.0-229.14.1.el7.x86_64' in boot_files
    assert len(boot_files) == 1


def test_boot_links():
    ls_boot = LsBoot(context_wrap(LS_BOOT_LINKS))
    boot_files = ls_boot.files_of('/boot')
    assert '/boot' in ls_boot
    assert 'initramfs-2.6.32-504.el6.x86_64.img' in boot_files
    assert 'initrd' in boot_files
    assert 'vmlinuz' in boot_files
    assert 'vmlinuz-2.6.32-504.el6.x86_64' in boot_files