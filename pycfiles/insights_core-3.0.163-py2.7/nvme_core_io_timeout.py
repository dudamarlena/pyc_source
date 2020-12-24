# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/nvme_core_io_timeout.py
# Compiled at: 2019-05-16 13:41:33
"""
NVMeCoreIOTimeout - The timeout for I/O operations submitted to NVMe devices
============================================================================

This parser reads the content of ``/sys/module/nvme_core/parameters/io_timeout``.
"""
from insights import Parser, parser
from insights.specs import Specs
from ..parsers import SkipException, ParseException

@parser(Specs.nvme_core_io_timeout)
class NVMeCoreIOTimeout(Parser):
    """
    Class for parsing the content of the ``/sys/module/nvme_core/parameters/io_timeout``.

    A typical sample of the content of this file looks like::

        4294967295

    Raises:
        SkipException: When content is empty or no parse-able content.
        ParseException: When type cannot be recognized.

    Attributes:
        val (int): It is used to show the current value of the timeout for I/O operations submitted to NVMe devices.

    Examples:
        >>> nciotmo.val
        4294967295
    """

    def parse_content(self, content):
        if not content or len(content) != 1:
            raise SkipException()
        if not content[0].strip('').isdigit():
            raise ParseException('Unexpected content: ', content)
        self.val = int(content[0].strip())