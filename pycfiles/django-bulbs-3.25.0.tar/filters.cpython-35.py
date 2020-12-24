# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/poll/filters.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 207 bytes
from django.utils import timezone
from elasticsearch_dsl.filter import Range

def Closed():
    end_date_params = {'lte': timezone.now()}
    return Range(end_date=end_date_params)