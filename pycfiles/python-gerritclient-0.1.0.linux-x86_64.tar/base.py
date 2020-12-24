# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/machin/.virtualenvs/twine/lib/python2.7/site-packages/gerritclient/v1/base.py
# Compiled at: 2017-08-06 08:02:33
import abc, six
from requests import utils as requests_utils
from gerritclient import client

@six.add_metaclass(abc.ABCMeta)
class BaseV1Client(object):

    @abc.abstractproperty
    def api_path(self):
        pass

    def __init__(self, connection=None):
        if connection is None:
            config = client.get_settings()
            connection = client.connect(**config)
        self.connection = connection
        return


@six.add_metaclass(abc.ABCMeta)
class BaseV1ClientCreateEntity(BaseV1Client):

    def create(self, entity_id, data=None):
        """Create a new entity."""
        data = data if data else {}
        request_path = ('{api_path}{entity_id}').format(api_path=self.api_path, entity_id=requests_utils.quote(entity_id, safe=''))
        return self.connection.put_request(request_path, json_data=data)