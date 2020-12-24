# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\SimpleMathCalc\Mode_number.py
# Compiled at: 2019-04-09 12:17:55
# Size of source mod 2**32: 676 bytes


def Mode_number(List1):
    count_dict = dict()
    for item in List1:
        if item in count_dict:
            count_dict[item] += 1
        else:
            count_dict[item] = 1

    print(count_dict)
    print(sorted((count_dict.items()), key=(lambda item: item[1])))
    z = list(sorted((count_dict.items()), key=(lambda item: item[1])))
    output = str(z[(-1)]) + "The first number is the mode and second number is it's frequency"
    return output