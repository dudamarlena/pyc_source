# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pilar/robocomp/components/learnbot/learnbot_dsl/Clients/Devices/Base.py
# Compiled at: 2019-04-07 11:14:14


class Base:
    """
    Base is the differential base of the robot.
    """
    __Sadv = 0
    __Srot = 0

    def __init__(self, _callFunction):
        self.__callDevice = _callFunction

    def move(self, _Sadv, _Srot):
        self.__Sadv, self.__Srot = _Sadv, _Srot
        self.__callDevice(_Sadv, _Srot)

    def adv(self):
        return self.__Sadv

    def rot(self):
        return self.__Srot