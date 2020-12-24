# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2gameLobby\ipAddresses.py
# Compiled at: 2018-08-15 18:59:29
# Size of source mod 2**32: 3567 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import json, socket, time
try:
    from urllib2 import urlopen
except Exception:
    from urllib.request import urlopen

from sc2gameLobby import gameConstants as c

def getAll():
    return (
     getPublicIPaddress(), getLocalIPaddress(), getMachineIPaddress())


def getMachineIPaddress():
    """visible on this local machine only"""
    return c.LOCALHOST


def getLocalIPaddress():
    """visible to other machines on LAN"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('google.com', 0))
        my_local_ip = s.getsockname()[0]
    except Exception:
        my_local_ip = None

    return my_local_ip


def getPublicIPaddress(timeout=c.DEFAULT_TIMEOUT):
    """visible on public internet"""
    start = time.time()
    my_public_ip = None
    e = Exception
    while my_public_ip == None:
        if time.time() - start > timeout:
            break
        try:
            my_public_ip = json.load(urlopen('http://httpbin.org/ip'))['origin']
            if my_public_ip:
                break
        except Exception as e:
            print(type(e), e, 'http://httpbin.org/ip')

        try:
            my_public_ip = json.load(urlopen('http://jsonip.com'))['ip']
            if my_public_ip:
                break
        except Exception as e:
            print(type(e), e, 'http://jsonip.com')

        try:
            my_public_ip = load(urlopen('https://api.ipify.org/?format=json'))['ip']
            if my_public_ip:
                break
        except Exception as e:
            print(type(e), e, 'https://api.ipify.org/')

        try:
            my_public_ip = urlopen('http://ip.42.pl/raw').read()
            if my_public_ip:
                break
        except Exception as e:
            print(type(e), e, 'http://ip.42.pl/raw')

    if not my_public_ip:
        raise e
    return my_public_ip