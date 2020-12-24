# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/zwsun/workspace/python/corunner/corunner/common/NetUtil.py
# Compiled at: 2013-10-09 12:24:54
import os, socket
if os.name != 'nt':
    import fcntl, struct

def getInterfaceIP(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 35093, struct.pack('256s', ifname[:15]))[20:24])


def __getLocalIP():
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith('127.') and os.name != 'nt':
        interfaces = ['eth0',
         'eth1',
         'eth2',
         'wlan0',
         'wlan1',
         'wifi0',
         'ath0',
         'ath1',
         'ppp0']
        for ifname in interfaces:
            try:
                ip = getInterfaceIP(ifname)
                break
            except IOError:
                pass

    localIP = ip
    return localIP


LOCAL_IP = __getLocalIP()

def getLocalIP():
    return LOCAL_IP


def isLocal(addr):
    return addr == 'localhost' or addr == '127.0.0.1' or addr == LOCAL_IP