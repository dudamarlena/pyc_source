# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ahqapiclient/resources/user.py
# Compiled at: 2016-10-17 07:52:17
# Size of source mod 2**32: 1993 bytes
from ahqapiclient.resources import Resource

class User(Resource):

    def __init__(self, http_client):
        super(User, self).__init__('/users', http_client)

    def create_user(self, uid, first_name, last_name, customer, mail, role, imap_access, web_access, api_access):
        return self.post(path=self.rurl(), data={'uid': uid, 
         'first_name': first_name, 
         'last_name': last_name, 
         'customer': customer, 
         'mail': mail, 
         'role': role, 
         'imap_access': imap_access, 
         'web_access': web_access, 
         'api_access': api_access})

    def get_user(self, uid):
        return self.get(path=self.rurl(uid))

    def update_user(self, uid, first_name, last_name, customer, mail, role, imap_access, web_access, api_access):
        return self.put(path=self.rurl(uid), data={'first_name': first_name, 
         'last_name': last_name, 
         'customer': customer, 
         'mail': mail, 
         'role': role, 
         'imap_access': imap_access, 
         'web_access': web_access, 
         'api_access': api_access})

    def delete_user(self, uid):
        return self.delete(path=self.rurl(uid))

    def get_users(self, limit=10, offset=0, query='', raw=False):
        return self.get(path=self.rurl(), params={'limit': limit, 
         'offset': offset, 
         'query': query}, raw=raw)
        return self.get(path=self.rurl())

    def reset_password(self, uid):
        return self.put(path=self.rurl('%s/password' % uid))

    def reset_apikey(self, uid):
        return self.put(path=self.rurl('%s/apikey' % uid))