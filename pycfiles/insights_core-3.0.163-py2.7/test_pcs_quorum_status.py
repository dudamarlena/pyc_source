# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_pcs_quorum_status.py
# Compiled at: 2020-03-25 13:10:41
import doctest, pytest
from insights.parsers import pcs_quorum_status, ParseException, SkipException
from insights.parsers.pcs_quorum_status import PcsQuorumStatus
from insights.tests import context_wrap
PCS_QUORUM_STATUS = ('\nQuorum information\n------------------\nDate:             Wed Jun 29 13:17:02 2016\nQuorum provider:  corosync_votequorum\nNodes:            2\nNode ID:          1\nRing ID:          1/8272\nQuorate:          Yes\n\nVotequorum information\n----------------------\nExpected votes:   3\nHighest expected: 3\nTotal votes:      3\nQuorum:           2\nFlags:            Quorate Qdevice\n\nMembership information\n----------------------\n    Nodeid      Votes    Qdevice Name\n         1          1    A,V,NMW node1 (local)\n         2          1    A,V,NMW node2\n         0          1            Qdevice\n').strip()
PCS_QUORUM_STATUS_INVALID = ('\nQuorum information\n------------------\nDate:             Wed Jun 29 13:17:02 2016\nQuorum provider:  corosync_votequorum\nNodes:            2\nNode ID:          1\nRing ID:          1/8272\nQuorate:          Yes\n\nXXXX invalid information\n----------------------\nExpected votes:   3\nHighest expected: 3\nTotal votes:      3\nQuorum:           2\nFlags:            Quorate Qdevice\n\nMembership information\n----------------------\n    Nodeid      Votes    Qdevice Name\n         1          1    A,V,NMW node1 (local)\n         2          1    A,V,NMW node2\n         0          1            Qdevice\n').strip()
PCS_QUORUM_STATUS_EMPTY = ('\n').strip()

def test_pcs_quorum_status():
    pcs_quorum_status = PcsQuorumStatus(context_wrap(PCS_QUORUM_STATUS))
    assert pcs_quorum_status.quorum_info['Date'] == 'Wed Jun 29 13:17:02 2016'
    assert pcs_quorum_status.votequorum_info['Highest expected'] == '3'
    assert pcs_quorum_status.membership_info[2]['Qdevice'] == ''
    assert len(pcs_quorum_status.membership_info) == 3
    assert pcs_quorum_status.membership_info[1] == {'Nodeid': '2', 'Votes': '1', 'Qdevice': 'A,V,NMW', 'Name': 'node2'}


def test_invalid():
    with pytest.raises(ParseException) as (e):
        PcsQuorumStatus(context_wrap(PCS_QUORUM_STATUS_INVALID))
    assert 'Incorrect content' in str(e)


def test_empty():
    with pytest.raises(SkipException) as (e):
        PcsQuorumStatus(context_wrap(PCS_QUORUM_STATUS_EMPTY))
    assert 'Empty content' in str(e)


def test_pcs_quorum_status_doc_examples():
    env = {'pcs_quorum_status': PcsQuorumStatus(context_wrap(PCS_QUORUM_STATUS))}
    failed, total = doctest.testmod(pcs_quorum_status, globs=env)
    assert failed == 0