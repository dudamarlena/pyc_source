# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/combiners/tests/test_user_namespaces.py
# Compiled at: 2019-05-16 13:41:33
from ..user_namespaces import UserNamespaces
from ...parsers.cmdline import CmdLine
from ...parsers.grub_conf import Grub2Config
from ...tests import context_wrap
ENABLE_TOK_A = ('\nuser_namespaces.enable=1\n').strip()
ENABLE_TOK_B = ('\nuser-namespaces.enable=1\n').strip()
CMDLINE = ('\nBOOT_IMAGE=/vmlinuz-3.10.0-514.6.1.el7.x86_64 root=/dev/mapper/rhel-root ro crashkernel=auto rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap {0}\n').strip()
GRUB2_CONF = "\n### BEGIN /etc/grub.d/10_linux ###\nmenuentry 'Red Hat Enterprise Linux Server (3.10.0-514.16.1.el7.x86_64) 7.3 (Maipo)' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-3.10.0-514.el7.x86_64-advanced-9727cab4-12c2-41a8-9527-9644df34e586' {{\n        load_video\n        set gfxpayload=keep\n        insmod gzio\n        insmod part_gpt\n        insmod xfs\n        set root='hd0,gpt2'\n        if [ x$feature_platform_search_hint = xy ]; then\n          search --no-floppy --fs-uuid --set=root --hint-bios=hd0,gpt2 --hint-efi=hd0,gpt2 --hint-baremetal=ahci0,gpt2  d80fa96c-ffa1-4894-9282-aeda37f0befe\n        else\n          search --no-floppy --fs-uuid --set=root d80fa96c-ffa1-4894-9282-aeda37f0befe\n        fi\n        linuxefi /vmlinuz-3.10.0-514.16.1.el7.x86_64 root=/dev/mapper/rhel-root ro rd.luks.uuid=luks-a40b320e-0711-4cd6-8f9e-ce32810e2a79 rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet LANG=en_US.UTF-8 {0}\n        initrdefi /initramfs-3.10.0-514.16.1.el7.x86_64.img\n}}\nmenuentry 'Red Hat Enterprise Linux Server (3.10.0-514.10.2.el7.x86_64) 7.3 (Maipo)' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-3.10.0-514.el7.x86_64-advanced-9727cab4-12c2-41a8-9527-9644df34e586' {{\n        load_video\n        set gfxpayload=keep\n        insmod gzio\n        insmod part_gpt\n        insmod xfs\n        set root='hd0,gpt2'\n        if [ x$feature_platform_search_hint = xy ]; then\n          search --no-floppy --fs-uuid --set=root --hint-bios=hd0,gpt2 --hint-efi=hd0,gpt2 --hint-baremetal=ahci0,gpt2  d80fa96c-ffa1-4894-9282-aeda37f0befe\n        else\n          search --no-floppy --fs-uuid --set=root d80fa96c-ffa1-4894-9282-aeda37f0befe\n        fi\n        linuxefi /vmlinuz-3.10.0-514.10.2.el7.x86_64 root=/dev/mapper/rhel-root ro rd.luks.uuid=luks-a40b320e-0711-4cd6-8f9e-ce32810e2a79 rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet LANG=en_US.UTF-8 {1}\n        initrdefi /initramfs-3.10.0-514.10.2.el7.x86_64.img\n}}\n"
MENUENTRY_0 = ("\n'Red Hat Enterprise Linux Server (3.10.0-514.16.1.el7.x86_64) 7.3 (Maipo)' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-3.10.0-514.el7.x86_64-advanced-9727cab4-12c2-41a8-9527-9644df34e586'\n").strip()
MENUENTRY_1 = ("\n'Red Hat Enterprise Linux Server (3.10.0-514.10.2.el7.x86_64) 7.3 (Maipo)' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-3.10.0-514.el7.x86_64-advanced-9727cab4-12c2-41a8-9527-9644df34e586'\n").strip()
CASES = [
 (
  (
   CMDLINE.format(''), None), (False, [])),
 (
  (
   CMDLINE.format(''), GRUB2_CONF.format('', '')), (False, [])),
 (
  (
   CMDLINE.format(''), GRUB2_CONF.format('', ENABLE_TOK_A)),
  (
   False, [MENUENTRY_1])),
 (
  (
   CMDLINE.format(ENABLE_TOK_A), None), (True, [])),
 (
  (
   CMDLINE.format(ENABLE_TOK_A), GRUB2_CONF.format('', '')),
  (
   True, [])),
 (
  (
   CMDLINE.format(ENABLE_TOK_A), GRUB2_CONF.format(ENABLE_TOK_A, '')),
  (
   True, [MENUENTRY_0])),
 (
  (
   CMDLINE.format(ENABLE_TOK_B), GRUB2_CONF.format(ENABLE_TOK_B, '')),
  (
   True, [MENUENTRY_0]))]

def test_integration():
    for case in CASES:
        context = {}
        context[CmdLine] = CmdLine(context_wrap(case[0][0]))
        if case[0][1] is not None:
            context[Grub2Config] = Grub2Config(context_wrap(case[0][1]))
        un = UserNamespaces(context.get(CmdLine), context.get(Grub2Config))
        assert un.enabled() == case[1][0]
        assert un.enabled_configs() == case[1][1]

    return