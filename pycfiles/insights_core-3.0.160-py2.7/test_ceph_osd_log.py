# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ceph_osd_log.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.ceph_osd_log import CephOsdLog
from insights.tests import context_wrap
from datetime import datetime
CEPH_OSD_LOG = ('\n2015-10-30 09:09:30.334033 7f12c6f8b700  0 -- 10.1.26.72:6851/1003139 >> 10.1.26.64:6800/1005943 pipe(0x14f3b000 sd=464 :6851 s=0 pgs=0 cs=0 l=0 c=0xfe3a840).accept connect_seq 30 vs existing 29 state standby\n2015-10-30 10:18:38.691642 7f1301f37700  0 -- 10.1.26.72:6851/1003139 >> 10.1.26.56:6820/1004150 pipe(0x6c79000 sd=275 :6851 s=0 pgs=0 cs=0 l=0 c=0x1504cf20).accept connect_seq 2 vs existing 1 state standby\n2015-10-30 10:18:58.266050 7f12e97b1700  0 -- 10.1.26.72:6851/1003139 >> 10.1.26.23:6830/30212 pipe(0x10759000 sd=629 :6851 s=2 pgs=22 cs=1 l=0 c=0x10178160).fault, initiating reconnect\n').strip()
matched_lines = [
 '2015-10-30 09:09:30.334033 7f12c6f8b700  0 -- 10.1.26.72:6851/1003139 >> 10.1.26.64:6800/1005943 pipe(0x14f3b000 sd=464 :6851 s=0 pgs=0 cs=0 l=0 c=0xfe3a840).accept connect_seq 30 vs existing 29 state standby', '2015-10-30 10:18:38.691642 7f1301f37700  0 -- 10.1.26.72:6851/1003139 >> 10.1.26.56:6820/1004150 pipe(0x6c79000 sd=275 :6851 s=0 pgs=0 cs=0 l=0 c=0x1504cf20).accept connect_seq 2 vs existing 1 state standby']

def test_ceph_osd_log():
    ceph_osd_log_obj = CephOsdLog(context_wrap(CEPH_OSD_LOG))
    assert 'initiating reconnect' in ceph_osd_log_obj
    assert CEPH_OSD_LOG.splitlines()[1] == ceph_osd_log_obj.get('state standby')[1]['raw_message']
    assert sorted([ i['raw_message'] for i in ceph_osd_log_obj.get_after(datetime(2015, 10, 30, 10, 0, 0)) ]) == [
     '2015-10-30 10:18:38.691642 7f1301f37700  0 -- 10.1.26.72:6851/1003139 >> 10.1.26.56:6820/1004150 pipe(0x6c79000 sd=275 :6851 s=0 pgs=0 cs=0 l=0 c=0x1504cf20).accept connect_seq 2 vs existing 1 state standby',
     '2015-10-30 10:18:58.266050 7f12e97b1700  0 -- 10.1.26.72:6851/1003139 >> 10.1.26.23:6830/30212 pipe(0x10759000 sd=629 :6851 s=2 pgs=22 cs=1 l=0 c=0x10178160).fault, initiating reconnect']