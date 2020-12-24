# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/drones/client/baits/clientbase.py
# Compiled at: 2016-11-12 07:38:04
from beeswarm.drones.client.models.session import BaitSession

class ClientBase(object):
    """ Base class for Bees. This should only be used after sub-classing. """

    def __init__(self, options):
        """
            Initializes common values.
        :param sessions: A dict which is updated every time a new session is created.
        :param options: A dict containing the options entry for this bait
        """
        self.options = options
        self.sessions = {}

    def create_session(self, server_host, server_port, honeypot_id):
        """
            Creates a new session.

        :param server_host: IP address of the server
        :param server_port: Server port
        :return: A new `BaitSession` object.
        """
        protocol = self.__class__.__name__.lower()
        session = BaitSession(protocol, server_host, server_port, honeypot_id)
        self.sessions[session.id] = session
        return session

    def close_session(self, session):
        session.end_session()
        if session.id in self.sessions:
            del self.sessions[session]
        else:
            assert False