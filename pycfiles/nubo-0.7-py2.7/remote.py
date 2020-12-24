# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nubo/remote.py
# Compiled at: 2013-04-12 07:54:03
"""     
    nubo.remote
    ===========

    Execute remote commands via SSH.

    :copyright: (C) 2013 by Emanuele Rocca.
"""
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

class RemoteHost(object):

    def __init__(self, host, private_key):
        self.host = host
        self.private_key = private_key

    def run_command(self, command, user='root'):
        """Execute the given command as 'user' on the given host. 

        Return stdout, stderr
        """
        ssh.connect(self.host, username=user, key_filename=self.private_key)
        _, stdout, stderr = ssh.exec_command(command)
        return (stdout.read(), stderr.read())

    def whoami(self, user='root'):
        return self.run_command('whoami', user)[0].rstrip('\n')


if __name__ == '__main__':
    host1 = RemoteHost('192.168.122.6', '/home/ema/.ssh/id_rsa')
    print host1.run_command('uptime')[0]