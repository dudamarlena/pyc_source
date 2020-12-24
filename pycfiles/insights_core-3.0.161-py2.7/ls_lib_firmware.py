# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/ls_lib_firmware.py
# Compiled at: 2019-05-16 13:41:33
"""
Lists ALL the firmware packages
===============================

Parsers included in this module are:

LsLibFW - command ``/bin/ls -lanR /lib/firmware``
----------------------------------------------------

"""
from insights.specs import Specs
from .. import parser, CommandParser, FileListing

@parser(Specs.ls_lib_firmware)
class LsLibFW(CommandParser, FileListing):
    """
    This parser will help to parse the output of command ``/bin/ls -lanR /lib/firmware``

    Typical output of the ``/bin/ls -lanR /lib/firmware`` command is::

        /lib/firmware:
        total 37592
        drwxr-xr-x. 83 0 0    8192 Aug 14 02:43 .
        dr-xr-xr-x. 26 0 0    4096 Aug 14 02:22 ..
        drwxr-xr-x.  2 0 0      40 Aug 14 02:42 3com
        lrwxrwxrwx.  1 0 0      16 Aug 14 02:42 a300_pfp.fw -> qcom/a300_pfp.fw
        lrwxrwxrwx.  1 0 0      16 Aug 14 02:42 a300_pm4.fw -> qcom/a300_pm4.fw
        drwxr-xr-x.  2 0 0      34 Aug 14 02:42 acenic
        drwxr-xr-x.  2 0 0      50 Aug 14 02:42 adaptec
        drwxr-xr-x.  2 0 0      73 Aug 14 02:42 advansys
        
        /lib/firmware/3com:
        total 84
        drwxr-xr-x.  2 0 0    40 Aug 14 02:42 .
        drwxr-xr-x. 83 0 0  8192 Aug 14 02:43 ..
        -rw-r--r--.  1 0 0 24880 Jun  6 10:14 3C359.bin
        -rw-r--r--.  1 0 0 44548 Jun  6 10:14 typhoon.bin
        
        /lib/firmware/acenic:
        total 160
        drwxr-xr-x.  2 0 0    34 Aug 14 02:42 .
        drwxr-xr-x. 83 0 0  8192 Aug 14 02:43 ..
        -rw-r--r--.  1 0 0 73116 Jun  6 10:14 tg1.bin
        -rw-r--r--.  1 0 0 77452 Jun  6 10:14 tg2.bin

    Example:

        >>> type(lslibfw)
        <class 'insights.parsers.ls_lib_firmware.LsLibFW'>
        >>> lslibfw.files_of("/lib/firmware/bnx2x")
        ['bnx2x-e1-6.0.34.0.fw', 'bnx2x-e1-6.2.5.0.fw', 'bnx2x-e1-6.2.9.0.fw', 'bnx2x-e1-7.0.20.0.fw', 'bnx2x-e1-7.0.23.0.fw']
        >>> lslibfw.dir_contains("/lib/firmware/bnx2x", "bnx2x-e1-6.0.34.0.fw")
        True
        >>> lslibfw.dirs_of("/lib/firmware")
        ['.', '..', '3com', 'acenic', 'adaptec', 'advansys']
        >>> lslibfw.total_of("/lib/firmware")
        37592
    """
    pass