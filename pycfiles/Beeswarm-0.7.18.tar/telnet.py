# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/drones/honeypot/capabilities/telnet.py
# Compiled at: 2016-11-12 07:38:04
import curses, logging, socket
from beeswarm.drones.honeypot.capabilities.handlerbase import HandlerBase
from beeswarm.drones.honeypot.capabilities.shared.shell import Commands
logger = logging.getLogger(__name__)

class Telnet(HandlerBase):

    def __init__(self, options, work_dir):
        super(Telnet, self).__init__(options, work_dir)

    def handle_session(self, gsocket, address):
        TelnetWrapper.max_tries = int(self.options['protocol_specific_data']['max_attempts'])
        session = self.create_session(address)
        try:
            try:
                TelnetWrapper(address, None, gsocket, session, self.vfsystem)
            except socket.error as err:
                logger.debug(('Unexpected end of telnet session: {0}, errno: {1}. ({2})').format(err, err.errno, session.id))

        finally:
            self.close_session(session)

        return


class TelnetWrapper(Commands):
    """
    Wraps the telnetsrv module to fit the Honeypot architecture.
    """
    PROMPT = '$ '

    def __init__(self, client_address, server, _socket, session, vfs):
        self.session = session
        self.auth_count = 0
        self.username = None
        request = TelnetWrapper.false_request()
        request._sock = _socket
        self.vfs = vfs
        Commands.__init__(self, request, client_address, server, vfs, self.session)
        return

    def authenticate_user(self, username, password):
        if self.session.try_auth(_type='plaintext', username=username, password=password):
            self.working_dir = '/'
            self.username = username
            self.PROMPT = ('[{0}@{1} {2}]$ ').format(self.username, self.HOSTNAME, self.working_dir)
            return True
        self.writeline('Invalid username/password')
        self.auth_count += 1
        return False

    def authentication_ok(self):
        username = None
        password = None
        while self.auth_count < TelnetWrapper.max_tries:
            if self.authNeedUser:
                username = self.readline(prompt='Username: ', use_history=False)
            if self.authNeedPass:
                password = self.readline(echo=False, prompt='Password: ', use_history=False)
                if self.DOECHO:
                    self.write('\n')
            if self.authenticate_user(username, password):
                self.username = username
                return True

        self.username = None
        return False

    def session_end(self):
        self.session.end_session()

    def setterm(self, term):
        f = open('/dev/null', 'w')
        curses.setupterm(term, f.fileno())
        self.TERM = term
        self.ESCSEQ = {}
        for k in self.KEYS.keys():
            str_ = curses.tigetstr(curses.has_key._capability_names[k])
            if str_:
                self.ESCSEQ[str_] = k

        self.CODES['DEOL'] = curses.tigetstr('el')
        self.CODES['DEL'] = curses.tigetstr('dch1')
        self.CODES['INS'] = curses.tigetstr('ich1')
        self.CODES['CSRLEFT'] = curses.tigetstr('cub1')
        self.CODES['CSRRIGHT'] = curses.tigetstr('cuf1')

    def writecooked(self, text):
        Commands.writecooked(self, text)