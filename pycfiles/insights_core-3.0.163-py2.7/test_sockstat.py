# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sockstat.py
# Compiled at: 2019-11-14 13:57:46
import doctest, pytest
from insights.parsers import sockstat
from insights.parsers.sockstat import SockStats
from insights.parsers import SkipException
from insights.tests import context_wrap
SOCK_STATS = ('\nsockets: used 3037\nTCP: inuse 1365 orphan 17 tw 2030 alloc 2788 mem 4109\nUDP: inuse 6 mem 3\nUDPLITE: inuse 0\nRAW: inuse 0\nFRAG: inuse 0 memory 10\n').strip()
SOCK_STATS_NO = ('\n').strip()
SOCK_STATS_DOC = ('\nsockets: used 3037\nTCP: inuse 1365 orphan 17 tw 2030 alloc 2788 mem 4109\nUDP: inuse 6 mem 3\nUDPLITE: inuse 0\nRAW: inuse 0\nFRAG: inuse 0 memory 0\n').strip()
SOCK_STATS_NO_2 = ('\nIn valid data is present\n').strip()

def test_sockstat():
    stats = SockStats(context_wrap(SOCK_STATS))
    assert stats.seg_details('sockets') == {'used': '3037'}
    assert stats.seg_details('tcp') == {'inuse': '1365', 'orphan': '17', 'tw': '2030', 'alloc': '2788', 'mem': '4109'}
    assert stats.seg_element_details('tcp', 'inuse') == 1365
    assert stats.seg_element_details('frag', 'memory') == 10
    assert stats.seg_element_details('xyz', 'abc') is None
    assert stats.seg_element_details(None, None) is None
    assert stats.seg_element_details('tcp', 'abc') is None
    assert len(stats.sock_stats)
    with pytest.raises(SkipException) as (exc):
        sock_obj = SockStats(context_wrap(SOCK_STATS_NO))
        assert sock_obj is not None
    assert 'No Contents' in str(exc)
    return


def test_modinfo_doc_examples():
    env = {'sock_obj': SockStats(context_wrap(SOCK_STATS_DOC))}
    failed, total = doctest.testmod(sockstat, globs=env)
    assert failed == 0