# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ahqapiclient/resources/setting.py
# Compiled at: 2016-10-17 07:52:17
# Size of source mod 2**32: 639 bytes
from ahqapiclient.resources import Resource

class Settings(Resource):

    def __init__(self, http_client):
        super(Settings, self).__init__('/settings', http_client)

    def make_doc(self, settings):
        return {'settings': settings}

    def create_settings(self, settings):
        return self.post(path=self.rurl(), data=self.make_doc(settings))

    def update_settings(self, settings):
        return self.put(path=self.rurl(), data=self.make_doc(settings))

    def get_settings(self):
        return self.get(path=self.rurl())