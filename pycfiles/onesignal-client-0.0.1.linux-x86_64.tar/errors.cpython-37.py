# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grelek/projects/onesignal-notifications/venv/lib/python3.7/site-packages/onesignal/errors.py
# Compiled at: 2019-03-19 08:10:19
# Size of source mod 2**32: 100 bytes


class OneSignalAPIError(BaseException):
    __doc__ = 'OneSignal API request was not successful'