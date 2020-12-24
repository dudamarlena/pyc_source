# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_gluster_peer_status.py
# Compiled at: 2019-11-14 13:57:46
import doctest, pytest
from insights.parsers import gluster_peer_status, SkipException
from insights.tests import context_wrap
OUTPUT = ('\nNumber of Peers: 1\n\nHostname: versegluster1.verse.loc\nUuid: 86c0266b-c78c-4d0c-afe7-953dec143530\nState: Peer in Cluster (Connected)\n').strip()
OUTPUT_1 = ('\nNumber of Peers: 3\n\nHostname: versegluster1.verse.loc\nUuid: 86c0266b-c78c-4d0c-afe7-953dec143530\nState: Peer in Cluster (Connected)\n\nHostname: 10.30.32.16\nUuid: 3b4673e3-5e95-4c02-b9bb-2823483e067b\nState: Peer in Cluster (Connected)\n\nHostname: 10.30.32.20\nUuid: 4673e3-5e95-4c02-b9bb-2823483e067bb3\nState: Peer in Cluster (Disconnected)\n').strip()

def test_output():
    output = gluster_peer_status.GlusterPeerStatus(context_wrap(OUTPUT_1))
    assert output.status['peers'] == len(output.status.get('hosts', []))
    assert output.status.get('hosts', []) == [{'Hostname': 'versegluster1.verse.loc', 'State': 'Peer in Cluster (Connected)', 'Uuid': '86c0266b-c78c-4d0c-afe7-953dec143530'}, {'Hostname': '10.30.32.16', 'State': 'Peer in Cluster (Connected)', 'Uuid': '3b4673e3-5e95-4c02-b9bb-2823483e067b'}, {'Hostname': '10.30.32.20', 'State': 'Peer in Cluster (Disconnected)', 'Uuid': '4673e3-5e95-4c02-b9bb-2823483e067bb3'}]


def test_blank_output():
    with pytest.raises(SkipException) as (e):
        gluster_peer_status.GlusterPeerStatus(context_wrap(''))
    assert 'No data.' in str(e)


def test_documentation():
    failed_count, tests = doctest.testmod(gluster_peer_status, globs={'output': gluster_peer_status.GlusterPeerStatus(context_wrap(OUTPUT))})
    assert failed_count == 0