# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ceph_osd_tree_text.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import ceph_osd_tree_text, ParseException, SkipException
from insights.parsers.ceph_osd_tree_text import CephOsdTreeText
from insights.tests import context_wrap
import pytest, doctest
OSD_TREE_CEPH_V3 = ('\nID CLASS WEIGHT  TYPE NAME       STATUS REWEIGHT PRI-AFF\n-1       0.08752 root default\n-9       0.02917     host ceph1\n 2   hdd 0.01459         osd.2       up  1.00000 1.00000\n 5   hdd 0.01459         osd.5       up  1.00000 1.00000\n-5       0.02917     host ceph2\n 1   hdd 0.01459         osd.1       up  1.00000 1.00000\n 4   hdd 0.01459         osd.4       up  1.00000 1.00000\n-3       0.02917     host ceph3\n 0   hdd 0.01459         osd.0       up  1.00000 1.00000\n 3   hdd 0.01459         osd.3       up  1.00000 1.00000\n-7             0     host ceph_1\n').strip()
OSD_TREE_CEPH_V2 = ('\nID WEIGHT  TYPE NAME     UP/DOWN REWEIGHT PRIMARY-AFFINITY\n-1 0.11670 root default\n-2 0.02917     host osd1\n 2 0.01459         osd.2      up  1.00000          1.00000\n 5 0.01459         osd.5      up  1.00000          1.00000\n-3 0.02917     host osd2\n 1 0.01459         osd.1      up  1.00000          1.00000\n 3 0.01459         osd.3      up  1.00000          1.00000\n-4 0.02917     host osd3\n 0 0.01459         osd.0      up  1.00000          1.00000\n 4 0.01459         osd.4      up  1.00000          1.00000\n-5 0.02917     host osd4\n 6 0.01459         osd.6    down        0          1.00000\n 7 0.01459         osd.7    down        0          1.00000\n').strip()
OSD_TREE_EMPTY = ('\n').strip()
OSD_TREE_INVALID = ('\nID WEIGHT  UP/DOWN REWEIGHT PRIMARY-AFFINITY\n').strip()

def test_ceph_osd_tree_text_v3():
    ceph_osd_tree = CephOsdTreeText(context_wrap(OSD_TREE_CEPH_V3))
    assert ceph_osd_tree['nodes'][0] == {'id': '-1', 'device_class': '', 'crush_weight': '0.08752', 'name': 'default', 'status': '', 
       'reweight': '', 'primary_affinity': '', 'type': 'root', 'children': [
                  -7, -3, -5, -9]}


def test_ceph_osd_tree_text_v2():
    ceph_osd_tree = CephOsdTreeText(context_wrap(OSD_TREE_CEPH_V2))
    assert ceph_osd_tree['nodes'][1] == {'id': '-2', 'crush_weight': '0.02917', 'name': 'osd1', 'status': '', 'reweight': '', 
       'primary_affinity': '', 'type': 'host', 'children': [5, 2]}


def test_skip_content():
    with pytest.raises(SkipException) as (e):
        CephOsdTreeText(context_wrap(OSD_TREE_EMPTY))
    assert 'Empty content.' in str(e)


def test_error_content():
    with pytest.raises(ParseException) as (e):
        CephOsdTreeText(context_wrap(OSD_TREE_INVALID))
    assert 'Wrong content in table' in str(e)


def test_ceph_osd_tree_text_doc_examples():
    env = {'ceph_osd_tree_text': CephOsdTreeText(context_wrap(OSD_TREE_CEPH_V3))}
    failed, total = doctest.testmod(ceph_osd_tree_text, globs=env)
    assert failed == 0