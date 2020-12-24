# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twisting/progress_info.py
# Compiled at: 2009-03-28 16:00:34
"""ProgressionInfo is a tools to extract progression informations :
    - Speed number of iteration per seconds
    - Remaining time
"""
from datetime import datetime
from decimal import Decimal

class ProgressInfo(object):

    def __init__(self, item_count=0):
        """
        """
        self.__last_timestamp = datetime.now()
        self.__speed = 0.0
        self.__items_bucket = list()
        self.item_count = item_count
        self.speed_text = ''
        self.progress_text = ''

    def clear_bucket(self):
        """
        """
        self.__items_bucket = list()

    def __compute_speed(self, index_):
        """
        """
        timestamp_ = datetime.now()
        delta_ = timestamp_ - self.__last_timestamp
        self.__last_timestamp = timestamp_
        self.__items_bucket.insert(0, delta_.microseconds)
        if len(self.__items_bucket) < 5:
            return
        try:
            s_time_ = sum(self.__items_bucket[-index_:]) / 1000000.0
            self.__speed = index_ / s_time_
        except:
            pass

    def __get_remaining_info(self, index_):
        """
        """
        if self.__speed <= 0 or len(self.__items_bucket) < 5:
            return ''
        remaining_items_ = self.item_count - index_
        remaining_seconds_ = int(remaining_items_ / self.__speed)
        hours = remaining_seconds_ / 3600
        remaining_seconds_ -= 3600 * hours
        minutes = remaining_seconds_ / 60
        remaining_seconds_ -= 60 * minutes
        seconds = remaining_seconds_
        remaining_info = '%02d' % hours
        remaining_info += ':%02d' % minutes
        remaining_info += ':%02d' % seconds
        remaining_info += ' Remaining'
        return remaining_info

    def update(self, item_count=None, index_=None):
        """
        """
        if index_ == None or index_ >= len(self.__items_bucket):
            index_ = len(self.__items_bucket) - 1
        if item_count:
            self.item_count = item_count
        self.__compute_speed(index_)
        if self.__speed > 0:
            self.speed_text = '%.2f items/s' % self.__speed
        else:
            self.speed_text = ''
        self.progress_text = '%s  %s' % (
         self.speed_text,
         self.__get_remaining_info(index_))
        return