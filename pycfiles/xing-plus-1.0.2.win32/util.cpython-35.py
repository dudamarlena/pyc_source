# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Anaconda3\Lib\site-packages\xing\util.py
# Compiled at: 2016-01-16 19:19:25
# Size of source mod 2**32: 3348 bytes
from datetime import datetime, timedelta
import math, pandas

def timeType(base=None):
    """장 전,후 시간을 반환

                :param base: 기준일시
                :type base: datetime
                :return: 기준일시에 맞는 타입문자를 반환

                        BEFORE(장시작 전),SHOWTIME(장 운영시간),AFTER(장종료 후)

                ::

                        timeType()
                        timeType(datetime.today())
        """
    today = base if base else datetime.today()
    mainStart = today.replace(hour=8, minute=50, second=0, microsecond=0)
    mainEnd = today.replace(hour=15, minute=0, second=0, microsecond=0)
    if today.weekday() < 5:
        if today >= mainStart and today <= mainEnd:
            return 'SHOWTIME'
        if today < mainStart:
            return 'BEFORE'
        if today > mainEnd:
            return 'AFTER'
    else:
        return 'NONE'


def today():
    """오늘 날자를 yyyymmdd 형태로 반환

                ::

                        today() # 20160101
        """
    return datetime.today().strftime('%Y%m%d')


def latestBusinessDay():
    """가장 최근 영업일을 yyyymmdd 형태로 반환

                ::

                        latestBusinessDay()     # 20160104
        """
    baseday = datetime.today()
    if baseday.weekday() > 4:
        while baseday.weekday() > 4:
            baseday = baseday - timedelta(days=1)

    return baseday.strftime('%Y%m%d')