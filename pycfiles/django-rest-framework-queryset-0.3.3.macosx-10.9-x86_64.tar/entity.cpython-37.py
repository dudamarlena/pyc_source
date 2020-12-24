# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jlin/virtualenvs/django-rest-framework-queryset/lib/python3.7/site-packages/rest_framework_queryset/entity.py
# Compiled at: 2019-05-08 19:46:33
# Size of source mod 2**32: 149 bytes
import requests

class Entity(dict):

    def __init__(self, url):
        url = url

    def save(self):
        requests.put((self.url), data=self)