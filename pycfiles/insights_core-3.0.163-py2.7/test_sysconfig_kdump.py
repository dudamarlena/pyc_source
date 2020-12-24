# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sysconfig_kdump.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.sysconfig import KdumpSysconfig
from insights.tests import context_wrap
SYSCONFIG_KDUMP_ALL = '\n# Comments\nKDUMP_KERNELVER=""\n\nKDUMP_COMMANDLINE=""\nKDUMP_COMMANDLINE_REMOVE="hugepages hugepagesz slub_debug quiet"\nKDUMP_COMMANDLINE_APPEND="irqpoll nr_cpus=1 reset_devices cgroup_disable=memory mce=off numa=off udev.children-max=2 panic=10 rootflags=nofail acpi_no_memhotplug transparent_hugepage=never"\nKEXEC_ARGS="--elf32-core-headers"\nKDUMP_IMG="vmlinuz"\nKDUMP_IMG_EXT=""\n'
SYSCONFIG_KDUMP_SOME = '\n# Comments\n# Comments with apostrophes won\'t fool the dequoting process\nKDUMP_COMMANDLINE_APPEND="irqpoll nr_cpus=1 reset_devices cgroup_disable=memory mce=off numa=off udev.children-max=2 panic=10 rootflags=nofail acpi_no_memhotplug transparent_hugepage=never"\nKDUMP_IMG="vmlinuz"\n'

def test_sysconfig_kdump():
    sc_kdump = KdumpSysconfig(context_wrap(SYSCONFIG_KDUMP_ALL))
    assert sc_kdump is not None
    assert sc_kdump.KDUMP_KERNELVER == ''
    assert sc_kdump.KDUMP_COMMANDLINE == ''
    assert sc_kdump.KDUMP_COMMANDLINE_REMOVE == 'hugepages hugepagesz slub_debug quiet'
    assert sc_kdump.KDUMP_COMMANDLINE_APPEND == 'irqpoll nr_cpus=1 reset_devices cgroup_disable=memory mce=off numa=off udev.children-max=2 panic=10 rootflags=nofail acpi_no_memhotplug transparent_hugepage=never'
    assert sc_kdump.KEXEC_ARGS == '--elf32-core-headers'
    assert sc_kdump.KDUMP_IMG == 'vmlinuz'
    assert sc_kdump.KDUMP_IMG_EXT == ''
    assert sc_kdump.get('KDUMP_IMG') == 'vmlinuz'
    sc_kdump = KdumpSysconfig(context_wrap(SYSCONFIG_KDUMP_SOME))
    assert sc_kdump is not None
    assert sc_kdump.KDUMP_KERNELVER == ''
    assert sc_kdump.KDUMP_COMMANDLINE == ''
    assert sc_kdump.KDUMP_COMMANDLINE_REMOVE == ''
    assert sc_kdump.KDUMP_COMMANDLINE_APPEND == 'irqpoll nr_cpus=1 reset_devices cgroup_disable=memory mce=off numa=off udev.children-max=2 panic=10 rootflags=nofail acpi_no_memhotplug transparent_hugepage=never'
    assert sc_kdump.KEXEC_ARGS == ''
    assert sc_kdump.KDUMP_IMG == 'vmlinuz'
    assert sc_kdump.KDUMP_IMG_EXT == ''
    assert sc_kdump.get('KDUMP_IMG') == 'vmlinuz'
    return