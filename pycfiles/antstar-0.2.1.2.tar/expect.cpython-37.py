# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/wangping/svn/work/code/project/AntShell/lib/antshell/expect.py
# Compiled at: 2019-10-22 00:36:45
# Size of source mod 2**32: 3561 bytes
from __future__ import absolute_import, division, print_function
from antshell.base import BaseToolsBox
from antshell.utils.errors import DeBug
from antshell.bastion import GetBastionConfig, GetPasswdByTotp
from antshell.config import CONFIG
import pexpect, datetime, time, sys, os, fcntl, errno, signal, socket, select, getpass
from binascii import hexlify
try:
    import termios, tty
except ImportError:
    time.sleep(3)
    sys.exit()

DEBUG = CONFIG.DEFAULT.DEBUG

class Expect(BaseToolsBox):
    """Expect"""

    def exsend(self, e, line):
        e.logfile = None
        e.sendline(line)
        e.logfile = sys.stdout.buffer

    def exConn(self, k, sudo):
        """采用pexcept模块执行"""
        BASTION = k.get('bastion')
        if BASTION:
            bastion = GetBastionConfig()
            ec = 'ssh -p{port} -l {user} {host}'.format(port=(bastion.get('port')),
              user=(bastion.get('user')),
              host=(bastion.get('host')))
            password = bastion.get('passwd')
        else:
            ec = 'ssh -p{port} -l {user} {host}'.format(port=(k.get('port')),
              user=(k.get('user')),
              host=(k.get('ip')))
            password = k.get('passwd')
        e = pexpect.spawn(ec)
        e.logfile = sys.stdout.buffer
        flag = True
        bastion_mode = True
        sudo_mode = True
        try:
            try:
                while flag:
                    i = e.expect(['continue connecting (yes/no)?', '[P|p]assword: ', ':', '.*[\\$#~]'])
                    if i == 0:
                        self.exsend(e, 'yes')
                    if i == 1:
                        self.exsend(e, str(password))
                    if i == 2:
                        if k.get('bastion') == 1:
                            if bastion_mode:
                                self.exsend(e, k.get('ip') + ' ' + str(k.get('port')))
                                bastion_mode = False
                    if i == 3:
                        if k.get('sudo'):
                            if sudo_mode:
                                sudo_user = sudo if sudo else k.get('sudo')
                                self.exsend(e, 'sudo -iu ' + sudo_user)
                                sudo_mode = False
                        flag = False

                e.logfile = None
                e.setwinsize(int(self.rows), int(self.columns))
                e.interact(chr(29))
            except pexpect.EOF:
                print('EOF')
            except pexpect.TIMEOUT:
                print('TIMEOUT')

        finally:
            e.close()