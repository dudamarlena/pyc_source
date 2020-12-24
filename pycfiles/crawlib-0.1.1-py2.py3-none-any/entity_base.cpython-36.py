# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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