# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/ls_sys_firmware.py
# Compiled at: 2019-05-16 13:41:33
"""
LsSysFirmware - command ``ls /sys/firmware``
============================================

The ``ls -lanR /sys/firmware`` command provides information for the listing of
the ``/sys/firmware`` directory.

Sample input is shown in the Examples. See ``FileListing`` class for
additional information.

Examples:
    >>> LS_SYS_FIRMWARE = '''
    ... /sys/firmware:
    ... total 0
    ... drwxr-xr-x.  5 0 0 0 Dec 22 17:56 .
    ... dr-xr-xr-x. 13 0 0 0 Dec 22 17:56 ..
    ... drwxr-xr-x.  5 0 0 0 Dec 22 17:56 acpi
    ... drwxr-xr-x.  3 0 0 0 Dec 22 17:57 dmi
    ... drwxr-xr-x. 10 0 0 0 Dec 22 17:57 memmap
    ...
    ... /sys/firmware/acpi:
    ... total 0
    ... drwxr-xr-x. 5 0 0    0 Dec 22 17:56 .
    ... drwxr-xr-x. 5 0 0    0 Dec 22 17:56 ..
    ... drwxr-xr-x. 6 0 0    0 Feb 10 15:54 hotplug
    ... drwxr-xr-x. 2 0 0    0 Feb 10 15:54 interrupts
    ... -r--r--r--. 1 0 0 4096 Feb 10 15:54 pm_profile
    ... drwxr-xr-x. 3 0 0    0 Dec 22 17:56 tables
    ... '''
    >>> ls_sys_firmware = LsSysFirmware(context_wrap(LS_SYS_FIRMWARE))
    >>> "acpi" in ls_sys_firmware
    False
    >>> "/sys/firmware/acpi" in ls_sys_firmware
    True
    >>> ls_sys_firmware.dirs_of("/sys/firmware")
    ['.', '..', 'acpi', 'dmi', 'memmap']
    >>> ls_sys_firmware.files_of("/sys/firmware/acpi")
    ['pm_profile']
"""
from .. import parser
from .. import FileListing, CommandParser
from insights.specs import Specs

@parser(Specs.ls_sys_firmware)
class LsSysFirmware(CommandParser, FileListing):
    """Parses output of ``ls -lanR /sys/firmware`` command."""
    pass