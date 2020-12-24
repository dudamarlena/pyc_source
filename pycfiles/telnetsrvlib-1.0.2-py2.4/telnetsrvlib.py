# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/telnetsrvlib.py
# Compiled at: 2010-08-03 18:51:51
"""TELNET server class

Based on the telnet client in telnetlib.py

Presents a command line interface to the telnet client.
Various settings can affect the operation of the server:

        authCallback = Reference to authentication function. If
                   there is none, no un/pw is requested. Should
                   raise an exception if authentication fails
                   Default: None
        authNeedUser = Should a username be requested?
                   Default: False
        authNeedPass = Should a password be requested?
                   Default: False
        COMMANDS     = Dictionary of supported commands
                   Key = command (Must be upper case)
                   Value = List of (function, help text)
                   Function.__doc__ should be long help
                                   Function.aliases may be a list of alternative spellings
"""
import threading, SocketServer, socket, time, sys, traceback, curses.ascii, curses.has_key, curses, logging, re
if not hasattr(socket, 'SHUT_RDWR'):
    socket.SHUT_RDWR = 2
__all__ = ['TelnetHandler', 'TelnetCLIHandler']
IAC = chr(255)
DONT = chr(254)
DO = chr(253)
WONT = chr(252)
WILL = chr(251)
theNULL = chr(0)
SE = chr(240)
NOP = chr(241)
DM = chr(242)
BRK = chr(243)
IP = chr(244)
AO = chr(245)
AYT = chr(246)
EC = chr(247)
EL = chr(248)
GA = chr(249)
SB = chr(250)
BINARY = chr(0)
ECHO = chr(1)
RCP = chr(2)
SGA = chr(3)
NAMS = chr(4)
STATUS = chr(5)
TM = chr(6)
RCTE = chr(7)
NAOL = chr(8)
NAOP = chr(9)
NAOCRD = chr(10)
NAOHTS = chr(11)
NAOHTD = chr(12)
NAOFFD = chr(13)
NAOVTS = chr(14)
NAOVTD = chr(15)
NAOLFD = chr(16)
XASCII = chr(17)
LOGOUT = chr(18)
BM = chr(19)
DET = chr(20)
SUPDUP = chr(21)
SUPDUPOUTPUT = chr(22)
SNDLOC = chr(23)
TTYPE = chr(24)
EOR = chr(25)
TUID = chr(26)
OUTMRK = chr(27)
TTYLOC = chr(28)
VT3270REGIME = chr(29)
X3PAD = chr(30)
NAWS = chr(31)
TSPEED = chr(32)
LFLOW = chr(33)
LINEMODE = chr(34)
XDISPLOC = chr(35)
OLD_ENVIRON = chr(36)
AUTHENTICATION = chr(37)
ENCRYPT = chr(38)
NEW_ENVIRON = chr(39)
TN3270E = chr(40)
XAUTH = chr(41)
CHARSET = chr(42)
RSP = chr(43)
COM_PORT_OPTION = chr(44)
SUPPRESS_LOCAL_ECHO = chr(45)
TLS = chr(46)
KERMIT = chr(47)
SEND_URL = chr(48)
FORWARD_X = chr(49)
PRAGMA_LOGON = chr(138)
SSPI_LOGON = chr(139)
PRAGMA_HEARTBEAT = chr(140)
EXOPL = chr(255)
NOOPT = chr(0)
IS = chr(0)
SEND = chr(1)
CMDS = {WILL: 'WILL', WONT: 'WONT', DO: 'DO', DONT: 'DONT', SE: 'Subnegotiation End', NOP: 'No Operation', DM: 'Data Mark', BRK: 'Break', IP: 'Interrupt process', AO: 'Abort output', AYT: 'Are You There', EC: 'Erase Character', EL: 'Erase Line', GA: 'Go Ahead', SB: 'Subnegotiation Begin', BINARY: 'Binary', ECHO: 'Echo', RCP: 'Prepare to reconnect', SGA: 'Suppress Go-Ahead', NAMS: 'Approximate message size', STATUS: 'Give status', TM: 'Timing mark', RCTE: 'Remote controlled transmission and echo', NAOL: 'Negotiate about output line width', NAOP: 'Negotiate about output page size', NAOCRD: 'Negotiate about CR disposition', NAOHTS: 'Negotiate about horizontal tabstops', NAOHTD: 'Negotiate about horizontal tab disposition', NAOFFD: 'Negotiate about formfeed disposition', NAOVTS: 'Negotiate about vertical tab stops', NAOVTD: 'Negotiate about vertical tab disposition', NAOLFD: 'Negotiate about output LF disposition', XASCII: 'Extended ascii character set', LOGOUT: 'Force logout', BM: 'Byte macro', DET: 'Data entry terminal', SUPDUP: 'Supdup protocol', SUPDUPOUTPUT: 'Supdup output', SNDLOC: 'Send location', TTYPE: 'Terminal type', EOR: 'End or record', TUID: 'TACACS user identification', OUTMRK: 'Output marking', TTYLOC: 'Terminal location number', VT3270REGIME: '3270 regime', X3PAD: 'X.3 PAD', NAWS: 'Window size', TSPEED: 'Terminal speed', LFLOW: 'Remote flow control', LINEMODE: 'Linemode option', XDISPLOC: 'X Display Location', OLD_ENVIRON: 'Old - Environment variables', AUTHENTICATION: 'Authenticate', ENCRYPT: 'Encryption option', NEW_ENVIRON: 'New - Environment variables'}

class TelnetHandler(SocketServer.BaseRequestHandler):
    """A telnet server based on the client in telnetlib"""
    __module__ = __name__
    DOACK = {ECHO: WILL, SGA: WILL, NEW_ENVIRON: WONT}
    WILLACK = {ECHO: DONT, SGA: DO, NAWS: DONT, TTYPE: DO, LINEMODE: DONT, NEW_ENVIRON: DO}
    TERM = 'ansi'
    KEYS = {curses.KEY_UP: 'Up', curses.KEY_DOWN: 'Down', curses.KEY_LEFT: 'Left', curses.KEY_RIGHT: 'Right', curses.KEY_DC: 'Delete', curses.KEY_BACKSPACE: 'Backspace'}
    ESCSEQ = {}
    CODES = {'DEOL': '', 'DEL': '', 'INS': '', 'CSRLEFT': '', 'CSRRIGHT': ''}
    PROMPT = 'Telnet Server> '
    authCallback = None
    authNeedUser = False
    authNeedPass = False

    def __init__(self, request, client_address, server):
        """Constructor.

                When called without arguments, create an unconnected instance.
                With a hostname argument, it connects the instance; a port
                number is optional.
                """
        self.DOECHO = True
        self.DOOPTS = {}
        self.WILLOPTS = {}
        self.COMMANDS = {}
        self.sock = None
        self.rawq = ''
        self.cookedq = []
        self.sbdataq = ''
        self.eof = 0
        self.iacseq = ''
        self.sb = 0
        self.history = []
        self.IQUEUELOCK = threading.Lock()
        self.OQUEUELOCK = threading.Lock()
        self.RUNSHELL = True
        for k in dir(self):
            if k[:3] == 'cmd':
                name = k[3:]
                method = getattr(self, k)
                self.COMMANDS[name] = method
                for alias in getattr(method, 'aliases', []):
                    self.COMMANDS[alias] = self.COMMANDS[name]

        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def setterm(self, term):
        """Set the curses structures for this terminal"""
        logging.debug('Setting termtype to %s' % (term,))
        curses.setupterm(term)
        self.TERM = term
        self.ESCSEQ = {}
        for k in self.KEYS.keys():
            str = curses.tigetstr(curses.has_key._capability_names[k])
            if str:
                self.ESCSEQ[str] = k

        self.CODES['DEOL'] = curses.tigetstr('el')
        self.CODES['DEL'] = curses.tigetstr('dch1')
        self.CODES['INS'] = curses.tigetstr('ich1')
        self.CODES['CSRLEFT'] = curses.tigetstr('cub1')
        self.CODES['CSRRIGHT'] = curses.tigetstr('cuf1')

    def setup(self):
        """Connect incoming connection to a telnet session"""
        self.setterm(self.TERM)
        self.sock = self.request._sock
        for k in self.DOACK.keys():
            self.sendcommand(self.DOACK[k], k)

        for k in self.WILLACK.keys():
            self.sendcommand(self.WILLACK[k], k)

        self.thread_ic = threading.Thread(target=self.inputcooker)
        self.thread_ic.setDaemon(True)
        self.thread_ic.start()
        time.sleep(0.5)

    def finish(self):
        """End this session"""
        self.sock.shutdown(socket.SHUT_RDWR)

    def options_handler(self, sock, cmd, opt):
        """Negotiate options"""
        if cmd == NOP:
            self.sendcommand(NOP)
        elif cmd == WILL or cmd == WONT:
            if self.WILLACK.has_key(opt):
                self.sendcommand(self.WILLACK[opt], opt)
            else:
                self.sendcommand(DONT, opt)
            if cmd == WILL and opt == TTYPE:
                self.writecooked(IAC + SB + TTYPE + SEND + IAC + SE)
        elif cmd == DO or cmd == DONT:
            if self.DOACK.has_key(opt):
                self.sendcommand(self.DOACK[opt], opt)
            else:
                self.sendcommand(WONT, opt)
            if opt == ECHO:
                self.DOECHO = cmd == DO
        elif cmd == SE:
            subreq = self.read_sb_data()
            if subreq[0] == TTYPE and subreq[1] == IS:
                try:
                    self.setterm(subreq[2:])
                except:
                    logging.debug('Terminal type not known')

        elif cmd == SB:
            pass
        else:
            logging.debug('Unhandled option: %s %s' % (cmdtxt, opttxt))

    def sendcommand(self, cmd, opt=None):
        """Send a telnet command (IAC)"""
        if cmd in [DO, DONT]:
            if not self.DOOPTS.has_key(opt):
                self.DOOPTS[opt] = None
            if cmd == DO and self.DOOPTS[opt] != True or cmd == DONT and self.DOOPTS[opt] != False:
                self.DOOPTS[opt] = cmd == DO
                self.writecooked(IAC + cmd + opt)
        elif cmd in [WILL, WONT]:
            if not self.WILLOPTS.has_key(opt):
                self.WILLOPTS[opt] = ''
            if cmd == WILL and self.WILLOPTS[opt] != True or cmd == WONT and self.WILLOPTS[opt] != False:
                self.WILLOPTS[opt] = cmd == WILL
                self.writecooked(IAC + cmd + opt)
        else:
            self.writecooked(IAC + cmd)
        return

    def read_sb_data(self):
        """Return any data available in the SB ... SE queue.

                Return '' if no SB ... SE available. Should only be called
                after seeing a SB or SE command. When a new SB command is
                found, old unread SB data will be discarded. Don't block.

                """
        buf = self.sbdataq
        self.sbdataq = ''
        return buf

    def _readline_echo(self, char, echo):
        """Echo a recieved character, move cursor etc..."""
        if echo == True or echo == None and self.DOECHO == True:
            self.write(char)
        return

    def readline(self, echo=None):
        """Return a line of text, including the terminating LF
                   If echo is true always echo, if echo is false never echo
                   If echo is None follow the negotiated setting.
                """
        line = []
        insptr = 0
        histptr = len(self.history)
        while True:
            c = self.getc(block=True)
            if c == theNULL:
                continue
            elif c == curses.KEY_LEFT:
                if insptr > 0:
                    insptr = insptr - 1
                    self._readline_echo(self.CODES['CSRLEFT'], echo)
                else:
                    self._readline_echo(chr(7), echo)
                continue
            elif c == curses.KEY_RIGHT:
                if insptr < len(line):
                    insptr = insptr + 1
                    self._readline_echo(self.CODES['CSRRIGHT'], echo)
                else:
                    self._readline_echo(chr(7), echo)
                continue
            elif c == curses.KEY_UP or c == curses.KEY_DOWN:
                if c == curses.KEY_UP:
                    if histptr > 0:
                        histptr = histptr - 1
                    else:
                        self._readline_echo(chr(7), echo)
                        continue
                elif c == curses.KEY_DOWN:
                    if histptr < len(self.history):
                        histptr = histptr + 1
                    else:
                        self._readline_echo(chr(7), echo)
                        continue
                line = []
                if histptr < len(self.history):
                    line.extend(self.history[histptr])
                for char in range(insptr):
                    self._readline_echo(self.CODES['CSRLEFT'], echo)

                self._readline_echo(self.CODES['DEOL'], echo)
                self._readline_echo(('').join(line), echo)
                insptr = len(line)
                continue
            elif c == chr(3):
                self._readline_echo('\n' + curses.ascii.unctrl(c) + ' ABORT\n', echo)
                return ''
            elif c == chr(4):
                if len(line) > 0:
                    self._readline_echo('\n' + curses.ascii.unctrl(c) + ' ABORT (QUIT)\n', echo)
                    return ''
                self._readline_echo('\n' + curses.ascii.unctrl(c) + ' QUIT\n', echo)
                return 'QUIT'
            elif c == chr(10):
                self._readline_echo(c, echo)
                if echo == True or echo == None and self.DOECHO == True:
                    self.history.append(line)
                return ('').join(line)
            elif c == curses.KEY_BACKSPACE or c == chr(127) or c == chr(8):
                if insptr > 0:
                    self._readline_echo(self.CODES['CSRLEFT'] + self.CODES['DEL'], echo)
                    insptr = insptr - 1
                    del line[insptr]
                else:
                    self._readline_echo(chr(7), echo)
                continue
            elif c == curses.KEY_DC:
                if insptr < len(line):
                    self._readline_echo(self.CODES['DEL'], echo)
                    del line[insptr]
                else:
                    self._readline_echo(chr(7), echo)
                continue
            else:
                if ord(c) < 32:
                    c = curses.ascii.unctrl(c)
                self._readline_echo(c, echo)
            line[insptr:insptr] = c
            insptr = insptr + len(c)

        return

    def getc(self, block=True):
        """Return one character from the input queue"""
        if not block:
            if not len(self.cookedq):
                return ''
        while not len(self.cookedq):
            time.sleep(0.05)

        self.IQUEUELOCK.acquire()
        ret = self.cookedq[0]
        self.cookedq = self.cookedq[1:]
        self.IQUEUELOCK.release()
        return ret

    def writeline(self, text):
        """Send a packet with line ending."""
        self.write(text + chr(10))

    def write(self, text):
        """Send a packet to the socket. This function cooks output."""
        text = text.replace(IAC, IAC + IAC)
        text = text.replace(chr(10), chr(13) + chr(10))
        self.writecooked(text)

    def writecooked(self, text):
        """Put data directly into the output queue (bypass output cooker)"""
        self.OQUEUELOCK.acquire()
        self.sock.sendall(text)
        self.OQUEUELOCK.release()

    def _inputcooker_getc(self, block=True):
        """Get one character from the raw queue. Optionally blocking.
                Raise EOFError on end of stream. SHOULD ONLY BE CALLED FROM THE
                INPUT COOKER."""
        if self.rawq:
            ret = self.rawq[0]
            self.rawq = self.rawq[1:]
            return ret
        if not block:
            if select.select([self.sock.fileno()], [], [], 0) == ([], [], []):
                return ''
        ret = self.sock.recv(20)
        self.eof = not ret
        self.rawq = self.rawq + ret
        if self.eof:
            raise EOFError
        return self._inputcooker_getc(block)

    def _inputcooker_ungetc(self, char):
        """Put characters back onto the head of the rawq. SHOULD ONLY
                BE CALLED FROM THE INPUT COOKER."""
        self.rawq = char + self.rawq

    def _inputcooker_store(self, char):
        """Put the cooked data in the correct queue (with locking)"""
        if self.sb:
            self.sbdataq = self.sbdataq + char
        else:
            self.IQUEUELOCK.acquire()
            if type(char) in [type(()), type([]), type('')]:
                for v in char:
                    self.cookedq.append(v)

            else:
                self.cookedq.append(char)
            self.IQUEUELOCK.release()

    def inputcooker(self):
        """Input Cooker - Transfer from raw queue to cooked queue.

                Set self.eof when connection is closed.  Don't block unless in
                the midst of an IAC sequence.
                """
        try:
            while True:
                c = self._inputcooker_getc()
                if not self.iacseq:
                    if c == IAC:
                        self.iacseq += c
                        continue
                    elif c == chr(13) and not self.sb:
                        c2 = self._inputcooker_getc(block=False)
                        if c2 == theNULL or c2 == '':
                            c = chr(10)
                        elif c2 == chr(10):
                            c = c2
                        else:
                            self._inputcooker_ungetc(c2)
                            c = chr(10)
                    elif c in [ x[0] for x in self.ESCSEQ.keys() ]:
                        codes = c
                        for keyseq in self.ESCSEQ.keys():
                            if len(keyseq) == 0:
                                continue
                            while codes == keyseq[:len(codes)] and len(codes) <= keyseq:
                                if codes == keyseq:
                                    c = self.ESCSEQ[keyseq]
                                    break
                                codes = codes + self._inputcooker_getc()

                            if codes == keyseq:
                                break
                            self._inputcooker_ungetc(codes[1:])
                            codes = codes[0]

                    self._inputcooker_store(c)
                elif len(self.iacseq) == 1:
                    if c in (DO, DONT, WILL, WONT):
                        self.iacseq += c
                        continue
                    self.iacseq = ''
                    if c == IAC:
                        self._inputcooker_store(c)
                    else:
                        if c == SB:
                            self.sb = 1
                            self.sbdataq = ''
                        elif c == SE:
                            self.sb = 0
                        self.options_handler(self.sock, c, NOOPT)
                elif len(self.iacseq) == 2:
                    cmd = self.iacseq[1]
                    self.iacseq = ''
                    if cmd in (DO, DONT, WILL, WONT):
                        self.options_handler(self.sock, cmd, c)

        except EOFError:
            pass

    def cmdHELP(self, params):
        """[<command>]
                Display help
                Display either brief help on all commands, or detailed
                help on a single command passed as a parameter.
                """
        if params:
            cmd = params[0].upper()
            if self.COMMANDS.has_key(cmd):
                method = self.COMMANDS[cmd]
                doc = method.__doc__.split('\n')
                docp = doc[0].strip()
                docl = ('\n').join(doc[2:]).replace('\n\t\t', ' ').replace('\t', '').strip()
                if len(docl) < 4:
                    docl = doc[1].strip()
                self.writeline('%s %s\n\n%s' % (cmd, docp, docl))
                return
            else:
                self.writeline("Command '%s' not known" % cmd)
        else:
            self.writeline('Help on built in commands\n')
        keys = self.COMMANDS.keys()
        keys.sort()
        for cmd in keys:
            method = self.COMMANDS[cmd]
            doc = method.__doc__.split('\n')
            docp = doc[0].strip()
            docs = doc[1].strip()
            if len(docp) > 0:
                docps = '%s - %s' % (docp, docs)
            else:
                docps = '- %s' % (docs,)
            self.writeline('%s %s' % (cmd, docps))

    cmdHELP.aliases = [
     '?']

    def cmdEXIT(self, params):
        """
                Exit the command shell
                """
        self.RUNSHELL = False
        self.writeline('Goodbye')

    cmdEXIT.aliases = ['QUIT', 'BYE', 'LOGOUT']

    def cmdDEBUG(self, params):
        """
                Display some debugging data
                """
        for (v, k) in self.ESCSEQ.items():
            line = '%-10s : ' % (self.KEYS[k],)
            for c in v:
                if ord(c) < 32 or ord(c) > 126:
                    line = line + curses.ascii.unctrl(c)
                else:
                    line = line + c

            self.writeline(line)

    def cmdHISTORY(self, params):
        """
                Display the command history
                """
        cnt = 0
        self.writeline('Command history\n')
        for line in self.history:
            cnt = cnt + 1
            self.writeline('%-5d : %s' % (cnt, ('').join(line)))

    def handleException(self, exc_type, exc_param, exc_tb):
        """Exception handler (False to abort)"""
        self.writeline(traceback.format_exception_only(exc_type, exc_param)[(-1)])
        return True

    def handle(self):
        """The actual service to which the user has connected."""
        username = None
        password = None
        if self.authCallback:
            if self.authNeedUser:
                if self.DOECHO:
                    self.write('Username: ')
                username = self.readline()
            if self.authNeedPass:
                if self.DOECHO:
                    self.write('Password: ')
                password = self.readline(echo=False)
                if self.DOECHO:
                    self.write('\n')
            try:
                self.authCallback(username, password)
            except:
                return

        while self.RUNSHELL:
            if self.DOECHO:
                self.write(self.PROMPT)
            cmdlist = [ item.strip() for item in self.readline().split() ]
            idx = 0
            while idx < len(cmdlist) - 1:
                if cmdlist[idx][0] in ["'", '"']:
                    cmdlist[idx] = cmdlist[idx] + ' ' + cmdlist.pop(idx + 1)
                    if cmdlist[idx][0] != cmdlist[idx][(-1)]:
                        continue
                    cmdlist[idx] = cmdlist[idx][1:-1]
                idx = idx + 1

            if cmdlist:
                cmd = cmdlist[0].upper()
                params = cmdlist[1:]
                if self.COMMANDS.has_key(cmd):
                    try:
                        self.COMMANDS[cmd](params)
                    except:
                        (t, p, tb) = sys.exc_info()
                        if self.handleException(t, p, tb):
                            break

                else:
                    self.write("Unknown command '%s'\n" % cmd)

        logging.debug('Exiting handler')
        return


if __name__ == '__main__':

    class TNS(SocketServer.TCPServer):
        __module__ = __name__
        allow_reuse_address = True


    class TNH(TelnetHandler):
        __module__ = __name__

        def cmdECHO(self, params):
            """ [<arg> ...]
                        Echo parameters
                        Echo command line parameters back to user, one per line.
                        """
            self.writeline('Parameters:')
            for item in params:
                self.writeline('\t%s' % item)


    logging.getLogger('').setLevel(logging.DEBUG)
    tns = TNS(('0.0.0.0', 8023), TNH)
    tns.serve_forever()