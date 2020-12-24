# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ls_sys_firmware.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.ls_sys_firmware import LsSysFirmware
from insights.tests import context_wrap
LS_SYS_FIRMWARE = '\n/sys/firmware:\ntotal 0\ndrwxr-xr-x.  5 0 0 0 Dec 22 17:56 .\ndr-xr-xr-x. 13 0 0 0 Dec 22 17:56 ..\ndrwxr-xr-x.  5 0 0 0 Dec 22 17:56 acpi\ndrwxr-xr-x.  3 0 0 0 Dec 22 17:57 dmi\ndrwxr-xr-x. 10 0 0 0 Dec 22 17:57 memmap\n\n/sys/firmware/acpi:\ntotal 0\ndrwxr-xr-x. 5 0 0    0 Dec 22 17:56 .\ndrwxr-xr-x. 5 0 0    0 Dec 22 17:56 ..\ndrwxr-xr-x. 6 0 0    0 Feb 10 15:54 hotplug\ndrwxr-xr-x. 2 0 0    0 Feb 10 15:54 interrupts\n-r--r--r--. 1 0 0 4096 Feb 10 15:54 pm_profile\ndrwxr-xr-x. 3 0 0    0 Dec 22 17:56 tables\n'

def test_ls_sys_firmware():
    ls_sys_firmware = LsSysFirmware(context_wrap(LS_SYS_FIRMWARE))
    assert 'acpi' not in ls_sys_firmware
    assert '/sys/firmware/acpi' in ls_sys_firmware
    assert ls_sys_firmware.dirs_of('/sys/firmware') == ['.', '..', 'acpi', 'dmi', 'memmap']
    assert ls_sys_firmware.files_of('/sys/firmware/acpi') == ['pm_profile']