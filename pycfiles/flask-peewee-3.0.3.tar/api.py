# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/charles/code/flask-peewee/example/api.py
# Compiled at: 2018-01-17 11:50:43
from flask_peewee.rest import RestAPI, RestResource, UserAuthentication, AdminAuthentication, RestrictOwnerResource
from app import app
from auth import auth
from models import User, Message, Relationship
user_auth = UserAuthentication(auth)
admin_auth = AdminAuthentication(auth)
api = RestAPI(app, default_auth=user_auth)

class UserResource(RestResource):
    exclude = ('password', 'email')


class MessageResource(RestrictOwnerResource):
    owner_field = 'user'
    include_resources = {'user': UserResource}


class RelationshipResource(RestrictOwnerResource):
    owner_field = 'from_user'
    include_resources = {'from_user': UserResource, 
       'to_user': UserResource}
    paginate_by = None


api.register(User, UserResource, auth=admin_auth)
api.register(Relationship, RelationshipResource)
api.register(Message, MessageResource)