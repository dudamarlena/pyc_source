# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/max_uid.py
# Compiled at: 2019-12-13 11:35:35
"""
MaxUID - command ``/bin/awk -F':' '{ if($3 > max) max = $3 } END { print max }' /etc/passwd``
=============================================================================================

This module provides the MaxUID value gathered from the ``/etc/passwd`` file.
"""
from insights.core import Parser
from insights.core.plugins import parser
from insights.parsers import ParseException, SkipException
from insights.specs import Specs

@parser(Specs.max_uid)
class MaxUID(Parser):
    """
    Class for parsing the MaxUID value from the ``/etc/passwd`` file returned by the command::

        /bin/awk -F':' '{ if($3 > max) max = $3 } END { print max }' /etc/passwd

    Typical output of the ``/etc/passwd`` file is::

        root:x:0:0:root:/root:/bin/bash
        bin:x:1:1:bin:/bin:/sbin/nologin
        daemon:x:2:2:daemon:/sbin:/sbin/nologin
        adm:x:3:4:adm:/var/adm:/sbin/nologin
        lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
        sync:x:5:0:sync:/sbin:/bin/sync
        shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
        halt:x:7:0:halt:/sbin:/sbin/halt
        mail:x:8:12:mail:/var/spool/mail:/sbin/nologin
        nobody:x:65534:65534:Kernel Overflow User:/:/sbin/nologin

    Typical output of this parser is::

        65534

    Raises:
        SkipException: When content is empty or cannot be parsed.
        ParseException: When type cannot be recognized.

    Examples:
        >>> max_uid.value
        65534
    """

    def parse_content(self, content):
        if not content:
            raise SkipException('No content.')
        for line in content:
            try:
                self.value = int(line)
            except ValueError as e:
                raise ParseException('Failed to parse content with error: {}', format(str(e)))