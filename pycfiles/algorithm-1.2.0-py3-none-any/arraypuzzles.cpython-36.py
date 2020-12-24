# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\algos\arrays\arraypuzzles.py
# Compiled at: 2019-04-22 02:19:19
# Size of source mod 2**32: 910 bytes
import numpy as np

def trapped_rainwater(arr_tank):
    """
    The elements of the array are heights of walls.
    If it rains, how much rain water will be trapped?
    I will answer this question for any array you give me.
    """
    prev_ht = arr_tank[0]
    drops = []
    goingdown = True
    area = 0
    for ht in arr_tank[1:]:
        for i in range(len(drops)):
            drops[i] += 1

        if ht < prev_ht:
            goingdown = True
            for _ in range(prev_ht - ht):
                drops.append(0)

        else:
            if ht > prev_ht:
                goingdown = False
                for _ in range(ht - prev_ht):
                    if len(drops) > 0:
                        area += drops.pop()

        prev_ht = ht
        print(str(drops))

    return area


if __name__ == '__main__':
    trapped_rainwater([5, 2, 1, 2, 1, 5])