# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\shaonutil\stats.py
# Compiled at: 2019-11-29 03:13:34
# Size of source mod 2**32: 889 bytes
"""Statistics"""

def counter(li, number):
    num = 0
    for c in li:
        if c == number:
            num += 1
        return num


def occurance_dic(li):
    dic = {}
    for number in li:
        dic[number] = counter(li, number)
    else:
        return dic


def mean(li):
    """Avearage or mean of elements - shaonutil.stats.mean(list of numbers)"""
    return sum(li) / len(li)


def median(li):
    """Median of elements - shaonutil.stats.median(list of numbers)"""
    n = len(li)
    li.sort()
    if n % 2 == 0:
        median1 = li[(n // 2)]
        median2 = li[(n // 2 - 1)]
        median = (median1 + median2) / 2
    else:
        median = li[(n // 2)]
    return median


def mode(li):
    """Mode of elements - shaonutil.stats.mode(list of numbers)"""
    n = len(li)
    data = occurance_dic(li)
    mode = [k for k, v in data.items() if v == max(list(data.values()))]
    if len(mode) == n:
        raise ValueError('No mode found !')
    else:
        return mode


if __name__ == '__main__':
    pass