# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_avc_cache_threshold.py
# Compiled at: 2019-05-16 13:41:33
import doctest, pytest
from insights.parsers import avc_cache_threshold, ParseException
from insights.parsers.avc_cache_threshold import AvcCacheThreshold
from insights.tests import context_wrap
AVC_CACHE_THRESHOLD = ('\n512\n').strip()
AVC_CACHE_THRESHOLD_INVALID = ('\ninvalid\ninvalid\ninvalid\n').strip()

def test_avc_cache_threshold():
    cache_threshold = avc_cache_threshold.AvcCacheThreshold(context_wrap(AVC_CACHE_THRESHOLD))
    assert cache_threshold.cache_threshold == 512


def test_invalid():
    with pytest.raises(ParseException) as (e):
        avc_cache_threshold.AvcCacheThreshold(context_wrap(AVC_CACHE_THRESHOLD_INVALID))
    assert 'invalid' in str(e)


def test_avc_cache_threshold_doc_examples():
    env = {'avc_cache_threshold': AvcCacheThreshold(context_wrap(AVC_CACHE_THRESHOLD))}
    failed, total = doctest.testmod(avc_cache_threshold, globs=env)
    assert failed == 0