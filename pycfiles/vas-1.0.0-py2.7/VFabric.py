# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/vfabric/VFabric.py
# Compiled at: 2012-11-01 11:37:44
from vas.util.LinkUtils import LinkUtils

class VFabric(object):
    """The entry point of the vFabric API

    :ivar `vas.vfabric.AgentImage`  agent_image:    the installation image for the vFabric Administration agent
    :ivar `vas.vfabric.Nodes.Nodes` nodes:          the nodes that are known to the server
    """

    @property
    def agent_image(self):
        return self.__agent_image

    @property
    def nodes(self):
        return self.__nodes

    def __init__(self, client, location):
        self.__client = client
        self.__location = location
        json = client.get(location)
        self.__agent_image = AgentImage(client, LinkUtils.get_link_href(json, 'agent-image'))
        self.__nodes = Nodes(client, LinkUtils.get_link_href(json, 'nodes'))

    def __repr__(self):
        return ('{}(client={}, location={})').format(self.__class__.__name__, self.__client, repr(self.__location))

    def __str__(self):
        return ('<{}>').format(self.__class__.__name__)


from vas.vfabric.AgentImage import AgentImage
from vas.vfabric.Nodes import Nodes