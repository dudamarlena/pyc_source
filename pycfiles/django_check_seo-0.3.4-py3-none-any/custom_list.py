# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kapt/workspace/django-check-seo/django_check_seo/checks/custom_list.py
# Compiled at: 2020-01-28 11:13:47


class CustomList:

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name', None)
        self.settings = kwargs.get('settings', None)
        self.found = kwargs.get('found', None)
        self.searched_in = kwargs.get('searched_in', [])
        self.description = kwargs.get('description', None)
        return