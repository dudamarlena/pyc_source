# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/tc_server/NodeRevisions.py
# Compiled at: 2012-11-01 11:37:44
from vas.shared.Collection import Collection
from vas.shared.StateResource import StateResource
from vas.util.LinkUtils import LinkUtils

class NodeRevisions(Collection):
    """Used to enumerate revisions of a node application

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """

    def __init__(self, client, location):
        super(NodeRevisions, self).__init__(client, location, 'revisions', NodeRevision)


class NodeRevision(StateResource):
    """A revision of a node application

    :ivar `vas.tc_server.NodeApplications.NodeApplication`  application:    The revision's application
    :ivar `vas.tc_server.Revisions.Revision`                revision:       The group revision that this node revision
                                                                            is a member of
    :ivar `vas.shared.Security.Security`                    security:       The resource's security
    :ivar str                                               state:          Retrieves the state of the resource from the
                                                                            server.  Will be one of:

                                                                            * ``STARTING``
                                                                            * ``STARTED``
                                                                            * ``STOPPING``
                                                                            * ``STOPPED``
    :ivar str                                               version:        The revision's version
    """
    __application = None
    __group_revision = None

    @property
    def application(self):
        self.__application = self.__application or NodeApplication(self._client, self.__application_location)
        return self.__application

    @property
    def group_revision(self):
        self.__group_revision = self.__group_revision or Revision(self._client, self.__group_revision_location)
        return self.__group_revision

    @property
    def version(self):
        return self.__version

    def __init__(self, client, location):
        super(NodeRevision, self).__init__(client, location)
        self.__version = self._details['version']
        self.__application_location = LinkUtils.get_link_href(self._details, 'node-application')
        self.__group_revision_location = LinkUtils.get_link_href(self._details, 'group-revision')

    def __str__(self):
        return ('<{} version={}>').format(self.__class__.__name__, self.__version)


from vas.tc_server.NodeApplications import NodeApplication
from vas.tc_server.Revisions import Revision