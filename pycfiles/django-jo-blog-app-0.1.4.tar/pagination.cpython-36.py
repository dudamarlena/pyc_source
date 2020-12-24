# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/maluki/blog/django_blog/blog_project/blog/api/pagination.py
# Compiled at: 2019-07-26 05:23:03
# Size of source mod 2**32: 201 bytes
from rest_framework.pagination import PageNumberPagination

class CustomResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 200