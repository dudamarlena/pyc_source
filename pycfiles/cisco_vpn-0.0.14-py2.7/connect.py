# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/lib/connect.py
# Compiled at: 2015-01-08 22:44:15
import os, sys, time
from subprocess import Popen, PIPE
from os.path import expanduser
import pexpect
home = expanduser('~')

def notify(message):
    os.system("terminal-notifier -sound default -title Cisco VPN '\uf8ff' -message " + message)


def disconnect():
    os.system('/opt/cisco/anyconnect/bin/vpn disconnect')


def connection(address, vpngroup, username, password):
    child = pexpect.spawn('/opt/cisco/anyconnect/bin/vpn -s connect ' + address, maxread=2000)
    child.logfile = sys.stdout
    child.expect('Group: \\[.*\\]')
    child.sendline(vpngroup)
    child.expect('Username: \\[.*\\]')
    child.sendline(username)
    child.expect('Password:')
    child.logfile = None
    child.sendline(password)
    child.logfile = sys.stdout
    child.expect('  >> notice: Please respond to banner.')
    child.delaybeforesend = 1
    child.sendline('y')
    child.sendline('exit')
    child.expect('  >> state: Connected')
    return


def is_connect():
    global inline
    global lines_nums
    global p
    p = Popen(['/opt/cisco/anyconnect/bin/vpn', 'state'], stdout=PIPE, close_fds=True)
    for lines_nums in xrange(1, 7):
        inline = p.stdout.readline()
        if 'state: Connected' in inline:
            notify('Connected')
            return True
        if 'state: Disconnected' in inline:
            notify('Disconnected')
            return False


def read_config():
    text_file = open(home + '/.uap', 'r')
    lines = text_file.read().split('\n')
    return lines


def main():
    while True:
        if not is_connect():
            configure = read_config()
            connection(configure[0], '1', configure[1], configure[2])
        time.sleep(30)


if __name__ == '__main__':
    main()