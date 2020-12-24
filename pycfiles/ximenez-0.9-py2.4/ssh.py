# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.11.1-i386/egg/ximenez/shared/ssh.py
# Compiled at: 2007-12-01 11:00:28
"""Define various classes and functions related to SSH.

$Id: ssh.py 42 2007-12-01 16:00:28Z damien.baty $
"""
from popen2 import popen3
from ximenez.shared import ConnectionException
DEFAULT_PORT = '22'

class SSHRemoteHost(object):
    """A class which represents an SSH remote host."""
    __module__ = __name__

    def __init__(self, host, port=None, user=None):
        self.host = host
        self.port = port or DEFAULT_PORT
        self.user = user

    def __repr__(self):
        representation = (':').join((self.host, self.port))
        if self.user:
            representation = '%s@%s' % (self.user, representation)
        return representation

    def execute(self, command):
        """Execute ``command`` on the remote host via SSH and return the
        output.

        This method takes care of escaping ``command`` if needed.
        """
        host = self.host
        if self.user:
            host = '%s@%s' % (self.user, host)
        command = escapeShellCommand(command)
        cmd = 'ssh -p %s %s %s' % (self.port, host, command)
        (stdout, stdin, stderr) = popen3(cmd)
        stdout = stdout.read()
        stderr = stderr.read()
        if stderr.startswith('ssh: %s:' % self.host):
            raise ConnectionException()
        output = stdout + stderr
        output = output.strip()
        return output


def escapeShellCommand(command, special_chars=';&|!><~*{}[]?()$\\`'):
    """Escape special shell characters from ``command``."""
    escaped = ''
    for c in command:
        if c in special_chars:
            escaped += '\\'
        escaped += c

    return escaped