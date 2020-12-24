# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_grub_conf.py
# Compiled at: 2019-11-14 13:57:46
from insights.tests import context_wrap
from insights.parsers import grub_conf
from insights.parsers.grub_conf import Grub1Config, Grub2Config, Grub1EFIConfig
from insights.parsers.grub_conf import BootLoaderEntries
import pytest, doctest
GRUB2_CFG_1 = ('\nif [ -s $prefix/grubenv ]; then\n  load_env\nfi\n#[...]\nif [ x"${feature_menuentry_id}" = xy ]; then\n  menuentry_id_option="--id"\nelse\n  menuentry_id_option=""\nfi\n## BEGIN /etc/grub.d/10_linux ###\nmenuentry \'Red Hat Enterprise Linux Server, with Linux 3.10.0-123.9.3.el7.x86_64\' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option \'gnulinux-3.10.0-123.9.3.el7.x86_64-advanced-5a1c841f-5cfe-4d59-b3a0-4b788369d6cb\'\n   {load_video\n    set gfxpayload=keep\n    insmod part_msdos\n    set root=\'hd0,msdos1\'\n    if [ x$feature_platform_search_hint = xy ]; then\n      search --no-floppy --fs-uuid --set=root --hint-bios=hd0,msdos1 --hint-efi=hd0,msdos1 --hint-baremetal=ahci0,msdos1 --hint=\'hd0,msdos1\'  93f2c0dc-6201-4d26-a610-4b3998983ea2\n      if [ -s $prefix/grubenv ]; then\n        load_env\n      fi\n    else\n      search --no-floppy --fs-uuid --set=root 93f2c0dc-6201-4d26-a610-4b3998983ea2\n    fi\n    linux16 /vmlinuz-3.10.0-123.9.3.el7.x86_64 root=UUID=5a1c841f-5cfe-4d59-b3a0-4b788369d6cb ro crashkernel=auto  vconsole.font=latarcyrheb-sun16 console=ttyS0,38400 rd.lvm.lv=VG_RACS-CCP/lv-rootfs vconsole.keymap=us LANG=en_US.UTF-8\n    initrd16 /initramfs-3.10.0-123.9.3.el7.x86_64.img\n    insmod gzio}\nmenuentry \'Red Hat Enterprise Linux Server, with Linux 0-rescue-00c2fbfaa85544e48d6ca1d919fa2dd3\' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option \'gnulinux-0-rescue-00c2fbfaa85544e48d6ca1d919fa2dd3-advanced-5a1c841f-5cfe-4d59-b3a0-4b788369d6cb\'\n    {\n    insmod part_msdos\n    insmod ext2\n    set root=\'hd0,msdos1\'\n    if [ x$feature_platform_search_hint = xy ]; then\n      search --no-floppy --fs-uuid --set=root --hint-bios=hd0,msdos1 --hint-efi=hd0,msdos1 --hint-baremetal=ahci0,msdos1 --hint=\'hd0,msdos1\'  93f2c0dc-6201-4d26-a610-4b3998983ea2\n    else\n      search --no-floppy --fs-uuid --set=root 93f2c0dc-6201-4d26-a610-4b3998983ea2\n    fi\n    linux16 /vmlinuz-0-rescue-00c2fbfaa85544e48d6ca1d919fa2dd3 root=UUID=5a1c841f-5cfe-4d59-b3a0-4b788369d6cb ro crashkernel=auto  vconsole.font=latarcyrheb-sun16 console=ttyS0,38400 rd.lvm.lv=VG_RACS-CCP/lv-rootfs vconsole.keymap=us\n    initrd16 /initramfs-0-rescue-00c2fbfaa85544e48d6ca1d919fa2dd3.img\n}\n').strip()
GRUB2_CFG_2 = ("\n### BEGIN /etc/grub.d/10_linux ###\nmenuentry 'Red Hat Enterprise Linux Server (3.10.0-229.el7.x86_64) 7.0 (Maipo)' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-3.10.0-123.el7.x86_64-advanced-7f18fec3-a016-42ab-9bb9-6e7f6a5985ca' {\n    linux16 /vmlinuz-3.10.0-229.el7.x86_64 root=/dev/mapper/rhel-root ro rd.lvm.lv=rhel/root crashkernel=auto  rd.lvm.lv=rhel/swap vconsole.font=latarcyrheb-sun16 vconsole.keymap=us rhgb quiet LANG=en_AU.UTF-8\n    initrd16 /initramfs-3.10.0-229.el7.x86_64.img\n}\nmenuentry 'Red Hat Enterprise Linux Server (3.10.0-123.13.2.el7.x86_64) 7.0 (Maipo)' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-3.10.0-123.el7.x86_64-advanced-7f18fec3-a016-42ab-9bb9-6e7f6a5985ca' {\n    linux16 /vmlinuz-3.10.0-123.13.2.el7.x86_64 root=/dev/mapper/rhel-root ro rd.lvm.lv=rhel/root crashkernel=auto  rd.lvm.lv=rhel/swap vconsole.font=latarcyrheb-sun16 vconsole.keymap=us rhgb quiet LANG=en_AU.UTF-8\n    initrd16 /initramfs-3.10.0-123.13.2.el7.x86_64.img\n}\nmenuentry 'Red Hat Enterprise Linux Server, with Linux 3.10.0-123.el7.x86_64' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-3.10.0-123.el7.x86_64-advanced-7f18fec3-a016-42ab-9bb9-6e7f6a5985ca' {\n    linux16 /vmlinuz-3.10.0-123.el7.x86_64 root=UUID=7f18fec3-a016-42ab-9bb9-6e7f6a5985ca ro rd.lvm.lv=rhel/root crashkernel=auto  rd.lvm.lv=rhel/swap vconsole.font=latarcyrheb-sun16 vconsole.keymap=us rhgb quiet LANG=en_AU.UTF-8\n    initrd16 /initramfs-3.10.0-123.el7.x86_64.img\n}\nmenuentry 'Red Hat Enterprise Linux Server, with Linux 0-rescue-13798ffcbc1ed4374f3f2e0fa6c923ad' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-0-rescue-13798ffcbc1ed4374f3f2e0fa6c923ad-advanced-7f18fec3-a016-42ab-9bb9-6e7f6a5985ca' {\n    linux16 /vmlinuz-0-rescue-13798ffcbc1ed4374f3f2e0fa6c923ad root=UUID=7f18fec3-a016-42ab-9bb9-6e7f6a5985ca ro rd.lvm.lv=rhel/root crashkernel=auto  rd.lvm.lv=rhel/swap vconsole.font=latarcyrheb-sun16 vconsole.keymap=us rhgb quiet\n    initrd16 /initramfs-0-rescue-13798ffcbc1ed4374f3f2e0fa6c923ad.img\n}\n").strip()
GRUB1_CONF_3 = ('\n# grub.conf generated by anaconda\n#\n# Note that you do not have to rerun grub after making changes to this file\n# NOTICE:  You have a /boot partition.  This means that\n#          all kernel and initrd paths are relative to /boot/, eg.\n#          root (hd0,0)\n#          kernel /vmlinuz-version ro root=/dev/cciss/c0d0p3\n#          initrd /initrd-version.img\n#boot=/dev/cciss/c0d0\ndefault=1\n# fallback=0 # commented out by Proliant HBA install script\ntimeout=5\nsplashimage=(hd0,0)/grub/splash.xpm.gz\nhiddenmenu\ntitle Red Hat Enterprise Linux Server (2.6.18-194.8.1.el5)\n    root (hd0,0)\n    kernel /vmlinuz-2.6.18-194.8.1.el5 ro root=LABEL=/1 crashkernel=128M@16M\n    initrd /initrd-2.6.18-194.8.1.el5.img\n\ntitle Red Hat Enterprise Linux Server (2.6.18-194.17.1.el5)\n    root (hd0,0)\n    kernel /vmlinuz-2.6.18-194.17.1.el5 ro root=LABEL=/1 crashkernel=128M@16M\n    module /initramfs-2.6.18-194.8.1.el5.img\n').strip()
GRUB1_CONF_4 = ('\ndefault=a\ntitle (2.6.18-194.8.1.el5)\n    kernel /vmlinuz-2.6.18-194.8.1.el5 ro root=LABEL=/1 crashkernel=128M@16M\n    module /2.6.18-194.8.1.el5.img\n').strip()
GRUB1_CONF_5 = ('\ndefaults=0\ntitle (2.6.18-194.8.1.el5)\n    kernel\n    module /2.6.18-194.8.1.el5.img\n').strip()
GRUB1_CONF_6 = ('\ntitle Red Hat Enterprise Linux Server\n    kernel test\n    module /2.6.18-194.8.1.el5.img\n').strip()
GRUB1_CONF_7 = ('\ndefault = 1\ntitle Red Hat Enterprise Linux Server (2.6.18-194.8.1.el5)\n    kernel test\n    module /2.6.18-194.8.1.el5.img\n').strip()
GRUB1_CONF_8 = ('\ntitle Red Hat Enterprise Linux Server (2.6.18-194.8.1.el5)\n').strip()
GRUB2_CFG_3 = ("\nmenuentry 'Red Hat Enterprise Linux Server, with Linux 3.10.0-123.9.3.el7.x86_64' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-3.10.0-123.9.3.el7.x86_64-advanced-5a1c841f-5cfe-4d59-b3a0-4b788369d6cb' { load_video\n    set gfxpayload=keep\n    if [ x$feature_platform_search_hint = xy ]; then\n      search --no-floppy --fs-uuid --set=root --hint-bios=hd0,msdos1 --hint-efi=hd0,msdos1 --hint-baremetal=ahci0,msdos1 --hint='hd0,msdos1'  93f2c0dc-6201-4d26-a610-4b3998983ea2\n    else\n      search --no-floppy --fs-uuid --set=root 93f2c0dc-6201-4d26-a610-4b3998983ea2\n    fi\n    linux16 /vmlinuz-3.10.0-123.9.3.el7.x86_64 root=UUID=5a1c841f-5cfe-4d59-b3a0-4b788369d6cb ro crashkernel=auto  vconsole.font=latarcyrheb-sun16 console=ttyS0,38400 rd.lvm.lv=VG_RACS-CCP/lv-rootfs vconsole.keymap=us LANG=en_US.UTF-8\n    initrd16 /initramfs-3.10.0-123.9.3.el7.x86_64.img\n}\n").strip()
GRUB2_CFG_4 = ('\nmenuentry {\n    linux16 /vmlinuz-3.10.0-123.9.3.el7.x86_64 crashkernel=auto\n    initrd16 /initramfs-3.10.0-123.9.3.el7.x86_64.img\n}\n').strip()
BOOT_LOADER_ENTRIES_CONF = ('\ntitle Red Hat Enterprise Linux (4.18.0-80.1.2.el8_0.x86_64) 8.0 (Ootpa)\nversion 4.18.0-80.1.2.el8_0.x86_64\nlinux /vmlinuz-4.18.0-80.1.2.el8_0.x86_64\ninitrd /initramfs-4.18.0-80.1.2.el8_0.x86_64.img $tuned_initrd\noptions root=/dev/mapper/rhel_vm37--146-root ro crashkernel=auto resume=/dev/mapper/rhel_vm37--146-swap rd.lvm.lv=rhel_vm37-146/root rd.lvm.lv=rhel_vm37-146/swap $tuned_params noapic\nid rhel-20190428101407-4.18.0-80.1.2.el8_0.x86_64\ngrub_users $grub_users\ngrub_arg --unrestricted\ngrub_class kernel\n').strip()
GRUB1_CFG_1_DOC = ('\ndefault=0\ntimeout=0\nsplashimage=(hd0,0)/grub/splash.xpm.gz\nhiddenmenu\ntitle Red Hat Enterprise Linux Server (2.6.32-431.17.1.el6.x86_64)\n    kernel /vmlinuz-2.6.32-431.17.1.el6.x86_64 crashkernel=128M rhgb quiet\ntitle Red Hat Enterprise Linux Server (2.6.32-431.11.2.el6.x86_64)\n    kernel /vmlinuz-2.6.32-431.11.2.el6.x86_64 crashkernel=128M rhgb quiet\n').strip()
GRUB2_CFG_1_DOC = ('\n### BEGIN /etc/grub.d/00_header ###\nset pager=1\n/\nif [ -s $prefix/grubenv ]; then\n  load_env\nfi\n#[...]\nif [ x"${feature_menuentry_id}" = xy ]; then\n  menuentry_id_option="--id"\nelse\n  menuentry_id_option=""\nfi\n#[...]\n### BEGIN /etc/grub.d/10_linux ###\nmenuentry \'Red Hat Enterprise Linux Workstation (3.10.0-327.36.3.el7.x86_64) 7.2 (Maipo)\' $menuentry_id_option \'gnulinux-3.10.0-123.13.2.el7.x86_64-advanced-fbff9f50-62c3-484e-bca5-d53f672cda7c\' {\n    load_video\n    set gfxpayload=keep\n    insmod gzio\n    insmod part_msdos\n    insmod ext2\n    set root=\'hd0,msdos1\'\n    if [ x$feature_platform_search_hint = xy ]; then\n      search --no-floppy --fs-uuid --set=root --hint-bios=hd0,msdos1 --hint-efi=hd0,msdos1 --hint-baremetal=ahci0,msdos1 --hint=\'hd0,msdos1\'  1184ab74-77b5-4cfa-81d3-fb87b0457577\n    else\n      search --no-floppy --fs-uuid --set=root 1184ab74-77b5-4cfa-81d3-fb87b0457577\n    fi\n    linux16 /vmlinuz-3.10.0-327.36.3.el7.x86_64 root=/dev/RHEL7CSB/Root ro rd.lvm.lv=RHEL7CSB/Root rd.luks.uuid=luks-96c66446-77fd-4431-9508-f6912bd84194 crashkernel=128M@16M rd.lvm.lv=RHEL7CSB/Swap vconsole.font=latarcyrheb-sun16 rhgb quiet LANG=en_GB.utf8\n    initrd16 /initramfs-3.10.0-327.36.3.el7.x86_64.img\n}\n').strip()

def test_grub_conf_1():
    expected_result = {'grub_kernels': ['vmlinuz-2.6.18-194.8.1.el5', 'vmlinuz-2.6.18-194.17.1.el5'], 'grub_initrds': [
                      'initrd-2.6.18-194.8.1.el5.img', 'initramfs-2.6.18-194.8.1.el5.img']}
    assert expected_result == Grub1Config(context_wrap(GRUB1_CONF_3)).kernel_initrds
    expected_result = {'grub_kernels': ['vmlinuz-2.6.18-194.8.1.el5'], 'grub_initrds': []}
    grub1 = Grub1Config(context_wrap(GRUB1_CONF_4))
    assert grub1.is_kdump_iommu_enabled is False
    assert expected_result == grub1.kernel_initrds
    assert grub1.get_current_title() is None
    grub1 = Grub1Config(context_wrap(GRUB1_CONF_5))
    assert grub1.is_kdump_iommu_enabled is False
    assert grub1.get_current_title() == {'title': '(2.6.18-194.8.1.el5)', 
       'kernel': [
                ''], 
       'module': ['/2.6.18-194.8.1.el5.img']}
    grub1 = Grub1Config(context_wrap(GRUB1_CONF_6))
    assert grub1.is_kdump_iommu_enabled is False
    assert grub1.get_current_title() == {'title': 'Red Hat Enterprise Linux Server', 
       'kernel': [
                'test'], 
       'module': ['/2.6.18-194.8.1.el5.img']}
    grub1 = Grub1Config(context_wrap(GRUB1_CONF_7))
    assert grub1.is_kdump_iommu_enabled is False
    assert grub1.get_current_title() is None
    grub1 = Grub1Config(context_wrap(GRUB1_CONF_8))
    assert grub1.is_kdump_iommu_enabled is False
    grub1efi = Grub1EFIConfig(context_wrap(GRUB1_CONF_4))
    assert grub1efi.get_current_title() is None
    grub1efi = Grub1EFIConfig(context_wrap(GRUB1_CONF_5))
    assert grub1efi.get_current_title() == {'title': '(2.6.18-194.8.1.el5)', 
       'kernel': [
                ''], 
       'module': ['/2.6.18-194.8.1.el5.img']}
    grub1efi = Grub1EFIConfig(context_wrap(GRUB1_CONF_6))
    assert grub1efi.get_current_title() == {'title': 'Red Hat Enterprise Linux Server', 
       'kernel': [
                'test'], 
       'module': ['/2.6.18-194.8.1.el5.img']}
    grub1efi = Grub1EFIConfig(context_wrap(GRUB1_CONF_7))
    assert grub1efi.get_current_title() is None
    grub_conf = Grub2Config(context_wrap(GRUB2_CFG_1))['menuentry']
    assert 'load_video' in grub_conf[0]
    assert 'load_env' not in grub_conf[0]
    assert 'insmod' in grub_conf[0]
    expected_result = {'grub_kernels': ['vmlinuz-3.10.0-229.el7.x86_64', 'vmlinuz-3.10.0-123.13.2.el7.x86_64',
                      'vmlinuz-3.10.0-123.el7.x86_64', 'vmlinuz-0-rescue-13798ffcbc1ed4374f3f2e0fa6c923ad'], 
       'grub_initrds': [
                      'initramfs-3.10.0-229.el7.x86_64.img', 'initramfs-3.10.0-123.13.2.el7.x86_64.img',
                      'initramfs-3.10.0-123.el7.x86_64.img', 'initramfs-0-rescue-13798ffcbc1ed4374f3f2e0fa6c923ad.img']}
    assert expected_result == Grub2Config(context_wrap(GRUB2_CFG_2)).kernel_initrds
    grub_conf = Grub2Config(context_wrap(GRUB2_CFG_3))
    assert 'load_video' in grub_conf['menuentry'][0]
    assert grub_conf.is_kdump_iommu_enabled is False
    return


def test_grub2_boot_loader_entries():
    grub_ble = BootLoaderEntries(context_wrap(BOOT_LOADER_ENTRIES_CONF))
    assert grub_ble.title == 'Red Hat Enterprise Linux (4.18.0-80.1.2.el8_0.x86_64) 8.0 (Ootpa)'
    assert 'crashkernel=auto' in grub_ble.cmdline


def test_grub_conf_raise():
    with pytest.raises(Exception) as (e):
        Grub2Config(context_wrap(GRUB2_CFG_4))
    assert 'Cannot parse menuentry line: menuentry {' in str(e.value)


def test_grub_conf_doc():
    env = {'grub1_config': Grub1Config(context_wrap(GRUB1_CFG_1_DOC)), 
       'grub2_config': Grub2Config(context_wrap(GRUB2_CFG_1_DOC))}
    failed, total = doctest.testmod(grub_conf, globs=env)
    assert failed == 0