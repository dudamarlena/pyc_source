# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lotonumber/loto6.py
# Compiled at: 2017-09-11 04:49:46
# Size of source mod 2**32: 527 bytes
import sys
from all_loto import AllLoto

def main():
    all_loto = AllLoto()
    if len(sys.argv) != 2:
        print('引数の数が違います。\nloto6 抽選回(1〜)\n')
        sys.exit()
    round = int(sys.argv[1])
    if round <= 0 or round > len(all_loto.loto6):
        print('抽選回が不正です。')
        print('1≦抽選回≦{}'.format(len(all_loto.loto6)))
        sys.exit()
    data = all_loto.data(6, int(sys.argv[1]))
    print(data.nums, data.bonus)


if __name__ == '__main__':
    main()