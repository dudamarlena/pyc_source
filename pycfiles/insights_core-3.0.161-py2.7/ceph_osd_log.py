# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/ceph_osd_log.py
# Compiled at: 2019-05-16 13:41:33
"""
CephOsdLog - file ``var/log/ceph/ceph-osd.*.log``
=================================================

This is a standard log parser based on the LogFileOutput class.

Sample input::

    2015-10-30 09:09:30.334033 7f12c6f8b700  0 -- 10.1.26.72:6851/1003139 >> 10.1.26.64:6800/1005943 pipe(0x14f3b000 sd=464 :6851 s=0 pgs=0 cs=0 l=0 c=0xfe3a840).accept connect_seq 30 vs existing 29 state standby
    2015-10-30 10:18:58.266050 7f12e97b1700  0 -- 10.1.26.72:6851/1003139 >> 10.1.26.23:6830/30212 pipe(0x10759000 sd=629 :6851 s=2 pgs=22 cs=1 l=0 c=0x10178160).fault, initiating reconnect

Examples:

    >>> logs = shared[CephOsdLog]
    >>> 'initiating reconnect' in logs
    True
    >>> logs.get('pipe')
    ['2015-10-30 09:09:30.334033 7f12c6f8b700  0 -- 10.1.26.72:6851/1003139 >> 10.1.26.64:6800/1005943 pipe(0x14f3b000 sd=464 :6851 s=0 pgs=0 cs=0 l=0 c=0xfe3a840).accept connect_seq 30 vs existing 29 state standby',
     '2015-10-30 10:18:58.266050 7f12e97b1700  0 -- 10.1.26.72:6851/1003139 >> 10.1.26.23:6830/30212 pipe(0x10759000 sd=629 :6851 s=2 pgs=22 cs=1 l=0 c=0x10178160).fault, initiating reconnect']
    >>> from datetime import datetime
    >>> logs.get_after(datetime(2015, 10, 30, 10, 0, 0))
    >>> ['2015-10-30 10:18:58.266050 7f12e97b1700  0 -- 10.1.26.72:6851/1003139 >> 10.1.26.23:6830/30212 pipe(0x10759000 sd=629 :6851 s=2 pgs=22 cs=1 l=0 c=0x10178160).fault, initiating reconnect']
"""
from .. import LogFileOutput, parser
from insights.specs import Specs

@parser(Specs.ceph_osd_log)
class CephOsdLog(LogFileOutput):
    """
    Provide access to Ceph OSD logs using the LogFileOutput parser class.

    .. note::
        Please refer to the super-class :class:`insights.core.LogFileOutput`
    """
    time_format = '%Y-%m-%d %H:%M:%S.%f'