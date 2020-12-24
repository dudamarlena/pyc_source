# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ppd-03020186/PycharmProjects/cocoNLP/cocoNLP/config/basic/time_nlp/RangeTimeEnum.py
# Compiled at: 2018-12-17 07:52:43
# Size of source mod 2**32: 519 bytes


class RangeTimeEnum:
    day_break = 3
    early_morning = 8
    morning = 10
    noon = 12
    afternoon = 15
    night = 18
    lateNight = 20
    midNight = 23


if __name__ == '__main__':
    print(RangeTimeEnum.afternoon)