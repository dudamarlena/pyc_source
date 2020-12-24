# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_avc_hash_stats.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import avc_hash_stats
from insights.parsers.avc_hash_stats import AvcHashStats
from insights.tests import context_wrap
AVC_HASH_STATS = ('\nentries: 509\nbuckets used: 290/512\nlongest chain: 7\n').strip()

def test_avc_hash_stats():
    hash_stats = avc_hash_stats.AvcHashStats(context_wrap(AVC_HASH_STATS))
    assert hash_stats.entries == 509
    assert hash_stats.buckets == 512
    assert hash_stats.buckets_used == 290
    assert hash_stats.longest_chain == 7


def test_avc_hash_stats_doc_examples():
    env = {'avc_hash_stats': AvcHashStats(context_wrap(AVC_HASH_STATS))}
    failed, total = doctest.testmod(avc_hash_stats, globs=env)
    assert failed == 0