# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/crawlib-project/crawlib/tests/dummy_site_crawler/mongo_backend/s2_music/entity_base.py
# Compiled at: 2019-12-27 11:32:44
# Size of source mod 2**32: 384 bytes
import requests
from crawlib.entity.mongodb.entity import MongodbEntitySingleStatus

class MusicWebsiteEntity(MongodbEntitySingleStatus):
    meta = {'abstract': True}

    def build_request(self, url, **kwargs):
        request = url
        return request

    def send_request(self, request, **kwargs):
        return requests.get(request)