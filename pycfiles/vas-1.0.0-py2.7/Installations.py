# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/web_server/Installations.py
# Compiled at: 2012-11-01 11:36:39
import vas.shared.Installations

class Installations(vas.shared.Installations.Installations):
    """Used to enumerate, create, and delete Web Server installations

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """

    def __init__(self, client, location):
        super(Installations, self).__init__(client, location, Installation)


class Installation(vas.shared.Installations.Installation):
    """A Web Server installation

    :ivar `vas.web_server.Groups.Group`                         group:              The group that contains the
                                                                                    installation
    :ivar `vas.web_server.InstallationImages.InstallationImage` installation_image: The installation image that was used
                                                                                    to create the installation
    :ivar list                                                  instances:          The instances that are using the
                                                                                    installation
    :ivar `vas.shared.Security.Security`                        security:           The resource's security
    :ivar str                                                   version:            The installation's version
    """

    @property
    def instances(self):
        self.__instances = self.__instances or self._create_resources_from_links('group-instance', Instance)
        return self.__instances

    def __init__(self, client, location):
        super(Installation, self).__init__(client, location, InstallationImage, Group)

    def reload(self):
        """Reloads the installation's details from the server"""
        super(Installation, self).reload()
        self.__instances = None
        return


from vas.web_server.Groups import Group
from vas.web_server.Instances import Instance
from vas.web_server.InstallationImages import InstallationImage