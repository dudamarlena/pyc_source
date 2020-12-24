# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/sshshell.py
# Compiled at: 2017-08-29 09:44:06
import paramiko
from time import sleep
from scp import SCPClient
import logging

class SshShell(object):
    """ This is a wrapper around paramiko.SSHClient and scp.SCPClient
    I provides a ssh connection with the ability to transfer files over it"""

    def __init__(self, hostname='localhost', user='root', password='root', delay=0.05, timeout=3, sshport=22, shell=True):
        self._logger = logging.getLogger(name=__name__)
        self.delay = delay
        self.apprunning = False
        self.hostname = hostname
        self.sshport = sshport
        self.user = user
        self.password = password
        self.timeout = timeout
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname, username=self.user, password=self.password, port=self.sshport, timeout=timeout)
        if shell:
            self.channel = self.ssh.invoke_shell()
        self.startscp()

    def startscp(self):
        self.scp = SCPClient(self.ssh.get_transport())

    def write(self, text):
        if self.channel.send_ready() and not text == '':
            return self.channel.send(text)
        else:
            return -1

    def read_nbytes(self, nbytes):
        if self.channel.recv_ready():
            return self.channel.recv(nbytes)
        else:
            return ''

    def read(self):
        sumstring = ''
        while True:
            string = self.read_nbytes(1024).decode('utf-8')
            sumstring += string
            if not string:
                break

        self._logger.debug(sumstring)
        return sumstring

    def askraw(self, question=''):
        self.write(question)
        sleep(self.delay)
        return self.read()

    def ask(self, question=''):
        return self.askraw(question + '\n')

    def __del__(self):
        self.endapp()
        try:
            self.channel.close()
        except AttributeError:
            pass

        self.ssh.close()

    def endapp(self):
        pass

    def reboot(self):
        self.endapp()
        self.ask('shutdown -r now')
        self.__del__()

    def shutdown(self):
        self.endapp()
        self.ask('shutdown now')
        self.__del__()

    def get_mac_addresses(self):
        """
        returns all MAC addresses of the SSH device.
        """
        macs = list()
        nextgood = False
        for token in self.ask('ifconfig | grep HWaddr').split():
            if nextgood and len(token.split(':')) == 6:
                macs.append(token)
            if token == 'HWaddr':
                nextgood = True
            else:
                nextgood = False

        return macs