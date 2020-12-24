# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/portlet/recentactivity/utils.py
# Compiled at: 2010-05-19 10:20:52


def compute_time(absolute_seconds):
    absolute_minutes = absolute_seconds / 60
    days = absolute_minutes / 1440
    hours = absolute_minutes / 60 - days * 24
    minutes = absolute_minutes - hours * 60 - days * 24 * 60
    return {'days': days, 'hours': hours, 'minutes': minutes}