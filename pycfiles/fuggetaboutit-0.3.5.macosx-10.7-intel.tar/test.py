# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/fuggetaboutit/test.py
# Compiled at: 2013-10-30 17:15:16
from tests.test_scaling_timing_bloom_filter import TestScalingTimingBloomFilter
from tests.test_timing_bloom_filter import TestTimingBloomFilter

def all():
    return (TestTimingBloomFilter, TestScalingTimingBloomFilter)