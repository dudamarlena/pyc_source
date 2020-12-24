# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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