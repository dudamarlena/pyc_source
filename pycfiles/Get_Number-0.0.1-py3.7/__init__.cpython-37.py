# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Get_Number\__init__.py
# Compiled at: 2019-07-27 10:10:39
# Size of source mod 2**32: 1308 bytes
import random

def Get_Nr_Num(range, amount):
    if isinstance(range, list):
        return '错误：range(minNumber, maxNumber)'
    if range[0] > range[1]:
        return '错误：范围错误'
    if range[1] - range[0] < amount:
        return '错误：范围过小'
    List = []
    i = 0
    while i < amount:
        Num = random.randint(range[0], range[1])
        if Num not in List:
            List.append(Num)
            i += 1
        continue

    return List


def Get_Prime_Num(number, all=False):
    i = 0
    List = []
    while len(List) < number:
        if i != 1:
            if i != 0:
                Bool = False
                Range = range(1, i + 1)
                for n in Range:
                    if i % n == 0:
                        if n != 1:
                            if n != i:
                                List.remove(i)
                                break
                    if i not in List:
                        List.append(i)

        i += 1

    if all:
        return List
    return List[(number - 1)]