# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synapseclient/team.py
# Compiled at: 2020-03-23 17:17:03
# Size of source mod 2**32: 3765 bytes
"""
*****
Teams
*****
"""
from synapseclient.core.models.dict_object import DictObject

class UserProfile(DictObject):
    __doc__ = '\n    Information about a Synapse user.  In practice the constructor is not called directly by the client.\n    \n    :param ownerId: A foreign key to the ID of the \'principal\' object for the user.\n    :param uri: The Uniform Resource Identifier (URI) for this entity.\n    :param etag: Synapse employs an Optimistic Concurrency Control (OCC) scheme to handle concurrent updates.\n     Since the E-Tag changes every time an entity is updated it is used to detect when a client\'s current representation\n     of an entity is out-of-date.\n    :param firstName: This person\'s given name (forename)\n    :param lastName: This person\'s family name (surname)\n    :param emails: The list of user email addresses registered to this user.\n    :param userName: A name chosen by the user that uniquely identifies them.\n    :param summary: A summary description about this person\n    :param position: This person\'s current position title\n    :param location: This person\'s location\n    :param industry: "The industry/discipline that this person is associated with\n    :param company: This person\'s current affiliation\n    :param profilePicureFileHandleId: The File Handle ID of the user\'s profile picture.\n    :param url: A link to more information about this person\n    :param notificationSettings: An object of type :py:class:`org.sagebionetworks.repo.model.message.Settings`\n     containing the user\'s preferences regarding when email notifications should be sent\n    '

    def __init__(self, **kwargs):
        super(UserProfile, self).__init__(kwargs)


class UserGroupHeader(DictObject):
    __doc__ = "\n    Select metadata about a Synapse principal.  In practice the constructor is not called directly by the client.\n    \n    :param ownerId: A foreign key to the ID of the 'principal' object for the user.\n    :param firstName: First Name\n    :param lastName: Last Name\n    :param userName: A name chosen by the user that uniquely identifies them.\n    :param email:   User's current email address\n    :param isIndividual: True if this is a user, false if it is a group\n    "

    def __init__(self, **kwargs):
        super(UserGroupHeader, self).__init__(kwargs)


class Team(DictObject):
    __doc__ = '\n    Represents a `Synapse Team <http://docs.synapse.org/rest/org/sagebionetworks/repo/model/Team.html>`_.\n    User definable fields are:\n    \n    :param icon:          fileHandleId for icon image of the Team\n    :param description:   A short description of this Team.\n    :param name:          The name of the Team.\n    :param canPublicJoin: true for teams which members can join without an invitation or approval\n    '

    def __init__(self, **kwargs):
        super(Team, self).__init__(kwargs)

    @classmethod
    def getURI(cls, id):
        return '/team/%s' % id

    def postURI(self):
        return '/team'

    def putURI(self):
        return '/team'

    def deleteURI(self):
        return '/team/%s' % self.id

    def getACLURI(self):
        return '/team/%s/acl' % self.id

    def putACLURI(self):
        return '/team/acl'


class TeamMember(DictObject):
    __doc__ = "\n    Contains information about a user's membership in a Team.  In practice the constructor is not called directly by\n     the client.\n    \n    :param teamId:  the ID of the team\n    :param member:  An object of type :py:class:`org.sagebionetworks.repo.model.UserGroupHeader` describing the member\n    :param isAdmin: Whether the given member is an administrator of the team\n    \n   "

    def __init__(self, **kwargs):
        if 'member' in kwargs:
            kwargs['member'] = UserGroupHeader(**kwargs['member'])
        super(TeamMember, self).__init__(kwargs)