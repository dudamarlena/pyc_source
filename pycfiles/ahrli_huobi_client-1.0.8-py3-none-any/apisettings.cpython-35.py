# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ahqapiclient/resources/apisettings.py
# Compiled at: 2017-05-05 07:20:01
# Size of source mod 2**32: 596 bytes
from ahqapiclient.resources import Resource

class ApiSettings(Resource):

    def __init__(self, http_client):
        super(ApiSettings, self).__init__('/settings/api', http_client)

    def make_doc(self, settings, identifier):
        return {'settings': settings, 
         'id': identifier}

    def update_settings(self, settings, identifier):
        return self.put(path=self.rurl(), data=self.make_doc(settings, identifier))

    def get_settings(self, identifier):
        return self.get(path=self.rurl() + '/' + identifier)