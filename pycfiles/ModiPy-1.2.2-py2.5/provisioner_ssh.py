# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/modipy/provisioner_ssh.py
# Compiled at: 2009-08-25 18:19:44
import os.path, getpass, struct, logging, re, debug
from twisted.conch.ssh import transport, userauth, connection, common, keys, channel
from twisted.internet import defer, protocol, reactor
from provisioner_command import ExpectProtocol, ConnectingProvisioner
from provisioner_command import MultiConnectingProvisioner
import util
log = logging.getLogger('modipy')

class SimpleTransport(transport.SSHClientTransport):

    def verifyHostKey(self, hostKey, fingerprint):
        log.debug('checking host key')
        print 'host key fingerprint: %s' % fingerprint
        return defer.succeed(1)

    def connectionSecure(self):
        log.debug('Creating secure connection...')
        self.requestService(SimpleUserAuth('daedalus', SSHProvisionerConnection()))


class SimpleUserAuth(userauth.SSHUserAuthClient):

    def getPassword(self):
        return defer.succeed(getpass.getpass("%s@%s's password: " % ('daedalus', 'localhost')))

    def getGenericAnswers(self, name, instruction, questions):
        print name
        print instruction
        answers = []
        for (prompt, echo) in questions:
            if echo:
                answer = raw_input(prompt)
            else:
                answer = getpass.getpass(prompt)
            answers.append(answer)

        return defer.succeed(answers)

    def getPublicKey(self):
        path = os.path.expanduser('~/.ssh/id_dsa')
        if not os.path.exists(path) or self.lastPublicKey:
            return
        return keys.getPublicKeyString(path + '.pub')

    def getPrivateKey(self):
        path = os.path.expanduser('~/.ssh/id_dsa')
        return defer.succeed(keys.getPrivateKeyObject(path))


class SSHProvisionerConnection(connection.SSHConnection):
    """
    We use this connection to send the provisioning command
    to the remote end over the secure channel.
    """

    def serviceStarted(self):
        self.command_d = {}
        log.debug('service started on transport: %s', self.transport.factory.provisioner)
        self.transport.factory.provisioner.connection_success(self, self.transport)

    def serviceStopped(self):
        log.debug('My channels are: %s', self.channels)
        connection.SSHConnection.serviceStopped(self)

    def exec_remote(self, command_string):
        """
        Run a remote command string.
        """
        channel = ProvisioningChannel(65536, 32768, self)
        exec_d = defer.Deferred()
        self.command_d[channel] = (exec_d, command_string)
        self.openChannel(channel)
        return exec_d

    def channelOnline(self, channel):
        """
        Called when the secure command channel has been set up.
        """
        log.debug('Secure channel online.')
        (exec_d, command_string) = self.command_d[channel]
        d = self.sendRequest(channel, 'exec', common.NS(command_string), wantReply=1)
        d.addCallback(self._cbRequest, channel)

    def _cbRequest(self, ignored, channel):
        log.debug('exec finished.')
        self.sendEOF(channel)

    def channelClosed(self, channel):
        """
        A channel closed. Get its results, and callback
        """
        log.debug('channel closed: %s', channel.data)
        results = (channel.status, channel.data)
        (exec_d, command_string) = self.command_d[channel]
        exec_d.callback(results)


class ProvisioningChannel(channel.SSHChannel):
    name = 'session'

    def openFailed(self, reason):
        log.error('Cannot open channel: %s', reason)

    def channelOpen(self, ignoredData):
        log.debug('channel is open.')
        self.data = ''
        log.debug('channel connection is: %s', self.conn)
        self.conn.channelOnline(self)

    def request_exit_status(self, data):
        self.status = struct.unpack('>L', data)[0]
        log.debug('channel exit status was: %s' % self.status)
        self.loseConnection()

    def dataReceived(self, data):
        log.debug('got some remote data: %s', data)
        self.data += data

    def closed(self):
        log.debug('channel closed: %s' % repr(self.data))
        self.conn.channelClosed(self)
        self.loseConnection()


class CatChannel(channel.SSHChannel):
    name = 'session'

    def openFailed(self, reason):
        print 'echo failed', reason

    def channelOpen(self, ignoredData):
        self.data = ''
        d = self.conn.sendRequest(self, 'exec', common.NS('cat'), wantReply=1)
        d.addCallback(self._cbRequest)

    def _cbRequest(self, ignored):
        self.write('hello conch\n')
        self.conn.sendEOF(self)

    def dataReceived(self, data):
        self.data += data

    def closed(self):
        print 'got data from cat: %s' % repr(self.data)
        self.loseConnection()


class SSHProvisioner(ConnectingProvisioner):
    """
    An SSHProvisioner connects to remote devices via the Secure
    Shell protocol and executes commands.

    The basic form connects once per device and runs all the
    changes over the same session.

    If you want to connect for every part of the change,
    use a MultiConnectingSSHProvisioner
    """

    def __init__(self, name='', namespace={}, authoritarian=False, autobackout=False, command_timeout=300):
        ConnectingProvisioner.__init__(self, name, namespace, authoritarian, autobackout, command_timeout)
        self.all_commands_defer = {}

    def parse_config_node(self, node):
        """
        Add any additional configuration information that is provisioner specific.
        """
        pass

    def connect(self, device, namespace):
        """
        Connect to the remote device via SSH.
        """
        log.debug("Connecting to '%s' via SSH...", device.name)
        self.transport = None
        self.connecting_d = defer.Deferred()
        self.connectedDevice = device
        self.connection_timeout_d = reactor.callLater(5, self.connection_timeout, device)
        factory = protocol.ClientFactory()
        factory.provisioner = self
        factory.protocol = SimpleTransport
        conn = reactor.connectTCP(device.name, 22, factory)
        return self.connecting_d

    def connection_success(self, conn, transport):
        log.debug('connection succeeded')
        self.conn = conn
        self.transport = transport
        log.debug('connection information: %s', self.transport)
        self.connection_timeout_d.cancel()
        self.connecting_d.callback(None)
        return

    def connection_timeout(self, device):
        log.error('connection to device timed out')
        self.connecting_d.errback(Exception('Connection to %s timed out' % device.name))

    def disconnect(self, ignored, device):
        if self.transport is not None:
            self.transport.loseConnection()
        return

    def run_commands(self, ignored, device, expectset, namespace):
        """
        Run each command, one after the other.
        """
        namespace['command.output'] = ''
        namespace['exitcode'] = None
        log.debug('running commands over ssh connection...')
        deferred_key = (
         device, expectset)
        self.all_commands_defer[deferred_key] = defer.Deferred()
        d = defer.succeed(None)
        for (expr, cmdstring) in expectset.commands:
            if expr is None:
                if cmdstring is not None:
                    log.debug("Command '%s' will run without waiting for output." % cmdstring)
                    d.addCallback(self.issue_command, cmdstring, namespace)
                    d.addCallbacks(self.command_completed, self.command_failed, callbackArgs=(namespace,), errbackArgs=(namespace,))
                else:
                    log.debug("cmdstring is 'None', so nothing to do")
            else:
                d.addCallback(self.check_expect_expr, expr, cmdstring, namespace)

        d.addCallbacks(self.all_commands_done, self.all_commands_failure, callbackArgs=(deferred_key, namespace), errbackArgs=(deferred_key, namespace))
        return self.all_commands_defer[deferred_key]

    def check_expect_expr(self, ignored, expr, cmdstring, namespace):
        """
        Check the results from previous commands to see if
        the expression is matched.
        """
        re_expr = re.compile(expr)
        log.debug('compiled expr')
        d = defer.succeed(None)
        match = re_expr.search(namespace['command.output'])
        log.debug('match object is: %s', match)
        if match:
            log.debug("Found expr '%s' in databuf! Yay!" % expr)
            if cmdstring is not None:
                d.addCallback(self.issue_command, cmdstring, namespace)
                d.addCallbacks(self.command_completed, self.command_failed, callbackArgs=(namespace,), errbackArgs=(namespace,))
        return d

    def issue_command(self, ignored, cmdstring, namespace):
        """
        Issue a command string to the remote device
        """
        log.debug('Issuing command: %s', cmdstring)
        cmdstring = str(util.substituteVariables(cmdstring, namespace))
        log.debug('commandstring is: %s', cmdstring)
        namespace['command.send'] = cmdstring
        return self.send_command(cmdstring)

    def send_command(self, cmdstring):
        """
        Override this method in subclasses to send the actual command
        to the remote host.
        """
        return self.conn.exec_remote(cmdstring)

    def command_completed(self, result, namespace):
        """
        When the command is completed, add its output to a
        global resultset. This sets the exitcode to the
        exitcode of the last command that completed, and
        """
        log.debug('a command has completed with result: %s', result)
        namespace['exitcode'] = result[0]
        namespace['command.output'] += result[1]
        log.debug("current results: exit '%d', output: %s", namespace['exitcode'], namespace['command.output'])

    def command_failed(self, failure, namespace):
        """
        If a command failed, pass the failure up the Deferred chain.
        Don't consume the error.
        FIXME: This should probably be a deferred list or similar.
        """
        return failure

    def all_commands_done(self, result, deferred_key, namespace):
        """
        Called when all the commands have completed.
        """
        log.debug('All commands have finished.')
        self.transport.loseConnection()
        self.all_commands_defer[deferred_key].callback(CommandChangeResult((self.exitcode, self.cmdoutput)))