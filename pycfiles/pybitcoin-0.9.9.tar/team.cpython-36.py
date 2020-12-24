# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pybitbucket/team.py
# Compiled at: 2016-12-28 18:40:02
# Size of source mod 2**32: 1239 bytes
from __future__ import unicode_literals
from pybitbucket.bitbucket import Bitbucket, BitbucketBase, Client, Enum

class TeamRole(Enum):
    ADMIN = 'admin'
    CONTRIBUTOR = 'contributor'
    MEMBER = 'member'


class Team(BitbucketBase):
    id_attribute = 'username'
    resource_type = 'teams'

    @staticmethod
    def is_type(data):
        return Team.has_v2_self_url(data)

    @staticmethod
    def find_teams_for_role(role=TeamRole.ADMIN, client=Client()):
        """
        A convenience method for finding teams by the user's role.
        The method is a generator Team objects.
        """
        TeamRole(role)
        return Bitbucket(client=client).teamsForRole(role=role)

    @staticmethod
    def find_team_by_username(username, client=Client()):
        """
        A convenience method for finding a specific team.
        In contrast to the pure hypermedia driven method on the Bitbucket
        class, this method returns a User object, instead of the
        generator.
        """
        return next(Bitbucket(client=client).teamByUsername(username=username))


Client.bitbucket_types.add(Team)