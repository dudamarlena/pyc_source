# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/getconf_pagesize.py
# Compiled at: 2019-11-14 13:57:46
"""
GetconfPageSize - command ``/usr/sbin/getconf PAGE_SIZE``
=========================================================

This very simple parser returns the output of the ``getconf PAGE_SIZE`` command.

Examples:

    >>> pagesize_parsed.page_size
    4096
"""
from . import ParseException
from .. import parser, CommandParser
from insights.specs import Specs

@parser(Specs.getconf_page_size)
class GetconfPageSize(CommandParser):
    """Class for parsing 'getconf PAGE_SIZE' command output

    Output: page_size

    Attributes:
        page_size (int): returns the page_size in bytes depending upon the architecture
    """

    def parse_content(self, content):
        if len(content) != 1:
            msg = 'getconf PAGE_SIZE output contains multiple non-empty lines'
            raise ParseException(msg)
        raw = content[0].strip()
        self.page_size = int(raw)

    def __str__(self, context):
        return ('<page_size: {}>').format(self.page_size)