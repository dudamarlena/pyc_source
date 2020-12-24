# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/myfact/fact.py
# Compiled at: 2019-05-19 04:31:51
# Size of source mod 2**32: 339 bytes
"""myface moudle"""

def factorialLYL(num):
    """
        返回给定数字的阶乘值

        :arg num: 我们将计算其阶乘的整数值

        :return: 阶乘值，若传递的参数为负数，则为-1
        """
    if num >= 0:
        if num == 0:
            return 1
        return num * factorialLYL(num - 1)
    return -1