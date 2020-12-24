# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Python27\Lib\site-packages\CodeLibWrapper\TextTools\RandomUtils.py
# Compiled at: 2016-09-28 03:53:49
import random, string

class RandomUtils:
    u"""
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