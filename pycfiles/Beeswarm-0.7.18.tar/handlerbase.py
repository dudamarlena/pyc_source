# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/drones/honeypot/capabilities/handlerbase.py
# Compiled at: 2016-11-12 07:38:04
import os, logging
from fs.osfs import OSFS
from beeswarm.drones.honeypot.models.session import Session
logger = logging.getLogger(__name__)

class HandlerBase(object):

    def __init__(self, options, workdir):
        """
        Base class that all capabilities must inherit from.

        :param sessions: a dictionary of Session objects.
        :param options: a dictionary of configuration options.
        :param workdir: the directory which contains files for this
                        particular instance of Beeswarm
        """
        self.options = options
        self.sessions = {}
        if 'users' in options:
            self.users = options['users']
        else:
            self.users = {}
        self.vfsystem = OSFS(os.path.join(workdir, 'data/vfs'))
        self.port = int(options['port'])

    def create_session(self, address):
        protocol = self.__class__.__name__.lower()
        session = Session(address[0], address[1], protocol, self.users)
        self.sessions[session.id] = session
        session.destination_port = self.port
        logger.debug(('Accepted {0} session on port {1} from {2}:{3}. ({4})').format(protocol, self.port, address[0], address[1], str(session.id)))
        logger.debug(('Size of session list for {0}: {1}').format(protocol, len(self.sessions)))
        return session

    def close_session(self, session):
        logger.debug('Closing sessions')
        session.end_session()
        if session.id in self.sessions:
            del self.sessions[session.id]
        else:
            assert False

    def handle_session(self, socket, address):
        raise Exception('Do no call base class!')