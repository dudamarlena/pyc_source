# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bruno1/Developing/Python-Files/express_vpn/express/connections.py
# Compiled at: 2017-08-28 22:16:53
# Size of source mod 2**32: 639 bytes
import os, time

def connect():
    os.system('/usr/bin/expressvpn connect ' + self.myalias)
    return connect


def reconnect():
    os.system('/usr/bin/expressvpn disconnect')
    time.sleep(2)
    os.system('/usr/bin/expressvpn connect ' + self.myalias)
    return reconnect


def disconnect():
    os.system('/usr/bin/expressvpn disconnect')
    return disconnect


def autoconnect():
    os.system('/usr/bin/expressvpn connect')
    return autoconnect


def status2(a):
    a = os.system('/usr/bin/expressvpn status')
    return a


def version():
    os.system('/usr/bin/expressvpn version')
    return version