# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_grub_conf_kdump.py
# Compiled at: 2019-11-14 13:57:46
from insights.parsers.grub_conf import Grub1Config, Grub2Config
from insights.tests import context_wrap
BAD_DEFAULT_1 = ('\n#boot=/dev/sda\n\ndefault=${last}\ntimeout=0\nsplashimage=(hd0,0)/grub/splash.xpm.gz\nhiddenmenu\ntitle Red Hat Enterprise Linux Server (2.6.32-431.11.2.el6.x86_64)\n        kernel /vmlinuz-2.6.32-431.11.2.el6.x86_64 crashkernel=128M@8M rhgb quiet\n').strip()
GOOD_OFFSET_4 = ('\n#boot=/dev/sda\n\ndefault=1\ntimeout=0\nsplashimage=(hd0,0)/grub/splash.xpm.gz\nhiddenmenu\ntitle Red Hat Enterprise Linux Server (2.6.32-431.17.1.el6.x86_64)\n        kernel /vmlinuz-2.6.32-431.17.1.el6.x86_64 crashkernel=  rhgb quiet\ntitle Red Hat Enterprise Linux Server (2.6.32-431.11.2.el6.x86_64)\n        kernel /vmlinuz-2.6.32-431.11.2.el6.x86_64 crashkernel=128M@32M rhgb quiet\n').strip()
GOOD_OFFSET_3 = ('\n#boot=/dev/sda\ndefault=1\ntimeout=0\nsplashimage=(hd0,0)/grub/splash.xpm.gz\nhiddenmenu\ntitle Red Hat Enterprise Linux Server (2.6.32-431.17.1.el6.x86_64)\n        kernel /vmlinuz-2.6.32-431.17.1.el6.x86_64 crashkernel=128M@0  rhgb quiet\ntitle Red Hat Enterprise Linux Server (2.6.32-431.11.2.el6.x86_64)\n        kernel /vmlinuz-2.6.32-431.11.2.el6.x86_64 crashkernel=128M@0 rhgb quiet\n').strip()
GOOD_OFFSET_2 = ('\n#boot=/dev/sda\n\ndefault=1\ntimeout=0\nsplashimage=(hd0,0)/grub/splash.xpm.gz\nhiddenmenu\ntitle Red Hat Enterprise Linux Server (2.6.32-431.17.1.el6.x86_64)\n        kernel /vmlinuz-2.6.32-431.17.1.el6.x86_64 crashkernel=128M@0M  rhgb quiet\ntitle Red Hat Enterprise Linux Server (2.6.32-431.11.2.el6.x86_64)\n        kernel /vmlinuz-2.6.32-431.11.2.el6.x86_64 crashkernel=128M@0M rhgb quiet\n').strip()
GOOD_OFFSET_1 = ('\n#boot=/dev/sda\ndefault=0\ntimeout=0\nsplashimage=(hd0,0)/grub/splash.xpm.gz\nhiddenmenu\ntitle Red Hat Enterprise Linux Server (2.6.32-431.17.1.el6.x86_64)\n        kernel /vmlinuz-2.6.32-431.17.1.el6.x86_64 crashkernel=128M rhgb quiet\ntitle Red Hat Enterprise Linux Server (2.6.32-431.11.2.el6.x86_64)\n        kernel /vmlinuz-2.6.32-431.11.2.el6.x86_64 crashkernel=128M rhgb quiet\n').strip()
BAD_OFFSET = ('\n#boot=/dev/sda\n\ndefault=1\ntimeout=0\nsplashimage=(hd0,0)/grub/splash.xpm.gz\nhiddenmenu\ntitle Red Hat Enterprise Linux Server (2.6.32-431.17.1.el6.x86_64)\n        kernel /vmlinuz-2.6.32-431.17.1.el6.x86_64 crashkernel=  rhgb quiet\ntitle Red Hat Enterprise Linux Server (2.6.32-431.11.2.el6.x86_64)\n        kernel /vmlinuz-2.6.32-431.11.2.el6.x86_64 crashkernel=128M@16M rhgb quiet\n').strip()
NOMATCH_MEMORY = ('\n#boot=/dev/sda\ndefault=1\ntimeout=0\nsplashimage=(hd0,0)/grub/splash.xpm.gz\nhiddenmenu\ntitle Red Hat Enterprise Linux Server (2.6.32-431.17.1.el6.x86_64)\n        kernel /vmlinuz-2.6.32-431.17.1.el6.x86_64 rhgb quiet\ntitle Red Hat Enterprise Linux Server (2.6.32-431.11.2.el6.x86_64)\n        kernel /vmlinuz-2.6.32-431.11.2.el6.x86_64 crashkernel=128M@M rhgb quiet\n').strip()
NOMATCH_CRASH_PARAM = ('\n#boot=/dev/sda\ndefault=1\ntimeout=0\nsplashimage=(hd0,0)/grub/splash.xpm.gz\nhiddenmenu\ntitle Red Hat Enterprise Linux Server (2.6.32-431.17.1.el6.x86_64)\n        kernel /vmlinuz-2.6.32-431.17.1.el6.x86_64 rhgb quiet\ntitle Red Hat Enterprise Linux Server (2.6.32-431.11.2.el6.x86_64)\n        kernel /vmlinuz-2.6.32-431.11.2.el6.x86_64 rhgb quiet\n').strip()
IOMMU_OFF = '\ntitle Red Hat Enterprise Linux Server (2.6.32-431.17.1.el6.x86_64)\n    kernel /vmlinuz-2.6.32-279.el6.x86_64 ro root=/dev/mapper/vg00-lv00 intel_iommu=off rd_LVM_LV=vg00/lv00 crashkernel=256M@16M\n'
IOMMU_MISSING = '\ntitle Red Hat Enterprise Linux Server (2.6.32-431.17.1.el6.x86_64)\n    kernel /vmlinuz-2.6.32-279.el6.x86_64 ro root=/dev/mapper/vg00-lv00 rd_LVM_LV=vg00/lv00 crashkernel=256M@16M\n'
IOMMU_ON = '\ntitle Red Hat Enterprise Linux Server (2.6.32-431.17.1.el6.x86_64)\n    kernel /vmlinuz-2.6.32-279.el6.x86_64 ro root=/dev/mapper/vg00-lv00 intel_iommu=on rd_LVM_LV=vg00/lv00 crashkernel=256M@16M\n'
IOMMU2_OFF = "\nmenuentry 'Red Hat Enterprise Linux Workstation (3.10.0-327.36.3.el7.x86_64) 7.2 (Maipo)' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-3.10.0-123.13.2.el7.x86_64-advanced-fbff9f50-62c3-484e-bca5-d53f672cda7c' {\n    linux16 /vmlinuz-3.10.0-327.36.3.el7.x86_64 root=/dev/RHEL7CSB/Root ro rd.lvm.lv=RHEL7CSB/Root rd.luks.uuid=luks-96c66446-77fd-4431-9508-f6912bd84194 intel_iommu=off crashkernel=128M@16M rd.lvm.lv=RHEL7CSB/Swap vconsole.font=latarcyrheb-sun16 rhgb quiet LANG=en_GB.utf8\n    initrd16 /initramfs-3.10.0-327.36.3.el7.x86_64.img\n}\n"
IOMMU2_MISSING = "\nmenuentry 'Red Hat Enterprise Linux Workstation (3.10.0-327.36.3.el7.x86_64) 7.2 (Maipo)' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-3.10.0-123.13.2.el7.x86_64-advanced-fbff9f50-62c3-484e-bca5-d53f672cda7c' {\n    linux16 /vmlinuz-3.10.0-327.36.3.el7.x86_64 root=/dev/RHEL7CSB/Root ro rd.lvm.lv=RHEL7CSB/Root rd.luks.uuid=luks-96c66446-77fd-4431-9508-f6912bd84194 crashkernel=128M@16M rd.lvm.lv=RHEL7CSB/Swap vconsole.font=latarcyrheb-sun16 rhgb quiet LANG=en_GB.utf8\n    initrd16 /initramfs-3.10.0-327.36.3.el7.x86_64.img\n}\n"
IOMMU2_ON = "\nmenuentry 'Red Hat Enterprise Linux Workstation (3.10.0-327.36.3.el7.x86_64) 7.2 (Maipo)' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-3.10.0-123.13.2.el7.x86_64-advanced-fbff9f50-62c3-484e-bca5-d53f672cda7c' {\n    linux16 /vmlinuz-3.10.0-327.36.3.el7.x86_64 root=/dev/RHEL7CSB/Root ro rd.lvm.lv=RHEL7CSB/Root rd.luks.uuid=luks-96c66446-77fd-4431-9508-f6912bd84194 intel_iommu=on crashkernel=128M@16M rd.lvm.lv=RHEL7CSB/Swap vconsole.font=latarcyrheb-sun16 rhgb quiet LANG=en_GB.utf8\n    initrd16 /initramfs-3.10.0-327.36.3.el7.x86_64.img\n}\n"
GRUB2_CONFIG = '\n### BEGIN /etc/grub.d/00_header ###\nset pager=1\n/\nif [ -s $prefix/grubenv ]; then\n  load_env\nfi\n#[...]\nif [ x"${feature_menuentry_id}" = xy ]; then\n  menuentry_id_option="--id"\nelse\n  menuentry_id_option=""\nfi\n#[...]\n### BEGIN /etc/grub.d/10_linux ###\nmenuentry \'Red Hat Enterprise Linux Workstation (3.10.0-327.36.3.el7.x86_64) 7.2 (Maipo)\' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option \'gnulinux-3.10.0-123.13.2.el7.x86_64-advanced-fbff9f50-62c3-484e-bca5-d53f672cda7c\' {\n    load_video\n    set gfxpayload=keep\n    insmod gzio\n    insmod part_msdos\n    insmod ext2\n    set root=\'hd0,msdos1\'\n    if [ x$feature_platform_search_hint = xy ]; then\n      search --no-floppy --fs-uuid --set=root --hint-bios=hd0,msdos1 --hint-efi=hd0,msdos1 --hint-baremetal=ahci0,msdos1 --hint=\'hd0,msdos1\'  1184ab74-77b5-4cfa-81d3-fb87b0457577\n    else\n      search --no-floppy --fs-uuid --set=root 1184ab74-77b5-4cfa-81d3-fb87b0457577\n    fi\n    linux16 /vmlinuz-3.10.0-327.36.3.el7.x86_64 root=/dev/RHEL7CSB/Root ro rd.lvm.lv=RHEL7CSB/Root rd.luks.uuid=luks-96c66446-77fd-4431-9508-f6912bd84194 crashkernel=128M@16M rd.lvm.lv=RHEL7CSB/Swap vconsole.font=latarcyrheb-sun16 rhgb quiet LANG=en_GB.utf8\n    initrd16 /initramfs-3.10.0-327.36.3.el7.x86_64.img\n}\nmenuentry \'Red Hat Enterprise Linux Workstation (3.10.0-267.el7.x86_64) 7.1 (Maipo)\' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option \'gnulinux-3.10.0-123.13.2.el7.x86_64-advanced-fbff9f50-62c3-484e-bca5-d53f672cda7c\' {\n    load_video\n    set gfxpayload=keep\n    insmod gzio\n    insmod part_msdos\n    insmod ext2\n    set root=\'hd0,msdos1\'\n    if [ x$feature_platform_search_hint = xy ]; then\n      search --no-floppy --fs-uuid --set=root --hint-bios=hd0,msdos1 --hint-efi=hd0,msdos1 --hint-baremetal=ahci0,msdos1 --hint=\'hd0,msdos1\'  1184ab74-77b5-4cfa-81d3-fb87b0457577\n    else\n      search --no-floppy --fs-uuid --set=root 1184ab74-77b5-4cfa-81d3-fb87b0457577\n    fi\n    linux16 /vmlinuz-3.10.0-267.el7.x86_64 root=/dev/RHEL7CSB/Root ro rd.lvm.lv=RHEL7CSB/Root rd.luks.uuid=luks-96c66446-77fd-4431-9508-f6912bd84194 crashkernel=auto  vconsole.keymap=us rd.lvm.lv=RHEL7CSB/Swap vconsole.font=latarcyrheb-sun16 rhgb quiet LANG=en_GB.utf8\n    initrd16 /initramfs-3.10.0-267.el7.x86_64.img\n}\nmenuentry \'Red Hat Enterprise Linux Workstation (3.10.0-230.el7synaptics.1186112.1186106.2.x86_64) 7.1 (Maipo)\' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option \'gnulinux-3.10.0-123.13.2.el7.x86_64-advanced-fbff9f50-62c3-484e-bca5-d53f672cda7c\' {\n    load_video\n    set gfxpayload=keep\n    insmod gzio\n    insmod part_msdos\n    insmod ext2\n    set root=\'hd0,msdos1\'\n    if [ x$feature_platform_search_hint = xy ]; then\n      search --no-floppy --fs-uuid --set=root --hint-bios=hd0,msdos1 --hint-efi=hd0,msdos1 --hint-baremetal=ahci0,msdos1 --hint=\'hd0,msdos1\'  1184ab74-77b5-4cfa-81d3-fb87b0457577\n    else\n      search --no-floppy --fs-uuid --set=root 1184ab74-77b5-4cfa-81d3-fb87b0457577\n    fi\n    linux16 /vmlinuz-3.10.0-230.el7synaptics.1186112.1186106.2.x86_64 root=/dev/RHEL7CSB/Root ro rd.lvm.lv=RHEL7CSB/Root rd.luks.uuid=luks-96c66446-77fd-4431-9508-f6912bd84194 crashkernel=auto  vconsole.keymap=us rd.lvm.lv=RHEL7CSB/Swap vconsole.font=latarcyrheb-sun16 rhgb quiet LANG=en_US.UTF-8\n    initrd16 /initramfs-3.10.0-230.el7synaptics.1186112.1186106.2.x86_64.img\n}\nmenuentry \'Red Hat Enterprise Linux Workstation, with Linux 0-rescue-71483baa33934d94a7804a398fed6241\' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option \'gnulinux-0-rescue-71483baa33934d94a7804a398fed6241-advanced-fbff9f50-62c3-484e-bca5-d53f672cda7c\' {\n    load_video\n    insmod gzio\n    insmod part_msdos\n    insmod ext2\n    set root=\'hd0,msdos1\'\n    if [ x$feature_platform_search_hint = xy ]; then\n      search --no-floppy --fs-uuid --set=root --hint-bios=hd0,msdos1 --hint-efi=hd0,msdos1 --hint-baremetal=ahci0,msdos1 --hint=\'hd0,msdos1\'  1184ab74-77b5-4cfa-81d3-fb87b0457577\n    else\n      search --no-floppy --fs-uuid --set=root 1184ab74-77b5-4cfa-81d3-fb87b0457577\n    fi\n    linux16 /vmlinuz-0-rescue-71483baa33934d94a7804a398fed6241 root=UUID=fbff9f50-62c3-484e-bca5-d53f672cda7c ro rd.lvm.lv=RHEL7CSB/Root rd.luks.uuid=luks-96c66446-77fd-4431-9508-f6912bd84194 crashkernel=auto  vconsole.keymap=us rd.lvm.lv=RHEL7CSB/Swap vconsole.font=latarcyrheb-sun16 rhgb quiet\n    initrd16 /initramfs-0-rescue-71483baa33934d94a7804a398fed6241.img\n}\n\n'
MODULE_TEST = '\n### BEGIN /etc/grub.d/00_header ###\nset pager=1\n/\nif [ -s $prefix/grubenv ]; then\n  load_env\nfi\n#[...]\nif [ x"${feature_menuentry_id}" = xy ]; then\n  menuentry_id_option="--id"\nelse\n  menuentry_id_option=""\nfi\n#[...]\n### BEGIN /etc/grub.d/10_linux ###\nmenuentry \'Red Hat Enterprise Linux Workstation (3.10.0-327.36.3.el7.x86_64) 7.2 (Maipo)\' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option \'gnulinux-3.10.0-123.13.2.el7.x86_64-advanced-fbff9f50-62c3-484e-bca5-d53f672cda7c\' {\n    load_video\n    set gfxpayload=keep\n    insmod gzio\n    insmod part_msdos\n    insmod ext2\n    set root=\'hd0,msdos1\'\n    if [ x$feature_platform_search_hint = xy ]; then\n      search --no-floppy --fs-uuid --set=root --hint-bios=hd0,msdos1 --hint-efi=hd0,msdosyy1 --hint-baremetal=ahci0,msdos1 --hint=\'hd0,msdos1\'  1184ab74-77b5-4cfa-81d3-fb87b0457577\n    else\n      search --no-floppy --fs-uuid --set=root 1184ab74-77b5-4cfa-81d3-fb87b0457577\n    fi\n    linux16 /vmlinuz-3.10.0-327.36.3.el7.x86_64 root=/dev/RHEL7CSB/Root ro rd.lvm.lv=RHEL7CSB/Root rd.luks.uuid=luks-96c66446-77fd-4431-9508-f6912bd84194 crashkernel=128M@16M rd.lvm.lv=RHEL7CSB/Swap vconsole.font=latarcyrheb-sun16 rhgb quiet LANG=en_GB.utf8\n    initrd16 /initramfs-3.10.0-327.36.3.el7.x86_64.img\n'

def test_mod_internal():
    config = Grub2Config(context_wrap(MODULE_TEST))
    assert config
    assert type(config.kernel_initrds) == dict
    assert 'grub_initrds' in config.kernel_initrds
    assert config.kernel_initrds['grub_initrds'] == ['initramfs-3.10.0-327.36.3.el7.x86_64.img']
    assert 'grub_kernels' in config.kernel_initrds
    assert config.kernel_initrds['grub_kernels'] == ['vmlinuz-3.10.0-327.36.3.el7.x86_64']


def test_kdump_iommu_enabled():
    assert Grub1Config(context_wrap(IOMMU_OFF)).is_kdump_iommu_enabled is False
    assert Grub1Config(context_wrap(IOMMU_MISSING)).is_kdump_iommu_enabled is False
    assert Grub1Config(context_wrap(IOMMU_ON)).is_kdump_iommu_enabled is True
    assert Grub2Config(context_wrap(IOMMU2_OFF)).is_kdump_iommu_enabled is False
    assert Grub2Config(context_wrap(IOMMU2_MISSING)).is_kdump_iommu_enabled is False
    assert Grub2Config(context_wrap(IOMMU2_ON)).is_kdump_iommu_enabled is True


def test_grub1_config():
    config = Grub1Config(context_wrap(GOOD_OFFSET_1))
    assert config
    assert 'configs' in config
    assert 'title' in config
    assert 'menuentry' not in config
    assert len(config['configs']) == 4
    assert config['configs']['default'] == ['0']
    assert config['configs']['timeout'] == ['0']
    assert config['configs']['splashimage'] == ['(hd0,0)/grub/splash.xpm.gz']
    assert config['configs']['hiddenmenu'] == ['']
    assert len(config['title']) == 2
    assert len(config['title'][0]) == 2
    assert config['title'][0]['title'] == 'Red Hat Enterprise Linux Server (2.6.32-431.17.1.el6.x86_64)'
    assert config['title'][0]['kernel'][0] == '/vmlinuz-2.6.32-431.17.1.el6.x86_64 crashkernel=128M rhgb quiet'
    assert len(config['title'][1]) == 2
    assert config['title'][1]['title'] == 'Red Hat Enterprise Linux Server (2.6.32-431.11.2.el6.x86_64)'
    assert config['title'][1]['kernel'][(-1)] == '/vmlinuz-2.6.32-431.11.2.el6.x86_64 crashkernel=128M rhgb quiet'
    assert config.is_kdump_iommu_enabled is False
    assert type(config.kernel_initrds) == dict
    assert 'grub_initrds' in config.kernel_initrds
    assert config.kernel_initrds['grub_initrds'] == []
    assert 'grub_kernels' in config.kernel_initrds
    assert config.kernel_initrds['grub_kernels'] == [
     'vmlinuz-2.6.32-431.17.1.el6.x86_64',
     'vmlinuz-2.6.32-431.11.2.el6.x86_64']


def test_grub2_config():
    config = Grub2Config(context_wrap(GRUB2_CONFIG))
    assert config
    assert 'configs' in config
    assert 'title' not in config
    assert 'menuentry' in config
    assert len(config['configs']) > 0
    assert len(config['menuentry']) == 4
    assert len(config['menuentry'][0]) == 6
    assert config['menuentry'][0]['menuentry'] == "'Red Hat Enterprise Linux Workstation (3.10.0-327.36.3.el7.x86_64) 7.2 (Maipo)' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-3.10.0-123.13.2.el7.x86_64-advanced-fbff9f50-62c3-484e-bca5-d53f672cda7c'"
    assert config['menuentry'][0]['load_video'] == ['']
    assert config['menuentry'][0]['initrd16'] == ['/initramfs-3.10.0-327.36.3.el7.x86_64.img']
    assert type(config.kernel_initrds) == dict
    assert 'grub_initrds' in config.kernel_initrds
    assert config.kernel_initrds['grub_initrds'] == [
     'initramfs-3.10.0-327.36.3.el7.x86_64.img',
     'initramfs-3.10.0-267.el7.x86_64.img',
     'initramfs-3.10.0-230.el7synaptics.1186112.1186106.2.x86_64.img',
     'initramfs-0-rescue-71483baa33934d94a7804a398fed6241.img']
    assert 'grub_kernels' in config.kernel_initrds
    assert config.kernel_initrds['grub_kernels'] == [
     'vmlinuz-3.10.0-327.36.3.el7.x86_64',
     'vmlinuz-3.10.0-267.el7.x86_64',
     'vmlinuz-3.10.0-230.el7synaptics.1186112.1186106.2.x86_64',
     'vmlinuz-0-rescue-71483baa33934d94a7804a398fed6241']