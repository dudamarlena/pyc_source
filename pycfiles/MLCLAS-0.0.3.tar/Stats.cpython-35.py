# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mark/PycharmProjects/multi_label_classification/Utils/Stats.py
# Compiled at: 2016-04-29 03:33:25
# Size of source mod 2**32: 384 bytes


class Aggregate:

    @staticmethod
    def intersection(a, b):
        inter = 0
        for i in a:
            if i in b:
                inter += 1

        return inter

    @staticmethod
    def sum(a, b):
        return len(a) + len(b) - Aggregate.intersection(a, b)

    @staticmethod
    def symDifference(a, b):
        return len(a) + len(b) - 2 * Aggregate.intersection(a, b)