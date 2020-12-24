# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Larco/Documents/Github/pyvenom/framework/venom/monkeypatches/datetime_json.py
# Compiled at: 2016-04-25 18:17:13
import datetime, time

class FakeDatetime(datetime.datetime):

    def __json__(self):
        timestamp = time.mktime(self.timetuple())
        return timestamp


datetime.datetime = FakeDatetime