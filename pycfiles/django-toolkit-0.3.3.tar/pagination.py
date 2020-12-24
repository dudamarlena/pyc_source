# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ahayes/.virtualenvs/roicrm-django1.7/local/lib/python2.7/site-packages/django_toolkit/pagination.py
# Compiled at: 2013-11-26 18:51:11
from __future__ import absolute_import
from django.core.paginator import Paginator, Page
import collections

class RangeBasedPaginator(Paginator):

    def __init__(self, object_count, *args, **kwargs):
        """
        @todo Creating a range of values is really a waste of cycles...
        """
        object_list = range(1, object_count + 1)
        super(RangeBasedPaginator, self).__init__(object_list, *args, **kwargs)