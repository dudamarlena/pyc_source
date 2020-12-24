# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/gemfire/CacheServerInstances.py
# Compiled at: 2012-11-01 11:35:36
from vas.shared.Instance import Instance
from vas.shared.MutableCollection import MutableCollection
from vas.util.LinkUtils import LinkUtils

class CacheServerInstances(MutableCollection):
    """Used to enumerate, create, and delete cache server instances

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """

    def __init__(self, client, location):
        super(CacheServerInstances, self).__init__(client, location, 'cache-server-group-instances', CacheServerInstance)

    def create(self, installation, name):
        """Creates a new cache server instance

        :param `vas.gemfire.Installations.Installation` installation:   The installation to be used by the instance
        :param str                                      name:           The name of the instance
        :rtype:     :class:`vas.gemfire.CacheServerInstances.CacheServerInstance`
        :return:    The new cache server instance
        """
        payload = {'installation': installation._location, 'name': name}
        return self._create(payload, 'cache-server-group-instance')


class CacheServerInstance(Instance):
    """A cache server instance

    :ivar `vas.gemfire.Groups.Group`                 group:          The group that contains this instance
    :ivar `vas.gemfire.Installations.Installation`   installation:   The installation that this instance is using
    :ivar `vas.gemfire.LiveApplicationCodes.LiveApplicationCodes`   live_application_code:  The instance's live
                                                                                            application code
    :ivar `vas.gemfire.CacheServerLiveConfigurations.CacheServerLiveConfigurations` live_configurations:    The instance's live
                                                                                                            configurations
    :ivar str                                       name:           The instance's name
    :ivar list                                      node_instances: The instance's individual node instances
    :ivar `vas.gemfire.PendingApplicationCodes.PendingApplicationCodes` pending_application_code:   The instance's
                                                                                                    pending application
                                                                                                    code
    :ivar `vas.gemfire.CacheServerPendingConfigurations.CacheServerPendingConfigurations`   pending_configurations: The instance's
                                                                                                                    pending configurations
    :ivar `vas.shared.Security.Security`            security:       The resource's security
    :ivar str                                       state:          Retrieves the state of the resource from the server.
                                                                    Will be one of:

                                                                    * ``STARTING``
                                                                    * ``STARTED``
                                                                    * ``STOPPING``
                                                                    * ``STOPPED``
    """
    __live_application_code = None
    __pending_application_code = None

    @property
    def live_application_code(self):
        self.__live_application_code = self.__live_application_code or LiveApplicationCodes(self._client, self.__live_application_code_location)
        return self.__live_application_code

    @property
    def pending_application_code(self):
        self.__pending_application_code = self.__pending_application_code or PendingApplicationCodes(self._client, self.__pending_application_code_location)
        return self.__pending_application_code

    def __init__(self, client, location):
        super(CacheServerInstance, self).__init__(client, location, Group, Installation, CacheServerLiveConfigurations, CacheServerPendingConfigurations, CacheServerNodeInstance, 'cache-server-node-instance')
        self.__live_application_code_location = LinkUtils.get_link_href(self._details, 'live-application-code')
        self.__pending_application_code_location = LinkUtils.get_link_href(self._details, 'pending-application-code')

    def update(self, installation):
        """Updates the instance to use a different installation

        :param `vas.gemfire.Installations.Installation` installation:   The installation that the instance should use
        """
        self._client.post(self._location, {'installation': installation._location})
        self.reload()


from vas.gemfire.CacheServerLiveConfigurations import CacheServerLiveConfigurations
from vas.gemfire.CacheServerNodeInstances import CacheServerNodeInstance
from vas.gemfire.CacheServerPendingConfigurations import CacheServerPendingConfigurations
from vas.gemfire.Groups import Group
from vas.gemfire.Installations import Installation
from vas.gemfire.LiveApplicationCodes import LiveApplicationCodes
from vas.gemfire.PendingApplicationCodes import PendingApplicationCodes