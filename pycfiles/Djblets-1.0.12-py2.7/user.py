# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/webapi/resources/user.py
# Compiled at: 2019-06-12 01:17:17
"""Built-in resource representing the User model."""
from __future__ import unicode_literals
from django.contrib.auth.models import User
from djblets.util.decorators import augment_method_from
from djblets.webapi.resources.base import WebAPIResource
from djblets.webapi.resources.registry import register_resource_for_model

class UserResource(WebAPIResource):
    """A default resource for representing a Django User model."""
    model = User
    fields = {b'id': {b'type': int, 
               b'description': b'The numeric ID of the user.'}, 
       b'username': {b'type': str, 
                     b'description': b"The user's username."}, 
       b'first_name': {b'type': str, 
                       b'description': b"The user's first name."}, 
       b'last_name': {b'type': str, 
                      b'description': b"The user's last name."}, 
       b'fullname': {b'type': str, 
                     b'description': b"The user's full name (first and last)."}, 
       b'email': {b'type': str, 
                  b'description': b"The user's e-mail address"}, 
       b'url': {b'type': str, 
                b'description': b"The URL to the user's page on the site. This is deprecated and will be removed in a future version."}}
    uri_object_key = b'username'
    uri_object_key_regex = b"[A-Za-z0-9@\\._\\-\\'\\+]+"
    model_object_key = b'username'
    autogenerate_etags = True
    allowed_methods = ('GET', )

    def serialize_fullname_field(self, user, **kwargs):
        return user.get_full_name()

    def serialize_url_field(self, user, **kwargs):
        return user.get_absolute_url()

    def has_modify_permissions(self, request, user, *args, **kwargs):
        """Return whether or not the user can modify this object."""
        return request.user.is_authenticated() and user.pk == request.user.pk

    @augment_method_from(WebAPIResource)
    def get_list(self, *args, **kwargs):
        """Retrieve the list of users on the site."""
        pass


user_resource = UserResource()
register_resource_for_model(User, user_resource)