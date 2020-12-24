# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Python27\Lib\site-packages\CodeLibWrapper\TextTools\RandomUtils.py
# Compiled at: 2016-09-28 03:53:49
import random, string

class RandomUtils:
    """
    随机数据生成工具类
    """

    def __init__(self):
        pass

    @staticmethod
    def genrandomstring(length):
        u"""
        随机出数字的个数
        :param length:
        :return:
        """
        numofnum = random.randint(1, length - 1)
        numofletter = length - numofnum
        slcnum = [ random.choice(string.digits) for i in range(numofnum) ]
        slcletter = [ random.choice(string.ascii_letters) for i in range(numofletter) ]
        slcchar = slcnum + slcletter
        random.shuffle(slcchar)
        return ('').join([ i for i in slcchar ])