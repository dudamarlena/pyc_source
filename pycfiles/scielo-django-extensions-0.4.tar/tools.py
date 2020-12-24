# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gustavofonseca/prj/github/scielo-django-extensions/scielo_extensions/tools.py
# Compiled at: 2012-03-21 14:32:09
from django.core.paginator import EmptyPage
from django.core.paginator import Paginator
from django.conf import settings

def get_paginated(items, page_num, items_per_page=settings.PAGINATION__ITEMS_PER_PAGE):
    """
    Wraps django core pagination object
    """
    paginator = Paginator(items, items_per_page)
    try:
        page_num = int(page_num)
    except ValueError:
        raise TypeError('page_num must be integer')

    try:
        paginated = paginator.page(page_num)
    except EmptyPage:
        paginated = paginator.page(paginator.num_pages)

    return paginated