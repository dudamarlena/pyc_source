# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lotonumber/miniloto.py
# Compiled at: 2017-09-11 04:49:30
# Size of source mod 2**32: 550 bytes
import sys
from all_loto import AllLoto

def main():
    all_loto = AllLoto()
    if len(sys.argv) != 2:
        print('引数の数が違います。\nminiloto 抽選回(1〜)\n')
        sys.exit()
    round = int(sys.argv[1])
    if round <= 0 or round > len(all_loto.miniloto):
        print('抽選回が最大値を超えています。')
        print('抽選回≦{}'.format(len(all_loto.miniloto)))
        sys.exit()
    data = all_loto.data(5, int(sys.argv[1]))
    print(data.nums, data.bonus)


if __name__ == '__main__':
    main()