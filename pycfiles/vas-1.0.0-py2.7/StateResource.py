# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/shared/StateResource.py
# Compiled at: 2012-11-01 11:35:36
from vas.shared.Resource import Resource
from vas.util.LinkUtils import LinkUtils

class StateResource(Resource):
    """A resource that has state, i.e. it can be started and stopped and its state can be queried

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    :ivar str                               state:      Retrieves the state of the resource from the server.  Will be
                                                        one of:

                                                        * ``STARTING``
                                                        * ``STARTED``
                                                        * ``STOPPING``
                                                        * ``STOPPED``
    """

    @property
    def state(self):
        return self._client.get(self.__state_location)['status']

    def __init__(self, client, location):
        super(StateResource, self).__init__(client, location)
        self.__state_location = LinkUtils.get_link_href(self._details, 'state')

    def start(self):
        """Starts the resource"""
        self._client.post(self.__state_location, {'status': 'STARTED'})

    def stop(self):
        """Stops the resource"""
        self._client.post(self.__state_location, {'status': 'STOPPED'})