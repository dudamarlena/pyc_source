# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\client\ssh.py
# Compiled at: 2018-08-27 17:21:06
import paramiko

class SSHClient(paramiko.SSHClient):
    """Save a Paramiko SSH Connection"""

    def __init__(self, username, host, password):
        port = 22
        self.host = host
        super(SSHClient, self).__init__()
        self.load_system_host_keys()
        self.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connect(host, port, username, password)