# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lotonumber/analysis_basic.py
# Compiled at: 2017-09-13 10:48:46
# Size of source mod 2**32: 1330 bytes
from collections import defaultdict
import numpy as np

class AnalysisBasic:

    def __init__(self, loto_data, loto_div):
        """
        loto_data: ロトくじデータ
        loto_div:  ロトくじ区分(5:ミニロト,6:ロト6, 7:ロト7)
        """
        self._data = loto_data
        self.div = loto_div

    @property
    def max_no(self):
        return [31, 43, 37][(self.div - 5)]

    def frequency(self):
        """抽選数字の出現頻度をリストで返す
        """
        nums_dist = defaultdict(int)
        for loto_basic in self._data:
            for col in range(self.div):
                number = int(loto_basic.nums[col])
                nums_dist[number] += 1

        dist_list = list(range(self.max_no))
        for key in nums_dist.keys():
            dist_list[key - 1] = nums_dist[key]

        return dist_list

    def number_ratio(self):
        """抽選数字の出現確率を返す
        """
        nums_ratio = np.array((self.frequency()), dtype=(np.float64))
        return nums_ratio / sum(nums_ratio)