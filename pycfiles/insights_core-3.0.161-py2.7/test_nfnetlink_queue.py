# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_nfnetlink_queue.py
# Compiled at: 2019-05-16 13:41:33
import pytest
from insights.parsers import nfnetlink_queue
from insights.tests import context_wrap
import doctest

def test_nfnetlink_doc_examples():
    failed, total = doctest.testmod(nfnetlink_queue)
    assert failed == 0


NFNETLINK_QUEUE = ('\n    0  -4423     0 2 65535     0     0       22  1\n    1  -4424     0 2 65535     0     0       27  1\n    2  -4425     0 2 65535     0     0       17  1\n    3  -4426     0 2 65535     0     0       14  1\n    4  -4427     0 2 65535     0     0       22  1\n    5  -4428     0 2 65535     0     0       16  1\n').strip()
CORRUPT_NFNETLINK_QUEUE_1 = ('\n    0  -4423     0 2 65535     0     0       22  1\n    1  -4424     0 2 6553\n    2  -4425     0 2 65535     0     0       17  1\n    3  -4426     0 2 65535     0     0       14  1\n    4  -4427     0 2 65535     0     0       22  1\n    5  -4428     0 2 65535     0     0       16  1\n').strip()
CORRUPT_NFNETLINK_QUEUE_2 = ('\n    0  -4423     0 2 65535     0     0       22  1\n    1  -4424     0 2 astring   0     0       27  1\n    2  -4425     0 2 65535     0     0       17  1\n    3  -4426     0 2 65535     0     0       14  1\n    4  -4427     0 2 65535     0     0       22  1\n    5  -4428     0 2 65535     0     0       16  1\n').strip()

def test_parse_content():
    nfnet_link_queue = nfnetlink_queue.NfnetLinkQueue(context_wrap(NFNETLINK_QUEUE))
    row = nfnet_link_queue.data[0]
    assert row['queue_number'] == 0
    assert row['peer_portid'] == -4423
    assert row['queue_total'] == 0
    assert row['copy_mode'] == 2
    assert row['copy_range'] == 65535
    assert row['queue_dropped'] == 0
    assert row['user_dropped'] == 0
    assert row['id_sequence'] == 22
    row = nfnet_link_queue.data[5]
    assert row['queue_number'] == 5
    assert row['peer_portid'] == -4428
    assert row['queue_total'] == 0
    assert row['copy_mode'] == 2
    assert row['copy_range'] == 65535
    assert row['queue_dropped'] == 0
    assert row['user_dropped'] == 0
    assert row['id_sequence'] == 16


def test_missing_columns():
    with pytest.raises(AssertionError):
        nfnetlink_queue.NfnetLinkQueue(context_wrap(CORRUPT_NFNETLINK_QUEUE_1))


def test_wrong_type():
    with pytest.raises(ValueError):
        nfnetlink_queue.NfnetLinkQueue(context_wrap(CORRUPT_NFNETLINK_QUEUE_2))