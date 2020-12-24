# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/web_server/Groups.py
# Compiled at: 2012-11-01 11:36:39
import vas.shared.Groups
from vas.util.LinkUtils import LinkUtils

class Groups(vas.shared.Groups.Groups):
    """Used to enumerate, create, and delete Web Server groups

    :ivar `vas.shared.Security.Security`    security:   The security configuration for the collection
    """

    def __init__(self, client, location):
        super(Groups, self).__init__(client, location, Group)


class Group(vas.shared.Groups.Group):
    """A Web Server group

    :ivar `vas.web_server.Installations.Installations`  installations:  The group's installations
    :ivar `vas.web_server.Instances.Instances`          instances:      The groups' instances
    :ivar str                                           name:           The group's name
    :ivar list                                          nodes:          The group's nodes
    :ivar `vas.shared.Security`                         security:       The resource's security
    """
    __instances = None

    @property
    def instances(self):
        self.__instances = self.__instances or Instances(self._client, self.__instances_location)
        return self.__instances

    def __init__(self, client, location):
        super(Group, self).__init__(client, location, Node, Installations)
        self.__instances_location = LinkUtils.get_link_href(self._details, 'group-instances')


from vas.web_server.Installations import Installations
from vas.web_server.Instances import Instances
from vas.web_server.Nodes import Node