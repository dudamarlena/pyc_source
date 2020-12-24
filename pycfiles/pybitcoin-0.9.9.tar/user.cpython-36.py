# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pybitbucket/user.py
# Compiled at: 2016-12-28 18:40:02
# Size of source mod 2**32: 4080 bytes
from __future__ import unicode_literals
from pybitbucket.bitbucket import Bitbucket, BitbucketBase, Client

class User(BitbucketBase):
    id_attribute = 'username'
    resource_type = 'users'

    @staticmethod
    def is_type(data):
        return User.has_v2_self_url(data)

    def __init__(self, data, client=Client()):
        super(User, self).__init__(data, client=client)
        self.v1 = UserV1(data, client)

    @staticmethod
    def find_current_user(client=Client()):
        """
        A convenience method for finding the current user.
        In contrast to the pure hypermedia driven method on the Bitbucket
        class, this method returns a User object, instead of the
        generator.
        """
        return next(Bitbucket(client=client).userForMyself())

    @staticmethod
    def find_user_by_username(username, client=Client()):
        """
        A convenience method for finding a specific user.
        In contrast to the pure hypermedia driven method on the Bitbucket
        class, this method returns a User object, instead of the
        generator.
        """
        return next(Bitbucket(client=client).userByUsername(username=username))


class UserAdapter(object):

    def __init__(self, data, client=Client()):
        self.client = client
        if data.get('user') is not None:
            self.username = data['user'].get('username')
        else:
            self.username = data.get('username')

    def self(self):
        return User.find_user_by_username((self.username),
          client=(self.client))


class UserV1(BitbucketBase):
    id_attribute = 'username'
    links_json = '\n{\n  "_links": {\n    "plan": {\n      "href": "{+bitbucket_url}/1.0/users{/username}/plan"\n    },\n    "followers": {\n      "href": "{+bitbucket_url}/1.0/users{/username}/followers"\n    },\n    "events": {\n      "href": "{+bitbucket_url}/1.0/users{/username}/events"\n    },\n    "consumers": {\n      "href": "{+bitbucket_url}/1.0/users{/username}/consumers"\n    },\n    "emails": {\n      "href": "{+bitbucket_url}/1.0/users{/username}/emails"\n    },\n    "invitations": {\n      "href": "{+bitbucket_url}/1.0/users{/username}/invitations"\n    },\n    "privileges": {\n      "href": "{+bitbucket_url}/1.0/users{/username}/privileges"\n    },\n    "ssh-keys": {\n      "href": "{+bitbucket_url}/1.0/users{/username}/ssh-keys"\n    }\n  }\n}\n'

    @staticmethod
    def is_type(data):
        return data.get('user') is not None and data['user'].get('resource_uri') is not None and data['user'].get('username') is not None and data['user'].get('is_team') is False

    def __init__(self, data, client=Client()):
        self.data = data
        self.client = client
        if data.get('user'):
            self.__dict__.update(data['user'])
        if data.get('repositories'):
            self.repositories = [client.convert_to_object(r) for r in data['repositories']]
        self.v2 = UserAdapter(data, client)
        expanded_links = self.expand_link_urls(bitbucket_url=(client.get_bitbucket_url()),
          username=(self.v2.username))
        self.links = expanded_links.get('_links', {})
        self.add_remote_relationship_methods(expanded_links)


Client.bitbucket_types.add(User)
Client.bitbucket_types.add(UserV1)