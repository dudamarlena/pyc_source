# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/tc_server/TcServer.py
# Compiled at: 2012-11-01 11:37:44
from vas.util.LinkUtils import LinkUtils

class TcServer(object):
    """The entry point to the API for administering tc Server

    :ivar `vas.tc_server.Groups.Groups`                         groups:                 the tc Server groups
    :ivar `vas.tc_server.InstallationImages.InstallationImages` installation_images:    the tc Server installation
                                                                                        images
    :ivar `vas.tc_server.Nodes.Nodes`                           nodes:                  The tc Server nodes
    :ivar `vas.tc_server.RevisionImages.RevisionImages`         revision_images:        The tc Server revision images
    :ivar `vas.tc_server.TemplateImages.TemplateImages`         template_images:        The tc Server template images
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

    @property
    def revision_images(self):
        return self.__revision_images

    @property
    def template_images(self):
        return self.__template_images

    def __init__(self, client, location):
        self.__client = client
        self.__location = location
        json = client.get(location)
        self.__groups = Groups(client, LinkUtils.get_link_href(json, 'groups'))
        self.__installation_images = InstallationImages(client, LinkUtils.get_link_href(json, 'installation-images'))
        self.__nodes = Nodes(client, LinkUtils.get_link_href(json, 'nodes'))
        self.__revision_images = RevisionImages(client, LinkUtils.get_link_href(json, 'revision-images'))
        self.__template_images = TemplateImages(client, LinkUtils.get_link_href(json, 'template-images'))

    def __repr__(self):
        return ('{}(client={}, location={})').format(self.__class__.__name__, self.__client, repr(self.__location))

    def __str__(self):
        return ('<{}>').format(self.__class__.__name__)


from vas.tc_server.Groups import Groups
from vas.tc_server.InstallationImages import InstallationImages
from vas.tc_server.Nodes import Nodes
from vas.tc_server.RevisionImages import RevisionImages
from vas.tc_server.TemplateImages import TemplateImages