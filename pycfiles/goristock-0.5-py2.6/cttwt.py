# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/grs/cttwt.py
# Compiled at: 2011-10-05 02:42:28
import time, datetime

class TWTime(object):
    """ Transform localtime to Taiwan time in UTF+8
      轉換當地時間到台灣時間 UTF+8
  """

    def __init__(self, tz=8):
        try:
            self.TimeZone = float(tz)
        except:
            self.TimeZone = 8

    @property
    def now(self):
        u""" Display Taiwan Time now
        顯示台灣此刻時間
    """
        localtime = datetime.datetime.now()
        return localtime + datetime.timedelta(hours=time.timezone / 60 / 60 + self.TimeZone)

    @property
    def date(self):
        u""" Display Taiwan date now
        顯示台灣此刻日期
    """
        localtime = datetime.date.today()
        return localtime + datetime.timedelta(hours=time.timezone / 60 / 60 + self.TimeZone)

    @property
    def localtime(self):
        u""" Display localtime now
        顯示當地此刻時間
    """
        return datetime.datetime.now()

    @property
    def localdate(self):
        u""" Display localdate now
        顯示當地此刻日期
    """
        return datetime.date.today()