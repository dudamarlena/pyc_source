# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ahqapiclient/resources/me.py
# Compiled at: 2016-10-17 07:52:17
# Size of source mod 2**32: 1166 bytes
from ahqapiclient.resources import Resource

class Me(Resource):

    def __init__(self, http_client):
        super(Me, self).__init__('/me', http_client)

    def reset_api_key(self):
        return self.put(path=self.rurl('apikey'))

    def set_password(self, password, repeated):
        return self.post(path=self.rurl('password'), data={'password': password, 
         'repeated': repeated})

    def set_twofactor_secret(self, secret):
        return self.post(path=self.rurl('twofactor'), data={'secret': secret})

    def delete_twofactor_secret(self):
        return self.delete(path=self.rurl('twofactor'))

    def login(self, twofactor=''):
        postdata = None
        if twofactor != '':
            postdata = {'token': twofactor}
        return self.post(path=self.rurl('login'), data=postdata)

    def logout(self):
        return self.post(path=self.rurl('logout'), data={})