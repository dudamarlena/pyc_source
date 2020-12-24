# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\services\ssh.py
# Compiled at: 2011-01-03 17:15:11
"""
A SSH server.
"""
from seishub.core import __version__ as SEISHUB_VERSION
from seishub.core.config import IntOption, Option, BoolOption
from seishub.core.core import PackageManager
from seishub.core.defaults import SSH_PORT, SSH_PRIVATE_KEY, SSH_PUBLIC_KEY, SSH_AUTOSTART
from seishub.core.exceptions import SeisHubError
from seishub.core.packages.interfaces import ISSHCommand
from seishub.core.util.text import getFirstSentence
from twisted.application.internet import TCPServer
from twisted.conch import avatar, recvline
from twisted.conch.insults import insults
from twisted.conch.interfaces import IConchUser, ISession
from twisted.conch.ssh import factory, keys, session
from twisted.cred import portal
from twisted.python import components
from zope.interface import implements
import os
__all__ = [
 'SSHService']

class SSHServiceProtocol(recvline.HistoricRecvLine):
    """
    """

    def __init__(self, avatar):
        recvline.HistoricRecvLine.__init__(self)
        self.user = avatar
        self.env = avatar.env
        self.status = {}
        plugins = PackageManager.getComponents(ISSHCommand, None, self.env)
        self.plugin_cmds = dict([ (p.command_id.upper(), p) for p in plugins if hasattr(p, 'executeCommand') and hasattr(p, 'command_id')
                                ])
        self.buildin_cmds = [ f[4:].upper() for f in dir(self) if f.startswith('cmd_')
                            ]
        return

    def connectionMade(self):
        recvline.HistoricRecvLine.connectionMade(self)
        self.writeln('Welcome to SeisHub ' + SEISHUB_VERSION)
        self.showPrompt()

    def showPrompt(self):
        self.write('$ ')

    def characterReceived(self, ch, mch):
        idx = self.lineBufferIndex
        if self.mode == 'insert':
            self.lineBuffer.insert(idx, ch)
        else:
            self.lineBuffer[idx:(idx + 1)] = [
             ch]
        self.lineBufferIndex += 1
        if 'hide' not in self.status:
            self.terminal.write(ch)

    def lineReceived(self, line):
        if self.status:
            cmd = self.status.get('cmd', '')
            try:
                func = getattr(self, 'cmd_' + cmd, None)
                func(line)
            except Exception as e:
                self.writeln('Error: %s' % e)

            return
        line = line.strip()
        if not line:
            self.showPrompt()
            return
        else:
            cmd_and_args = line.split()
            cmd = cmd_and_args[0].upper()
            args = cmd_and_args[1:]
            if cmd in self.buildin_cmds:
                try:
                    func = getattr(self, 'cmd_' + cmd, None)
                    func(*args)
                except Exception as e:
                    self.writeln('Error: %s' % e)

                if not self.status:
                    self.showPrompt()
                return
            if cmd in self.plugin_cmds.keys():
                ssh_cmd = self.plugin_cmds.get(cmd)
                ssh_cmd.env = self.env
                ssh_cmd.executeCommand(self, args)
            else:
                self.writeln('No such command: ' + cmd)
                self.writeln('Use help to get all available commands.')
            self.showPrompt()
            return

    def write(self, data):
        self.terminal.write(data)

    def writeln(self, data):
        self.write(data)
        self.nextLine()

    def nextLine(self):
        self.write('\r\n')

    def handle_RETURN(self):
        if self.lineBuffer and 'hide' not in self.status:
            self.historyLines.append(('').join(self.lineBuffer))
        self.historyPosition = len(self.historyLines)
        line = ('').join(self.lineBuffer)
        self.lineBuffer = []
        self.lineBufferIndex = 0
        self.terminal.nextLine()
        self.lineReceived(line)

    def cmd_HELP(self, *args):
        self.writeln('== Build-in keywords ==')
        for cmd in self.buildin_cmds:
            func = getattr(self, 'cmd_' + cmd, None)
            func_doc = func.__doc__
            if not func_doc:
                continue
            self.writeln(cmd + ' - ' + getFirstSentence(str(func_doc)))

        self.nextLine()
        self.writeln('== Plugin keywords ==')
        for cmd, plugin in self.plugin_cmds.items():
            self.writeln(cmd + ' - ' + getFirstSentence(str(plugin.__doc__)))

        return

    def cmd_VERSION(self):
        """
        Prints the current SeisHub version.
        """
        self.writeln('SeisHub SSH version %s' % SEISHUB_VERSION)

    def cmd_WHOAMI(self):
        """
        Prints your user name.
        """
        self.writeln(self.user.username)

    def cmd_EXIT(self):
        """
        Ends your session.
        """
        self.cmd_QUIT()

    def cmd_QUIT(self):
        """
        Ends your session.
        """
        self.writeln('Bye!')
        self.terminal.loseConnection()

    def cmd_CLEAR(self):
        """
        Clears the screen.
        """
        self.terminal.reset()

    def cmd_PASSWD(self, line=''):
        """
        Changes your password.
        """
        uid = self.user.username
        status = self.status.get('cmd', '')
        current = 'current' in self.status
        password = self.status.get('password', '')
        if not status:
            self.writeln('Changing password for %s' % uid)
            self.write('Enter current password: ')
            self.status = dict(cmd='PASSWD', current='', hide=True)
        elif current:
            if not self.env.auth.checkPassword(uid, line):
                self.status = {}
                self.writeln('Authentication failure.')
                self.showPrompt()
            else:
                self.write('Enter new password: ')
                self.status = dict(cmd='PASSWD', password='', hide=True)
        elif password == '':
            self.write('Retype new password: ')
            self.status = dict(cmd='PASSWD', password=line, hide=True)
        elif password != '':
            if password != line:
                self.writeln('Sorry, passwords do not match.')
            else:
                try:
                    self.env.auth.changePassword(uid, password)
                except SeisHubError as e:
                    self.writeln(str(e))
                except Exception as e:
                    raise e
                else:
                    self.writeln('Password has been changed.')

            self.status = {}
            self.showPrompt()


class SSHServiceSession:

    def __init__(self, avatar):
        self.avatar = avatar

    def getPty(self, term, windowSize, attrs):
        pass

    def execCommand(self, proto, cmd):
        raise NotImplementedError

    def openShell(self, protocol):
        serverProtocol = insults.ServerProtocol(SSHServiceProtocol, self.avatar)
        serverProtocol.makeConnection(protocol)
        protocol.makeConnection(session.wrapProtocol(serverProtocol))

    def eofReceived(self):
        pass

    def closed(self):
        pass

    def windowChanged(self, windowSize):
        pass


class SSHServiceAvatar(avatar.ConchUser):

    def __init__(self, username, env):
        avatar.ConchUser.__init__(self)
        self.username = username
        self.env = env
        self.channelLookup.update({'session': session.SSHSession})


components.registerAdapter(SSHServiceSession, SSHServiceAvatar, ISession)

class SSHServiceRealm:
    implements(portal.IRealm)

    def __init__(self, env):
        self.env = env

    def requestAvatar(self, avatarId, mind, *interfaces):
        if IConchUser in interfaces:
            logout = lambda : None
            return (
             IConchUser, SSHServiceAvatar(avatarId, self.env), logout)
        raise Exception('No supported interfaces found.')


class SSHServiceFactory(factory.SSHFactory):
    """
    Factory for SSH Server.
    """

    def __init__(self, env):
        self.env = env
        self.portal = portal.Portal(SSHServiceRealm(env), env.auth.getCheckers())
        pub, priv = self._getCertificates()
        self.publicKeys = {'ssh-rsa': keys.Key.fromFile(pub)}
        self.privateKeys = {'ssh-rsa': keys.Key.fromFile(priv)}

    def _getCertificates(self):
        """
        Fetch SSH certificate paths from configuration.
        
        return: Paths to public and private key files.
        """
        pub_file = self.env.config.get('ssh', 'public_key_file')
        priv_file = self.env.config.get('ssh', 'private_key_file')
        if not os.path.isabs(pub_file):
            pub_file = os.path.join(self.env.config.path, pub_file)
        if not os.path.isabs(priv_file):
            priv_file = os.path.join(self.env.config.path, priv_file)
        msg = 'SSH certificate file %s is missing!'
        if not os.path.isfile(pub_file):
            self.env.log.warn(msg % pub_file)
            return self._generateCertificates()
        if not os.path.isfile(priv_file):
            self.env.log.warn(msg % priv_file)
            return self._generateCertificates()
        return (
         pub_file, priv_file)

    def _generateCertificates(self):
        """
        Generates new private RSA keys for the SFTP service.
        
        return: Paths to public and private key files.
        """
        from Crypto.PublicKey import RSA
        from twisted.python.randbytes import secureRandom
        pub_file = os.path.join(self.env.config.path, SSH_PUBLIC_KEY)
        priv_file = os.path.join(self.env.config.path, SSH_PRIVATE_KEY)
        msg = 'Generating new certificate files for the SSH service ...'
        self.env.log.warn(msg)
        rsa_key = RSA.generate(1024, secureRandom)
        pub_key = keys.Key(rsa_key).public().toString('openssh')
        file(pub_file, 'w+b').write(str(pub_key))
        msg = 'Private key file %s has been created.'
        self.env.log.warn(msg % pub_file)
        priv_key = keys.Key(rsa_key).toString('openssh')
        file(priv_file, 'w+b').write(str(priv_key))
        msg = 'Private key file %s has been created.'
        self.env.log.warn(msg % priv_file)
        self.env.config.set('ssh', 'public_key_file', pub_file)
        self.env.config.set('ssh', 'private_key_file', priv_file)
        self.env.config.save()
        return (pub_file, priv_file)


class SSHService(TCPServer):
    """
    Service for SSH server.
    """
    service_id = 'ssh'
    BoolOption('ssh', 'autostart', SSH_AUTOSTART, 'Run service on start-up.')
    IntOption('ssh', 'port', SSH_PORT, 'SSH port number.')
    Option('ssh', 'public_key_file', SSH_PUBLIC_KEY, 'Public RSA key.')
    Option('ssh', 'private_key_file', SSH_PRIVATE_KEY, 'Private RSA key.')

    def __init__(self, env):
        self.env = env
        port = env.config.getint('ssh', 'port')
        TCPServer.__init__(self, port, SSHServiceFactory(env))
        self.setName('SSH')
        self.setServiceParent(env.app)

    def privilegedStartService(self):
        if self.env.config.getbool('ssh', 'autostart'):
            TCPServer.privilegedStartService(self)

    def startService(self):
        if self.env.config.getbool('ssh', 'autostart'):
            TCPServer.startService(self)