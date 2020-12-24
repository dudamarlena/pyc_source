# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/web_server/WebServer.py
# Compiled at: 2012-11-01 11:36:39
from vas.util.LinkUtils import LinkUtils

class WebServer(object):
    """The entry point to the API for administering vFabric Web Server

    :ivar `vas.web_server.Groups.Groups`                            groups:                 The Web Server groups
    :ivar `vas.web_server.InstallationImages.InstallationImages`    installation_images:    The Web Server installation
                                                                                            images
    :ivar `vas.web_server.Nodes.Nodes`                              nodes:                  The Web Server nodes
    """

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
        self.__groups = Groups(client, LinkUtils.get_link_href(json, 'groups'))
        self.__installation_images = InstallationImages(client, LinkUtils.get_link_href(json, 'installation-images'))
        self.__nodes = Nodes(client, LinkUtils.get_link_href(json, 'nodes'))

    def __repr__(self):
        return ('{}(client={}, location={})').format(self.__class__.__name__, self.__client, repr(self.__location))

    def __str__(self):
        return ('<{}>').format(self.__class__)


from vas.web_server.Groups import Groups
from vas.web_server.InstallationImages import InstallationImages
from vas.web_server.Nodes import Nodes