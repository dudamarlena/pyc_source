# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/zoinksftp/ssh.py
# Compiled at: 2009-02-04 10:21:34
"""Friendly Python SSH2 interface.

http://commandline.org.uk/python/sftp-python-really-simple-ssh

This code was copied from:

 * http://media.commandline.org.uk//code/ssh.txt

"""
import os, logging, tempfile, paramiko

class Connection(object):
    """Connects and logs into the specified hostname. 
    Arguments that are not given are guessed from the environment."""
    __module__ = __name__

    def __init__(self, host, username=None, private_key=None, password=None, port=22):
        self.log = logging.getLogger('zoinksftp.ssh.Connection')
        self._sftp_live = False
        self._sftp = None
        if not username:
            username = os.environ['LOGNAME']
        templog = tempfile.mkstemp('.txt', 'ssh-')[1]
        paramiko.util.log_to_file(templog)
        self._transport = paramiko.Transport((host, port))
        self._tranport_live = True
        if password:
            self._transport.connect(username=username, password=password)
        else:
            if not private_key:
                if os.path.exists(os.path.expanduser('~/.ssh/id_rsa')):
                    private_key = '~/.ssh/id_rsa'
                elif os.path.exists(os.path.expanduser('~/.ssh/id_dsa')):
                    private_key = '~/.ssh/id_dsa'
                else:
                    raise TypeError, 'You have not specified a password or key.'
            private_key_file = os.path.expanduser(private_key)
            rsa_key = paramiko.RSAKey.from_private_key_file(private_key_file)
            self._transport.connect(username=username, pkey=rsa_key)
        return

    def _sftp_connect(self):
        """Establish the SFTP connection."""
        if not self._sftp_live:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
            self._sftp_live = True

    def get(self, remotepath, localpath=None):
        """Copies a file between the remote host and the local host."""
        if not localpath:
            localpath = os.path.split(remotepath)[1]
        self._sftp_connect()
        self._sftp.get(remotepath, localpath)

    def getdir(self, remotepath, localpath=None):
        """Copies and entire directory from remote to local.

      Based on what is seen by listdir.
      
      This does not recurse through a directory tree currently. If 
      a directory is encountered then you'll see and unable to recover 
      error message.

      """
        if not localpath:
            localpath = os.path.abspath(os.curdir)
        self._sftp_connect()
        for i in self._sftp.listdir(remotepath):
            try:
                self._sftp.get('%s/%s' % (remotepath, i), '%s/%s' % (localpath, i))
            except IOError, e:
                self.log.warn("unable to recover item '%s'" % i)

    def put(self, localpath, remotepath=None):
        """Copies a file between the local host and the remote host."""
        if not remotepath:
            remotepath = os.path.split(localpath)[1]
        self._sftp_connect()
        self._sftp.put(localpath, remotepath)

    def execute(self, command):
        """Execute the given commands on a remote machine."""
        channel = self._transport.open_session()
        channel.exec_command(command)
        output = channel.makefile('rb', -1).readlines()
        if output:
            return output
        else:
            return channel.makefile_stderr('rb', -1).readlines()

    def close(self):
        """Closes the connection and cleans up."""
        if self._sftp_live:
            self._sftp.close()
            self._sftp_live = False
        if self._tranport_live:
            self._transport.close()
            self._tranport_live = False

    def __del__(self):
        """Attempt to clean up if not explicitly closed."""
        try:
            self.close()
        except AttributeError, e:
            pass