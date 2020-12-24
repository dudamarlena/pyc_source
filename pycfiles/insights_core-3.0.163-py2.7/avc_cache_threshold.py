# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/avc_cache_threshold.py
# Compiled at: 2019-05-16 13:41:33
"""
AvcCacheThreshold - File ``/sys/fs/selinux/avc/cache_threshold``
================================================================

This parser reads the content of ``/sys/fs/selinux/avc/cache_threshold``.
"""
from .. import parser, CommandParser
from ..parsers import ParseException
from insights.specs import Specs

@parser(Specs.avc_cache_threshold)
class AvcCacheThreshold(CommandParser):
    """
    Class ``AvcCacheThreshold`` parses the content of the ``/sys/fs/selinux/avc/cache_threshold``.

    Attributes:
        cache_threshold (int): It is used to show the value of cache threshold.

    A typical sample of the content of this file looks like::

        512

    Examples:
        >>> type(avc_cache_threshold)
        <class 'insights.parsers.avc_cache_threshold.AvcCacheThreshold'>
        >>> avc_cache_threshold.cache_threshold
        512
    """

    def parse_content(self, content):
        if len(content) != 1:
            raise ParseException('Error: ', content[0] if content else 'empty file')
        self.cache_threshold = int(content[0].strip())