# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Protocol/AIM/LoginHandler.py
# Compiled at: 2008-10-19 12:19:52
"""=========
AIM Login
=========

This component logs into to AIM with the given screenname and password. It then
sends its logged-in OSCAR connection out of its "signal" outbox, followed by a
list of any non-login-related messages it has received.

Example Usage
-------------
Login and wire the resulting OSCARClient up to a ChatManager::

    class AIMHarness(component):
        def main(self):
            self.loginer = LoginHandler('sitar63112', 'sitar63112').activate()
            self.link((self.loginer, "signal"), (self, "internal inbox"))
            self.addChildren(self.loginer)
            while not self.dataReady("internal inbox"):
                yield 1
            self.oscar = self.recv("internal inbox")
            queued = self.recv("internal inbox")
            self.unlink(self.oscar)

            self.chatter = ChatManager().activate()
            self.link((self.chatter, "heard"), (self, "outbox"), passthrough=2)
            self.link((self, "inbox"), (self.chatter, "talk"), passthrough=1)
            self.link((self.chatter, "outbox"), (self.oscar, "inbox"))
            self.link((self.oscar, "outbox"), (self.chatter, "inbox"))
            self.link((self, "internal outbox"), (self.chatter, "inbox"))
            while len(queued):
                self.send(queued[0], "internal outbox")
                del(queued[0])
            while True:
                yield 1

    AIMHarness().run()

You can also run LoginHandler by itself. This is useful for debugging::

    LoginHandler("kamaelia1", "abc123").run()

How it works
------------
First, LoginHandler connects to the authorization server at login.oscar.aol.com
and gets the address of the Basic Oscar Service server, the port to connect on,
and an authorization cookie. It connects to the BOS server, which after some
negotiation sends LoginHandler a list of the services it supports and their
service versions. LoginHandler then finds out rate limits and service
limitations. Then LoginHandler tells the server it is ready to begin normal
operation as an AIM client.

At this point the server recognizes us as a functioning AIM client. LoginHandler
unlinks its internal OSCARClient and passes the OSCARClient out of the "signal"
outbox. LoginHandler also collects any additional messages from OSCARClient and
sends them out of its "signal" outbox. Now any component that connects to that
OSCARClient will be able to send and receive AIM messages.

"""
from Kamaelia.Support.OscarUtil import *
from Kamaelia.Support.OscarUtil2 import *
from Kamaelia.Protocol.AIM.OSCARClient import OSCARClient, SNACExchanger
from Axon.Component import component
import Kamaelia.Util.Clock as Clock, time, Axon

class LoginHandler(SNACExchanger):
    """    LoginHandler(screenname, password, [versionNumber]) -> new LoginHandler
    component

    Once started, LoginHandler logs in to AIM and sends the primed connection
    out of its "signal" outbox.

    Keyword arguments:

    - versionNumber  -- the version of OSCAR protocol we are using. Default 1.
    """
    Inboxes = {'inbox': 'Receives messages from the server', '_clock': 'Receives timout messages', 
       'control': 'NOT USED'}
    Outboxes = {'outbox': 'Send messages to the server', 'signal': 'Also sends messages to the server'}

    def __init__(self, screenname, password, versionNumber=1):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(LoginHandler, self).__init__()
        self.screenname = screenname
        self.password = password
        self.versionNumber = versionNumber
        self.desiredServiceVersions = {1: 3, 2: 1, 
           3: 1, 
           4: 1, 
           8: 1, 
           9: 1, 
           10: 1, 
           11: 1, 
           19: 4, 
           21: 1}
        self.client_id = 265
        self.major_version = 0
        self.minor_version = 1
        self.lesser_version = 0
        self.build_num = 42
        self.distr_num = 0
        self.language = 'en'
        self.country = 'us'
        self.use_SSI = 1
        self.oscar = OSCARClient('login.oscar.aol.com', 5190).activate()
        self.link((self, 'outbox'), (self.oscar, 'inbox'))
        self.link((self.oscar, 'outbox'), (self, 'inbox'))
        debugSections = {'LoginHandler.main': 10, 'LoginHandler.connectAuth': 10, 
           'LoginHandler.reconnect': 10, 
           'LoginHandler.passTheReins': 10}
        self.debugger.addDebug(**debugSections)

    def main(self):
        """        Gets BOS and auth cookie, negotiates protocol, and then passes the
        connection + any non-login-related messages out.
        """
        yield Axon.Ipc.WaitComplete(self.getBOSandCookie())
        if self.error:
            self.send(self.error, 'signal')
        else:
            yield Axon.Ipc.WaitComplete(self.negotiateProtocol())
            yield Axon.Ipc.WaitComplete(self.passTheReins())

    def getBOSandCookie(self):
        """Gets BOS and auth cookie."""
        yield Axon.Ipc.WaitComplete(self.connectAuth())
        for reply in self.getCookie():
            yield 1

        self.error = self.extractBOSandCookie(reply)
        if self.error:
            assert self.debugger.note('LoginHandler.main', 1, self.error)
        else:
            assert self.debugger.note('LoginHandler.main', 1, 'Got cookie!')

    def negotiateProtocol(self):
        """Negotiates protocol."""
        yield Axon.Ipc.WaitComplete(self.reconnect(self.server, self.port, self.cookie))
        yield Axon.Ipc.WaitComplete(self.setServiceVersions())
        yield Axon.Ipc.WaitComplete(self.getRateLimits())
        self.requestRights()
        yield Axon.Ipc.WaitComplete(self.getRights())
        assert self.debugger.note('LoginHandler.main', 5, 'rights gotten, activating connection')
        self.activateConnection()

    def connectAuth(self):
        """
        Connects to the AIM authorization server, says hi, and waits for
        acknowledgement.
        """
        assert self.debugger.note('LoginHandler.connectAuth', 7, 'sending new connection...')
        data = struct.pack('!i', self.versionNumber)
        self.send((CHANNEL_NEWCONNECTION, data))
        self.clock = Clock.CheapAndCheerfulClock(120)
        t = time.time()
        self.link((self.clock, 'outbox'), (self, '_clock'))
        self.clock.activate()
        not_done = True
        while not_done:
            while not self.anyReady():
                self.pause()
                yield 1

            while self.dataReady('inbox'):
                reply = self.recv('inbox')
                self.unlink(self.clock)
                not_done = False
                while self.dataReady('_clock'):
                    self.recv('_clock')

            while self.dataReady('_clock'):
                if self.recv('_clock') and not_done:
                    if time.time() - t > 2:
                        raise 'Connection time out!' + str(time.time() - t)
                    else:
                        print 'odd'

        assert self.debugger.note('LoginHandler.connectAuth', 5, 'received new connection ack')

    def getCookie(self):
        """ Requests and waits for MD5 key. """
        zero = struct.pack('!H', 0)
        request = TLV(1, self.screenname) + TLV(75, zero) + TLV(90, zero)
        self.sendSnac(23, 6, request)
        for reply in self.waitSnac(23, 7):
            yield 1

        assert self.debugger.note('AuthCookieGetter.main', 5, 'received md5 key')
        md5key = reply[2:]
        request = TLV(1, self.screenname) + TLV(37, encryptPasswordMD5(self.password, md5key)) + TLV(76, '') + TLV(3, CLIENT_ID_STRING) + TLV(22, Double(self.client_id)) + TLV(23, Double(self.major_version)) + TLV(24, Double(self.minor_version)) + TLV(25, Double(self.lesser_version)) + TLV(26, Double(self.build_num)) + TLV(20, Quad(self.distr_num)) + TLV(15, self.language) + TLV(14, self.country) + TLV(74, Single(self.use_SSI))
        self.sendSnac(23, 2, request)
        for reply in self.waitSnac(23, 3):
            yield 1

        assert self.debugger.note('AuthCookieGetter.main', 5, 'received BOS/auth cookie')
        while not self.dataReady():
            self.pause()
            yield 1

        recvdflap = self.recv()
        assert recvdflap[0] == 4
        yield reply

    def extractBOSandCookie(self, reply):
        """Extracts BOS server, port, and auth cookie from server reply."""
        parsed = readTLVs(reply)
        if parsed.has_key(8):
            return readTLV08(parsed[8])
        assert parsed.has_key(5)
        BOS_server = parsed[5]
        (BOS_server, port) = BOS_server.split(':')
        port = int(port)
        auth_cookie = parsed[6]
        self.server, self.port, self.cookie = BOS_server, port, auth_cookie

    def reconnect(self, server, port, cookie):
        """
        Discards old connection to authorization server, connects to BOS, says
        hi, and waits for acknowledgement.
        """
        self.unlink(self.oscar)
        self.oscar = OSCARClient(server, port).activate()
        self.link((self, 'outbox'), (self.oscar, 'inbox'))
        self.link((self.oscar, 'outbox'), (self, 'inbox'))
        yield 1
        assert self.debugger.note('LoginHandler.reconnect', 7, 'linked, linked, and unlinked')
        data = Quad(self.versionNumber)
        data += TLV(6, cookie)
        self.send((CHANNEL_NEWCONNECTION, data))
        while not self.dataReady():
            self.pause()
            yield 1

        serverAck = self.recv()
        assert serverAck[0] == CHANNEL_NEWCONNECTION

    def setServiceVersions(self):
        """
        Waits for supported services list from server, requests service
        versions, and waits for server acknowledgement of accepted service
        versions.
        """
        for reply in self.waitSnac(1, 3):
            yield 1

        supportedFamilies = struct.unpack('!%iH' % (len(reply) / 2), reply)
        data = ''
        for family in supportedFamilies:
            if family in self.desiredServiceVersions:
                data += Double(family) + Double(self.desiredServiceVersions[family])

        self.sendSnac(1, 23, data)
        for reply in self.waitSnac(1, 24):
            yield 1

        reply = unpackDoubles(reply)
        self.acceptedServices = dict(zip(reply[::2], reply[1::2]))
        assert self.debugger.note('LoginHandler.main', 5, 'accepted ' + str(self.acceptedServices))

    def parseRateInfo(self, data, numClasses):
        """
        Does something useful with the information about rate classes that the
        server sends us and returns the acknowledgement we are supposed to send
        back to the server.

        """
        return '\x00\x01\x00\x02\x00\x03\x00\x04\x00\x05'

    def getRateLimits(self):
        """
        Request rate limits, wait for reply, and send acknowledgement to the
        server.
        """
        self.sendSnac(1, 6, '')
        for reply in self.waitSnac(1, 7):
            yield 1

        assert self.debugger.note('LoginHandler.main', 7, 'parsing rate info...')
        (numClasses,) = struct.unpack('!H', reply[:2])
        ack = self.parseRateInfo(reply[2:], numClasses)
        self.sendSnac(1, 8, ack)

    def requestRights(self):
        """
        Request that the server tell us our rights and limitations for the
        services that were accepted.
        """
        self.sendSnac(1, 14, '')
        self.sendSnac(19, 2, '')
        self.sendSnac(19, 4, '')
        self.sendSnac(2, 2, '')
        self.sendSnac(3, 2, '')
        self.sendSnac(4, 4, '')
        self.sendSnac(9, 2, '')

    def getRights(self):
        """.
        Get the server's reply on rights and limitations
        """
        doNothing = lambda x: None
        expecting = {(1, 15): doNothing, (19, 3): doNothing, 
           (19, 6): doNothing, 
           (2, 3): doNothing, 
           (3, 3): doNothing, 
           (4, 5): doNothing, 
           (9, 3): doNothing}
        done = False
        while not done and len(expecting):
            while not self.dataReady():
                self.pause()
                yield 1

            (header, reply) = self.recvSnac()
            if (header[0], header[1]) in expecting.keys():
                del expecting[(header[0], header[1])]
            else:
                done = True

        assert self.debugger.note('LoginHandler.main', 5, 'last reply: ' + str((header[0], header[1])))

    def activateConnection(self):
        """
        Send some parameters up to the server, then signal that we're ready to
        begin receiving data.
        """
        capabilities = TLV(5, '')
        self.sendSnac(2, 4, capabilities)
        self.sendSnac(19, 18, '')
        self.sendSnac(19, 7, '')
        userStatus = TLV(6, struct.pack('!HH', STATUS_MISC_DCDISABLED, STATUS_ONLINE))
        self.sendSnac(1, 30, userStatus)
        body = ''
        for (service, version) in self.desiredServiceVersions.items():
            data = struct.pack('!HHi', service, version, 17827369)
            body += data

        self.sendSnac(1, 2, body)
        assert self.debugger.note('LoginHandler.activateConnection', 5, 'sent CLI_READY')

    def passTheReins(self):
        """
        Unlink the internal OSCARClient and send it to "signal".
        Also collect any unused messages from OSCARClient and send them out
        through "signal".
        """
        while not self.dataReady():
            self.pause()
            yield 1

        queued = []
        while self.dataReady():
            queued.append(self.recv())
            yield 1

        self.unlink(self.oscar)
        self.send(self.oscar, 'signal')
        self.send(queued, 'signal')
        assert self.debugger.note('LoginHandler.passTheReins', 5, 'Login done')


__kamaelia_components__ = (
 LoginHandler,)
if __name__ == '__main__':
    screenname = 'kamaelia1'
    password = 'abc123'
    LoginHandler(screenname, password).run()