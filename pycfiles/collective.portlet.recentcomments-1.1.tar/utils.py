# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/portlet/recentactivity/utils.py
# Compiled at: 2010-05-19 10:20:52


def compute_time(absolute_seconds):
    absolute_minutes = absolute_seconds / 60
    days = absolute_minutes / 1440
    hours = absolute_minutes / 60 - days * 24
    minutes = absolute_minutes - hours * 60 - days * 24 * 60
    return {'days': days, 'hours': hours, 'minutes': minutes}