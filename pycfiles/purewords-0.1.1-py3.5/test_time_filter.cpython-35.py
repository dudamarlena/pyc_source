# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/filters/test_time_filter.py
# Compiled at: 2018-08-07 00:31:26
# Size of source mod 2**32: 608 bytes
"""Time filter testcase"""
from unittest import TestCase
from purewords.filters import time_filter

class TestTimeFilterClass(TestCase):

    def setUp(self):
        self.filter = time_filter

    def test_time_filter(self):
        sentence = '今天是2018-02-30日，' + '也是1070230，又是20180230, ' + '早上07:30，全國放假一天'
        answer = '今天是_time_日，也是_time_，' + '又是_time_, 早上_time_，全國放假一天'
        self.assertEqual(answer, self.filter(sentence))