# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lotonumber/all_loto.py
# Compiled at: 2017-09-11 03:49:02
# Size of source mod 2**32: 1146 bytes
import sys, os, csv
from read_miniloto import read_miniloto
from read_loto6 import read_loto6
from read_loto7 import read_loto7

class AllLoto:

    def __init__(self):
        self.miniloto = read_miniloto()
        self.loto6 = read_loto6()
        self.loto7 = read_loto7()

    def data(self, div, round):
        """
        ロトくじの当選データを返す。
        div:  宝くじ種別(数値 5:ミニロト, 6:ロト6, 7:ロト7)
        round: 抽選回(1〜)
        """
        if div == 5:
            return self.miniloto[(round - 1)]
        else:
            if div == 6:
                return self.loto6[(round - 1)]
            if div == 7:
                return self.loto7[(round - 1)]
        raise '宝くじ種別が不正です。div={}'.format(div)


if __name__ == '__main__':
    all_loto = AllLoto()
    loto = all_loto.data(7, 208)
    print(loto.nums)
    print(loto.bonus)
    print(loto.priznum)
    print(loto.amounts)
    print(loto.c_over)