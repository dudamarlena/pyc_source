# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\time\TimeUtil.py
# Compiled at: 2019-08-04 22:14:48
# Size of source mod 2**32: 2096 bytes
import time, datetime, string

class TimeUtil:
    __doc__ = '\n    一个获取时间的工具类\n    该工具类可以指定输出格式、可以指定时间偏移\n    '

    @property
    def timeStamp(self):
        return time.time()

    @property
    def currentTimeString(self):
        return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

    def currentTime(self, ft='%Y-%m-%d %H:%M:%S'):
        return time.strftime(ft, time.localtime(time.time()))

    def getTargetWeeks(self, weeks=0, ft='%Y-%m-%d %H:%M:%S'):
        nowTime = datetime.datetime.now()
        targetTime = nowTime + datetime.timedelta(weeks=weeks)
        return targetTime.strftime(ft)

    def getTargetDays(self, days=0, ft='%Y-%m-%d %H:%M:%S'):
        nowTime = datetime.datetime.now()
        targetTime = nowTime + datetime.timedelta(days=days)
        return targetTime.strftime(ft)

    def getTargetHours(self, hours=0, ft='%Y-%m-%d %H:%M:%S'):
        nowTime = datetime.datetime.now()
        targetTime = nowTime + datetime.timedelta(hours=hours)
        return targetTime.strftime(ft)

    def getTargetMinutes(self, minutes=0, ft='%Y-%m-%d %H:%M:%S'):
        nowTime = datetime.datetime.now()
        targetTime = nowTime - datetime.timedelta(minutes=minutes)
        return targetTime.strftime(ft)

    def getTargetSeconds(self, seconds=0, ft='%Y-%m-%d %H:%M:%S'):
        nowTime = datetime.datetime.now()
        targetTime = nowTime + datetime.timedelta(seconds=seconds)
        return targetTime.strftime(ft)