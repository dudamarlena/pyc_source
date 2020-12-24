# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/omnilog/sshh.py
# Compiled at: 2016-03-08 18:23:57
# Size of source mod 2**32: 1943 bytes
import io, paramiko

class SSHhandler(object):
    __doc__ = '\n    Our SSH wrapper class for paramiko. Its not only a wrapper class.\n    It has some responsibility , that is , return the proper ssh connection\n    object taking in count the config passed.\n    '

    def __init__(self, config):
        self.config = config

    def get_session(self):
        """
        Determines what auth method need to use.
        :return: object connection
        """
        if 'password' in self.config.keys():
            ssh = self.connect_with_password()
        else:
            if 'privateKey' in self.config.keys():
                ssh = self.connect_with_private_key()
            else:
                ssh = self.connect_with_system_keys()
        return ssh

    def connect_with_password(self):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.config['hostname'], password=self.config['password'], username=self.config['username'], port=self.config['port'])
        return ssh

    def connect_with_system_keys(self):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.config['hostname'], username=self.config['username'], port=self.config['port'])
        return ssh

    def connect_with_private_key(self):
        pkfile = io.StringIO(open(self.config['privateKey']['path'], 'r').read())
        pkey = paramiko.RSAKey.from_private_key(pkfile, password=self.config['privateKey']['passphrase'])
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.config['hostname'], username=self.config['username'], port=self.config['port'], pkey=pkey, look_for_keys=False)
        return ssh