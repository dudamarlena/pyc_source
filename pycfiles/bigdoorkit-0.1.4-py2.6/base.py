# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/bigdoorkit/resources/base.py
# Compiled at: 2010-07-29 15:08:39
from bigdoorkit.client import Client
from bigdoorkit.exc import MissingParentDetails
from datetime import datetime
from types import MethodType

def clean_obj_keys(data):
    """JSON returns unicode keys which cannot be passed to
    __init__ methods directly. Here we convert the keys to strings.
    """
    return dict([ (str(k), v) for (k, v) in data.items() ])


class BDResource(object):
    endpoint = None
    parent_class = None
    parent_id_attr = None

    def __init__(self, created_timestamp, modified_timestamp, **kw):
        self.id = kw.get('id', None)
        self.pub_title = kw.get('pub_title', None)
        self.pub_description = kw.get('pub_description', None)
        self.end_user_title = kw.get('end_user_title', None)
        self.end_user_description = kw.get('end_user_description', None)
        if isinstance(created_timestamp, (int, float)):
            created_timestamp = datetime.fromtimestamp(created_timestamp)
        self.created_timestamp = created_timestamp
        if isinstance(modified_timestamp, (int, float)):
            modified_timestamp = datetime.fromtimestamp(modified_timestamp)
        self.modified_timestamp = modified_timestamp
        self.delete = MethodType(self.__instance_delete, self, self.__class__)
        self._undefined_kw = kw
        return

    @classmethod
    def all(cls, client):
        """Retrieves all of the available objects"""
        if cls.parent_class and not getattr(cls, cls.parent_id_attr, None):
            raise MissingParentDetails()
        endpoint = cls.endpoint
        if cls.parent_class:
            endpoint = '%s/%s/%s' % (cls.parent_class.endpoint,
             getattr(cls, cls.parent_id_attr),
             cls.endpoint)
        data = client.get(endpoint)
        return [ cls(**clean_obj_keys(i)) for i in data[0] ]

    @classmethod
    def get(cls, id, client):
        """Retrieves an object with the given `id`, using the `client` object
        if passed.
        """
        data = client.get('%s/%s' % (cls.endpoint, id))
        return cls(**clean_obj_keys(data[0]))

    def save(self, client):
        """Create or Update this object.

        If the object has an id, this method will try to PUT, otherwise
        the HTTP method will be POST.
        """
        if not self.id:
            client.post(self.endpoint, self.to_dict())
        else:
            data = client.put(self.endpoint, self.to_dict())
            self = self.__class__(**data)

    def __class_delete(cls, id, client=None):
        """Deletes an object identified by `id`"""
        if client is None:
            client = get_client()
        client.delete(cls.endpoint, id)
        return

    delete = classmethod(__class_delete)

    def __instance_delete(self, obj, client=None):
        return self.__class_delete(self.id, client)