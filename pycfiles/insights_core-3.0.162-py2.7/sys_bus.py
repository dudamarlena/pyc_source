# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/sys_bus.py
# Compiled at: 2019-11-14 13:57:46
"""
``/sys/bus`` Device Usage Information
=====================================

A parser to parse the usage information of devices connected
on sys/bus.

Parsers included in this module are:

CdcWDM - file ``/sys/bus/usb/drivers/cdc_wdm/module/refcnt``
------------------------------------------------------------

"""
from insights import parser, Parser
from insights.parsers import ParseException
from insights.specs import Specs

@parser(Specs.cdc_wdm)
class CdcWDM(Parser):
    """
    This file `/sys/bus/usb/drivers/cdc_wdm/module/refcnt` contains
    device usage count, i.e if a device is in use then the non-zero
    value will be present in the file.

    Sample Content::

        0 - Not in use.
        1 - Device is opened and it is in use.

    Examples::

        >>> type(device_usage)
        <class 'insights.parsers.sys_bus.CdcWDM'>
        >>> device_usage.device_usage_cnt
        1
        >>> device_usage.device_in_use
        True

    Raises:
        SkipException: When contents are empty
        ParseException: When contents are invalid
    """

    def parse_content(self, content):
        try:
            self._ref_count = int(content[0].strip())
        except Exception:
            raise ParseException('Invalid Content!')

    @property
    def device_usage_cnt(self):
        """
        Returns (int): device usage count.
        """
        return self._ref_count

    @property
    def device_in_use(self):
        """
        Returns (bool): ``True`` when device in use else ``False``.
        """
        if self._ref_count:
            return True
        return False