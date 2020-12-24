# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/snpplib.py
# Compiled at: 2010-05-28 18:48:31
import socket, string, re
SNPP_HOST = 'localhost'
SNPP_PORT = 444
CRLF = '\r\n'

class SNPPException(Exception):
    """Base class for all exceptions raised by this module."""
    pass


class SNPPInitalize(SNPPException):
    """Error on class initializations.

    Not to be confused with SNPP server initialization, this exception
    is raised when an SNPP-family class is initialized improperly.
    """
    pass


class SNPPServerDisconnected(SNPPException):
    """Not connected to any SNPP server.

    This exception is raised when the server unexpectedly disconnects,
    or when an attempt is made to use the SNPP instance before
    connecting it to a server.
    """
    pass


class SNPPResponseException(SNPPException):
    """Base class for all exceptions that include an SNPP error code.

    These exceptions are generated in some instances when the SNPP
    server returns an error code.  The error code is stored in the
    `snpp_code' attribute of the error, and the `snpp_error' attribute
    is set to the error message.
    """

    def __init__(self, code, msg):
        self.snpp_code = code
        self.snpp_error = msg
        self.args = (code, msg)


class SNPPConnectError(SNPPResponseException):
    """Error during connection establishment.
    Includes 421 Class General Errors"""
    pass


class SNPPResponseError(SNPPResponseException):
    """Catchall for other errors.
    !Note- Probably should expand this.
    Includes 500-700 level response codes.
    """
    pass


class SNPP:
    """
    This Class implements RFC 1861 - Simple Network Paging Protocol
    """
    debuglevel = 0
    file = None
    sock = None

    def __init__(self, host=SNPP_HOST, port=SNPP_PORT, debuglevel=0):
        """Instantiate a new SNPP connection object
        """
        if debuglevel:
            self.debuglevel = debuglevel
        if port:
            self.port = port
        if host:
            self.host = host
            self.connect(host, port)

    def quotedata(self, data):
        """Quote data

        Double leading '.', and change Unix newline '
', or Mac '
' into
        Internet CRLF end-of-line.
        """
        return re.sub('(?m)^\\.', '..', re.sub('(?:\\r\\n|\\n|\\r(?!\\n))', CRLF, data))

    def set_debuglevel(self, debuglevel):
        """Set the debug output level.

        A non-false value results in debug messages for connection and for all
        messages sent to and received from the server.
        """
        self.debuglevel = debuglevel

    def connect(self, host=SNPP_HOST, port=SNPP_PORT):
        """
        Creates a socket connection. This code is almost directly stolen from
        smtplib.py in the main python distribution.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.debuglevel > 0:
            print 'connect:', (host, port)
        self.sock.connect((host, port))
        (code, msg) = self._getreply()
        if self.debuglevel > 0:
            print 'connect:', msg
        if code != 220:
            raise SNPPConnectError(code, msg)

    def _getreply(self):
        """Get a reply from the server.
        
        Returns a tuple consisting of:

          - server response code (e.g. '250', or such, if all goes well)
            Note: returns -1 if it can't read response code.

          - server response string corresponding to response code (multiline
            responses are converted to a single, multiline string).

        Raises SNPPServerDisconnected if end-of-file is reached.
        """
        resp = []
        if self.file is None:
            self.file = self.sock.makefile('rb')
        while 1:
            line = self.file.readline()
            if line == '':
                self.close()
                raise SNPPServerDisconnected('Connection unexpectedly closed')
            if self.debuglevel > 0:
                print 'reply:', `line`
            resp.append(string.strip(line[4:]))
            code = line[:3]
            try:
                errcode = string.atoi(code)
            except ValueError:
                errcode = -1
                break

            if line[3:4] != '-':
                break

        errmsg = string.join(resp, '\n')
        if self.debuglevel > 0:
            print 'reply: retcode (%s); Msg: %s' % (errcode, errmsg)
        return (
         errcode, errmsg)

    def docmd(self, cmd, args=''):
        """Send a command, and return its response code."""
        self._putcmd(cmd, args)
        (code, msg) = self._getreply()
        if self.debuglevel > 0:
            print '%s resp: %d, %s' % (cmd, code, msg)
        if code == 421:
            raise SNPPConnectError(code, msg)
        if code >= 500 and code < 800:
            raise SNPPResponseError(code, msg)
        return (
         code, msg)

    def _putcmd(self, cmd, args=''):
        """Send a command to the server."""
        str = '%s %s%s' % (cmd, args, CRLF)
        self._send(str)

    def _send(self, str):
        """Send `str' to the server.

        !!!! REVISIT ME -- I could be better !!!!!1

        """
        if self.debuglevel > 0:
            print 'send: %s' % str
        if self.sock != None:
            try:
                self.sock.send(str)
            except socket.error:
                raise SNPPServerDisconnected('Server not connected')

        else:
            try:
                self.connect(self.host, self.port)
                self.sock.send(str)
            except socket.error:
                raise SNPPServerDisconnected('Problems with socket')

            return

    def close(self):
        """Close the connection to the SNPP server."""
        if self.file:
            self.file.close()
        self.file = None
        if self.sock:
            self.sock.close()
        self.sock = None
        return

    def pager(self, id, pin=''):
        """ Set the pager id """
        return self._PAGE('%s %s' % (id, pin))

    def message(self, msg):
        """ Set the message to be sent """
        return self._MESS(msg)

    def reset(self):
        """ Reset server session information """
        return self._RESE()

    def send(self):
        """ Finalize current message transaction """
        return self._SEND()

    def quit(self):
        """ Terminates current session """
        return self._QUIT()

    def help(self):
        """ Returns Help information """
        (code, msg) = self._HELP()
        if code == 214:
            helpmsg = ''
        while code == 214:
            helpmsg = string.join([helpmsg, msg], '\n')
            (code, msg) = self._getreply()

        return (
         code, helpmsg)

    def data(self, lines):
        """ Sends a multi-line message """
        (code, msg) = self._DATA()
        if code == 354:
            self._send(str=self.quotedata(lines))
            self._send('%s.%s' % (CRLF, CRLF))
            (code, msg) = self._getreply()
            if self.debuglevel > 0:
                print 'DATA resp: %d, %s' % (code, msg)
        return (
         code, msg)

    def login(self, login, password=''):
        """ Sends a login, password combination """
        return self._LOGI('%s %s' % (login, password))

    def level(self, arg):
        """ Sets Service Level """
        return self._LEVE(arg)

    def alert(self, arg):
        """ Override the default alert setting """
        return self._ALER(arg)

    def coverage(self, arg):
        """ Override subscribers default coverage area """
        return self._COVE(arg)

    def holduntil(self, time):
        """ Allows for delayed delivery of a message """
        return self._HOLD(time)

    def callerid(self, id):
        """ Specifies CallerID function. Message based """
        return self._CALL(id)

    def subject(self, arg):
        """ Specifies subject for a message. Message based. """
        return self._SUBJ(arg)

    def twoway(self):
        """ Signifies begining of two-way commincations """
        return self._2WAY()

    def mcresponse(self, seed, text):
        """ Seeds transaction with acceptable multiple choice response """
        return self._MCRE('%s %s' % (seed, text))

    def mstatus(self, tag, code):
        """ Check the status of a page in the system """
        return self._MSTA('%s %s' % (tag, code))

    def _PAGE(self, args):
        return self.docmd('PAGE', args)

    def _MESS(self, args):
        return self.docmd('MESS', args)

    def _RESE(self):
        return self.docmd('RESE')

    def _SEND(self):
        return self.docmd('SEND')

    def _QUIT(self):
        return self.docmd('QUIT')

    def _HELP(self):
        return self.docmd('HELP')

    def _DATA(self):
        return self.docmd('DATA')

    def _LOGI(self, args):
        return self.docmd('LOGI', args)

    def _LEVE(self, args):
        return self.docmd('LEVE', args)

    def _ALER(self, args):
        return self.docmd('ALER', args)

    def _COVE(self, args):
        return self.docmd('COVE', args)

    def _HOLD(self, args):
        return self.docmd('HOLD', args)

    def _CALL(self, args):
        return self.docmd('CALL', args)

    def _SUBJ(self, args):
        return self.docmd('SUBJ', args)

    def _2WAY(self):
        return self.docmd('2WAY')

    def _PING(self, args):
        return self.docmd('PING', args)

    def _EXPT(self, args):
        return self.docmd('EXPT', args)

    def _NOQUEUE(self, args):
        return self.docmd('NOQUEUE', args)

    def _ACKR(self, args):
        return self.docmd('ACKR', args)

    def _RTYP(self, args):
        return self.docmd('RTYP', args)

    def _MCRE(self, args):
        return self.docmd('MCRE', args)

    def _MSTA(self, args):
        return self.docmd('MSTA', args)

    def _KTAG(self, args):
        return self.docmd('KTAG', args)


if __name__ == '__main__':
    debuglevel = 1
    s = SNPP(debuglevel=debuglevel)
    s.close()
    lines = "This is a test page\nI want to see about multiple lines\nI don't see any reason why this shouldn't work\n    "
    print s.pager(id='5551212', pin='1111')
    print s.level('0')
    print s.holduntil('001231120000 +0100')
    print s.callerid('Monty')
    print s.login(login='mtaylor', password='password')
    print s.data(lines=lines)
    try:
        print s.message(msg='This is a test page from Python')
    except SNPPResponseException, args:
        print args.snpp_code, args.snpp_error
    else:
        print s.send()
        print s.reset()
        try:
            print s.pager(id='5551212')
            print s.message(msg='This is a test page from Python')
        except SNPPResponseException, args:
            print args.snpp_code, args.snpp_error
        else:
            (code, msg) = s.help()
            print msg
            print s.send()
            print s.quit()
            s.close()