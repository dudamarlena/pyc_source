# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/combiners/tests/test_ipv6.py
# Compiled at: 2019-05-16 13:41:33
from ..ipv6 import IPv6
from ...parsers.modprobe import ModProbe
from ...parsers.lsmod import LsMod
from ...parsers.cmdline import CmdLine
from ...parsers.sysctl import Sysctl
from ...parsers.uname import Uname
from ...tests import context_wrap
from collections import namedtuple
Case = namedtuple('Case', ['cmdline', 'lsmod', 'modprobe', 'sysctl'])
UNAME_RHEL7 = '\nLinux localhost.localdomain 3.10.0-514.6.1.el7.x86_64 #1 SMP Sat Dec 10 11:15:38 EST 2016 x86_64 x86_64 x86_64 GNU/Linux\n'
UNAME_RHEL6 = '\nLinux localhost.localdomain 2.6.32-642.el6.x86_64 #1 SMP Wed Apr 13 00:51:26 EDT 2016 x86_64 x86_64 x86_64 GNU/Linux\n'
CMDLINE_DISABLED = '\nBOOT_IMAGE=/vmlinuz-3.10.0-514.6.1.el7.x86_64 root=/dev/mapper/rhel-root ro crashkernel=auto rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap ipv6.disable=1\n'
CMDLINE_NOT_DISABLED = '\nBOOT_IMAGE=/vmlinuz-3.10.0-514.6.1.el7.x86_64 root=/dev/mapper/rhel-root ro crashkernel=auto rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap\n'
CMDLINE_RHEL6_DISABLED = '\nro root=/dev/mapper/VolGroup-lv_root rd_NO_LUKS LANG=en_US.UTF-8 rd_NO_MD rd_LVM_LV=VolGroup/lv_swap SYSFONT=latarcyrheb-sun16  rd_LVM_LV=VolGroup/lv_root  KEYBOARDTYPE=pc KEYTABLE=us rd_NO_DM rhgb quiet ipv6.disable=1\n'
LSMOD_LOADED = '\nModule                  Size  Used by\nvboxsf                 37955  1 \nipv6                  336282  12 \ni2c_piix4              11232  0 \ni2c_core               29132  1 i2c_piix4\nsnd_intel8x0           30524  0 \n'
LSMOD_NOT_LOADED = '\nModule                  Size  Used by\nvboxsf                 37955  1 \ni2c_piix4              11232  0 \ni2c_core               29132  1 i2c_piix4\nsnd_intel8x0           30524  0 \n'
MODPROBE_NOT_DISABLED = '\n# framebuffer drivers\nblacklist aty128fb\nblacklist atyfb\nblacklist radeonfb\nblacklist i810fb\nblacklist cirrusfb\nblacklist intelfb\n'
MODPROBE_DISABLED = '\nblacklist radeonfb\nblacklist i810fb\nblacklist cirrusfb\nblacklist intelfb\noptions ipv6 disable=1\n'
MODPROBE_FAKE = '\nblacklist radeonfb\nblacklist i810fb\nblacklist cirrusfb\nblacklist intelfb\ninstall ipv6 /bin/true\ninstall blarfl /bin/true\n'
MODPROBE_FAKE_COMMENTED = '\nblacklist radeonfb\nblacklist i810fb\nblacklist cirrusfb\nblacklist intelfb\n# install ipv6 /bin/true\n'
SYSCTL_DISABLED = '\nnet.ipv6.conf.all.disable_ipv6 = 1\n'
SYSCTL_NOT_DISABLED = '\nnet.ipv6.route.gc_elasticity = 9\nnet.ipv6.route.gc_interval = 30\nnet.ipv6.route.gc_min_interval = 0\nnet.ipv6.route.gc_min_interval_ms = 500\nnet.ipv6.route.gc_thresh = 1024\nnet.ipv6.route.gc_timeout = 60\n'
CASES = [
 (
  7, Case(CMDLINE_NOT_DISABLED, None, None, SYSCTL_NOT_DISABLED),
  (
   False, set())),
 (
  7, Case(CMDLINE_DISABLED, None, None, SYSCTL_NOT_DISABLED),
  (
   True, set(['cmdline']))),
 (
  7, Case(CMDLINE_NOT_DISABLED, None, None, SYSCTL_DISABLED),
  (
   True, set(['sysctl']))),
 (
  7, Case(CMDLINE_DISABLED, None, None, SYSCTL_DISABLED),
  (
   True, set(['cmdline', 'sysctl']))),
 (
  7, Case(None, None, None, None),
  (
   False, set())),
 (
  6,
  Case(None, LSMOD_LOADED, MODPROBE_NOT_DISABLED, SYSCTL_NOT_DISABLED), (False, set())),
 (
  6,
  Case(None, LSMOD_NOT_LOADED, MODPROBE_NOT_DISABLED, SYSCTL_NOT_DISABLED), (False, set())),
 (
  6, Case(None, LSMOD_LOADED, MODPROBE_FAKE, SYSCTL_NOT_DISABLED),
  (
   False, set())),
 (
  6,
  Case(None, LSMOD_NOT_LOADED, MODPROBE_FAKE_COMMENTED, SYSCTL_NOT_DISABLED), (False, set())),
 (
  6, Case(None, LSMOD_LOADED, MODPROBE_DISABLED, SYSCTL_NOT_DISABLED),
  (
   True, set(['modprobe_disable']))),
 (
  6,
  Case(None, LSMOD_NOT_LOADED, MODPROBE_DISABLED, SYSCTL_NOT_DISABLED), (True, set(['modprobe_disable']))),
 (
  6, Case(None, LSMOD_NOT_LOADED, MODPROBE_FAKE, SYSCTL_NOT_DISABLED),
  (
   True, set(['fake_install']))),
 (
  6, Case(None, LSMOD_LOADED, MODPROBE_NOT_DISABLED, SYSCTL_DISABLED),
  (
   True, set(['sysctl']))),
 (
  6,
  Case(None, LSMOD_NOT_LOADED, MODPROBE_NOT_DISABLED, SYSCTL_DISABLED), (True, set(['sysctl']))),
 (
  6, Case(None, LSMOD_NOT_LOADED, MODPROBE_DISABLED, SYSCTL_DISABLED),
  (
   True, set(['sysctl', 'modprobe_disable']))),
 (
  6, Case(None, LSMOD_LOADED, None, None),
  (
   False, set())),
 (
  6, Case(None, None, MODPROBE_DISABLED, None),
  (
   True, set(['modprobe_disable']))),
 (
  6, Case(None, None, MODPROBE_FAKE, None),
  (
   False, set())),
 (
  6, Case(CMDLINE_RHEL6_DISABLED, None, None, None),
  (
   True, set(['cmdline'])))]

def test_integration():
    for rhel, case, result in CASES:
        context = {}
        context[Uname] = Uname(context_wrap(UNAME_RHEL7 if rhel == 7 else UNAME_RHEL6))
        if case.modprobe is not None:
            context[ModProbe] = ModProbe(context_wrap(case.modprobe, path='/etc/modprobe.d/ipv6.conf'))
        if case.lsmod is not None:
            context[LsMod] = LsMod(context_wrap(case.lsmod))
        if case.cmdline is not None:
            context[CmdLine] = CmdLine(context_wrap(case.cmdline))
        if case.sysctl is not None:
            context[Sysctl] = Sysctl(context_wrap(case.sysctl))
        un = context.get(Uname)
        mp = context.get(ModProbe)
        lsm = context.get(LsMod)
        cl = context.get(CmdLine)
        sct = context.get(Sysctl)
        ipv6 = IPv6(un, mp, lsm, cl, sct)
        assert ipv6.disabled() == result[0]
        assert ipv6.disabled_by() == result[1]

    return