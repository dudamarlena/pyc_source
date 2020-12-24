# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lotonumber/loto_basic.py
# Compiled at: 2017-09-11 03:01:43
# Size of source mod 2**32: 1811 bytes


class LotoBasic:

    def __init__(self, round, numbers, bonus_numbers, prize_nums, amount_nums, carry_over=0):
        """
        round: 回
        numbers: 当選番号のリスト
        bonus_numbers: ボーナス数字のリスト
        prize_nums: 当選者数のリスト
        amount_nums: 当選金額のリスト
        carry_over: キャリーオーバーの金額
        """
        self._round = round
        self._numbers = numbers
        self._bn = bonus_numbers
        self._pn = prize_nums
        self._an = amount_nums
        self._co = carry_over

    @property
    def nums(self):
        return self._numbers

    @property
    def bonus(self):
        return self._bn

    @property
    def priznum(self):
        return self._pn

    @property
    def amounts(self):
        return self._an

    @property
    def c_over(self):
        return self._co

    def __str__(self):
        bn_str = '[' + ','.join([str(i) for i in self._bn]) + ']'
        return '({round}) {numbers} {bn} PN[{pn}] AN[{an}] CO({co})'.format(round=(self._round), numbers=(','.join([str(i) for i in self._numbers])),
          bn=bn_str,
          pn=(','.join([str(i) for i in self._pn])),
          an=(','.join([str(i) for i in self._an])),
          co=(self._co))


if __name__ == '__main__':
    loto7 = LotoBasic(229, [2, 3, 9, 30, 33, 36, 37], [1, 32], [10, 20, 30, 40, 50, 60, 70], [100, 200, 300, 400, 500, 600, 700], 7777777)
    print(loto7)