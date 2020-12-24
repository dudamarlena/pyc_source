# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lotonumber/loto.py
# Compiled at: 2017-09-13 10:37:13
# Size of source mod 2**32: 971 bytes
import sys, numpy as np, matplotlib.pyplot as plt
from all_loto import AllLoto
from miniloto_analysis import MinilotoAnalysis
from loto6_analysis import Loto6Analysis
from loto7_analysis import Loto7Analysis

def main():
    if len(sys.argv) != 2:
        print('引数の数が違います。\nloto 種別(5,6,7) 抽選回(1〜)\n')
        sys.exit()
    div = int(sys.argv[1])
    if div < 5 or div > 7:
        print('宝くじ種別が違います。')
        print('宝くじ種別:\n5:ミニロト\n6:ロト6\n7:ロト7')
        sys.exit()
    loto_class = [MinilotoAnalysis, Loto6Analysis, Loto7Analysis]
    all_loto = AllLoto()
    loto_data = [all_loto.miniloto, all_loto.loto6, all_loto.loto7]
    analysis = loto_class[(div - 5)](loto_data[(div - 5)])
    ratio = analysis.number_ratio()
    plt.bar(list(range(1, len(ratio) + 1)), ratio)
    plt.show()


if __name__ == '__main__':
    main()