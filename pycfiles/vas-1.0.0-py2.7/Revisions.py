# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/tc_server/Revisions.py
# Compiled at: 2012-11-01 11:37:44
from vas.shared.Deletable import Deletable
from vas.shared.MutableCollection import MutableCollection
from vas.shared.StateResource import StateResource
from vas.util.LinkUtils import LinkUtils

class Revisions(MutableCollection):
    """Used to enumerate, create, and delete application revisions

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """

    def __init__(self, client, location):
        super(Revisions, self).__init__(client, location, 'revisions', Revision)

    def create(self, revision_image):
        """Creates a revision by deploying the revision image

        :param `vas.tc_server.RevisionImages.RevisionImage` revision_image: The revision image to deploy
        :rtype:     :class:`vas.tc_server.Revisions.Revision`
        :return:    The new revision
        """
        return self._create({'image': revision_image._location}, 'group-revision')


class Revision(StateResource, Deletable):
    """A revision of an application

    :ivar `vas.tc_server.Applications.Application`      application:    The revision's application
    :ivar list                                          node_revisions: The revision's node revisions
    :ivar `vas.tc_server.RevisionImages.RevisionImage`  revision_image: The revision image, if any, that was used to
                                                                        create the revision
    :ivar `vas.shared.Security.Security`                security:       The resource's security
    :ivar str                                           state:          Retrieves the state of the resource from the
                                                                        server. Will be one of:

                                                                        * ``STARTING``
                                                                        * ``STARTED``
                                                                        * ``STOPPING``
                                                                        * ``STOPPED``
    :ivar str                                           version:        The revision's version
    """
    __application = None
    __node_revisions = None
    __revision_image = None

    @property
    def application(self):
        self.__application = self.__application or Application(self._client, self.__application_location)
        return self.__application

    @property
    def node_revisions(self):
        self.__node_revisions = self.__node_revisions or self._create_resources_from_links('node-revision', NodeRevision)
        return self.__node_revisions

    @property
    def revision_image(self):
        self.__revision_image = self.__revision_image or RevisionImage(self._client, self.__revision_image_location) if self.__revision_image_location else None
        return self.__revision_image

    @property
    def version(self):
        return self.__version

    def __init__(self, client, location):
        super(Revision, self).__init__(client, location)
        self.__version = self._details['version']
        self.__application_location = LinkUtils.get_link_href(self._details, 'group-application')
        self.__revision_image_location = LinkUtils.get_link_href(self._details, 'revision-image')

    def __str__(self):
        return ('<{} version={}>').format(self.__class__.__name__, self.__version)


from vas.tc_server.Applications import Application
from vas.tc_server.NodeRevisions import NodeRevision
from vas.tc_server.RevisionImages import RevisionImage