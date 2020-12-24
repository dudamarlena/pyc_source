# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/packagetrack/data.py
# Compiled at: 2010-06-20 17:42:07


class TrackingInfo(object):

    def __init__(self, delivery_date, status, last_update):
        self.delivery_date = delivery_date
        self.status = status
        self.last_update = last_update

    def __repr__(self):
        return '<TrackingInfo(delivery_date=%r, status=%r, last_update=%r)>' % (
         self.delivery_date, self.status, self.last_update)