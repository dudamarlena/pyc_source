# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/dracut_modules.py
# Compiled at: 2020-04-23 14:49:03
"""
Dracut module configuration files to build and extend the initramfs image
=========================================================================

This module contains the following parsers:

DracutModuleKdumpCaptureService - file ``/usr/lib/dracut/modules.d/99kdumpbase/kdump-capture.service``
------------------------------------------------------------------------------------------------------
"""
from insights import parser, IniConfigFile
from insights.specs import Specs

@parser(Specs.dracut_kdump_capture_service)
class DracutModuleKdumpCaptureService(IniConfigFile):
    """
    Class for parsing the `/usr/lib/dracut/modules.d/99kdumpbase/kdump-capture.service` file.

    .. note::
        Please refer to its super-class :py:class:`insights.core.IniConfigFile`
        for full usage.

    Sample input::

        [Unit]
        Description=Kdump Vmcore Save Service
        After=initrd.target initrd-parse-etc.service sysroot.mount
        Before=initrd-cleanup.service

        [Service]
        Type=oneshot
        ExecStart=/bin/kdump.sh
        StandardInput=null
        StandardOutput=syslog

    Examples:
        >>> 'Service' in config.sections()
        True
        >>> config.has_option('Service', 'Type')
        True
        >>> config.get('Service', 'Type') == 'oneshot'
        True
    """
    pass