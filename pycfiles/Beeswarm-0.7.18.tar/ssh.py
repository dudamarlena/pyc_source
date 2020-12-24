# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/drones/honeypot/capabilities/ssh.py
# Compiled at: 2016-11-12 07:38:04
import logging, os
from telnetsrv.paramiko_ssh import SSHHandler, TelnetToPtyHandler
from paramiko import RSAKey
from paramiko.ssh_exception import SSHException
from beeswarm.drones.honeypot.capabilities.handlerbase import HandlerBase
from beeswarm.drones.honeypot.capabilities.shared.shell import Commands
logger = logging.getLogger(__name__)

class SSH(HandlerBase):

    def __init__(self, options, work_dir, key='server.key'):
        logging.getLogger('telnetsrv.paramiko_ssh ').setLevel(logging.WARNING)
        logging.getLogger('paramiko').setLevel(logging.WARNING)
        self.key = os.path.join(work_dir, key)
        super(SSH, self).__init__(options, work_dir)

    def handle_session(self, gsocket, address):
        session = self.create_session(address)
        try:
            try:
                SshWrapper(address, None, gsocket, session, self.options, self.vfsystem, self.key)
            except (SSHException, EOFError) as ex:
                logger.debug(('Unexpected end of ssh session: {0}. ({1})').format(ex, session.id))

        finally:
            self.close_session(session)

        return


class BeeTelnetHandler(Commands):

    def __init__(self, request, client_address, server, vfs, session):
        Commands.__init__(self, request, client_address, server, vfs, session)


class SshWrapper(SSHHandler):
    """
    Wraps the telnetsrv paramiko module to fit the Honeypot architecture.
    """
    WELCOME = '...'
    HOSTNAME = 'host'
    PROMPT = None
    telnet_handler = BeeTelnetHandler

    def __init__(self, client_address, server, socket, session, options, vfs, key):
        self.session = session
        self.auth_count = 0
        self.vfs = vfs
        self.working_dir = None
        self.username = None
        SshWrapper.host_key = RSAKey(filename=key)
        request = SshWrapper.dummy_request()
        request._sock = socket
        SSHHandler.__init__(self, request, client_address, server)

        class __MixedPtyHandler(TelnetToPtyHandler, BeeTelnetHandler):

            def __init__(self, *args):
                TelnetToPtyHandler.__init__(self, *args)

        self.pty_handler = __MixedPtyHandler
        return

    def authCallbackUsername(self, username):
        raise

    def authCallback(self, username, password):
        self.session.activity()
        if self.session.try_auth('plaintext', username=username, password=password):
            self.working_dir = '/'
            self.username = username
            self.telnet_handler.PROMPT = ('[{0}@{1} {2}]$ ').format(self.username, self.HOSTNAME, self.working_dir)
            return True
        raise

    def finish(self):
        self.session.end_session()

    def setup(self):
        self.transport.load_server_moduli()
        self.transport.add_server_key(self.host_key)
        self.transport.start_server(server=self)
        while True:
            channel = self.transport.accept(20)
            if channel is None:
                any_running = False
                for _, thread in self.channels.items():
                    if thread.is_alive():
                        any_running = True
                        break

                if not any_running:
                    break

        return

    def start_pty_request(self, channel, term, modes):
        """Start a PTY - intended to run it a (green)thread."""
        request = self.dummy_request()
        request._sock = channel
        request.modes = modes
        request.term = term
        request.username = self.username
        self.pty_handler(request, self.client_address, self.tcp_server, self.vfs, self.session)
        self.transport.close()