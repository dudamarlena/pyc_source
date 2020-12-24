# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/gemfire/GemFire.py
# Compiled at: 2012-11-01 11:37:44
from vas.util.LinkUtils import LinkUtils

class GemFire(object):
    """The entry point to the API for administering GemFire

    :ivar `vas.gemfire.ApplicationCodeImages`   application_code_images:    The collection of application code images
    :ivar `vas.gemfire.Groups`                  groups:                     The collection of groups
    :ivar `vas.gemfire.InstallationImages`      installation_images:        The collection of installation images
    :ivar `vas.gemfire.Nodes`                   nodes:                      The collection of nodes
    """

    @property
    def application_code_images(self):
        return self.__application_code_images

    @property
    def groups(self):
        return self.__groups

    @property
    def installation_images(self):
        return self.__installation_images

    @property
    def nodes(self):
        return self.__nodes

    def __init__(self, client, location):
        self.__client = client
        self.__location = location
        json = client.get(location)
        self.__application_code_images = ApplicationCodeImages(client, LinkUtils.get_link_href(json, 'application-code-images'))
        self.__groups = Groups(client, LinkUtils.get_link_href(json, 'groups'))
        self.__installation_images = InstallationImages(client, LinkUtils.get_link_href(json, 'installation-images'))
        self.__nodes = Nodes(client, LinkUtils.get_link_href(json, 'nodes'))

    def __repr__(self):
        return ('{}(client={}, location={})').format(self.__class__.__name__, self.__client, repr(self.__location))

    def __str__(self):
        return ('<{}>').format(self.__class__.__name__)


from vas.gemfire.ApplicationCodeImages import ApplicationCodeImages
from vas.gemfire.Groups import Groups
from vas.gemfire.InstallationImages import InstallationImages
from vas.gemfire.Nodes import Nodes