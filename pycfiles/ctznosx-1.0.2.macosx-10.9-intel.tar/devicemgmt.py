# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/ctznosx/devicemgmt.py
# Compiled at: 2014-08-24 12:02:51
from __future__ import unicode_literals
import datetime
from os import environ
from sys import exit
from os.path import join
from ctznosx import __version__ as version
from titantools import system as s
import urllib2, urllib, httplib, json
from config import ctznConfig
CTZNOSX_PATH = environ.get(b'CTZNOSX_PATH') or b'/var/lib/ctznosx/'
CTZNOSX_CONFIG = join(b'/etc/', b'ctznosx.conf')
CONFIG = ctznConfig(CTZNOSX_CONFIG, CTZNOSX_PATH)
software = s.sw_details()
hardware = s.hw_details()
PREFIX = b'[ Manager::Register ] '

def register_device():
    print PREFIX, b'Attempting to register device with remote server'
    data = {}
    data[b'serial'] = hardware[b'serial_number']
    data[b'uuid'] = hardware[b'hardware_uuid']
    data[b'make'] = hardware[b'machine_make']
    data[b'model'] = hardware[b'model_short']
    data[b'cpu_type'] = hardware[b'cpu_type']
    data[b'cpu_speed'] = hardware[b'cpu_speed']
    data[b'physical_memory'] = hardware[b'physical_memory']
    data[b'os_version'] = software[b'os_version']
    data[b'os_build'] = software[b'os_build']
    code, resp = send_request(b'%s/connect/%s' % (CONFIG[b'reporting'][b'target'], data[b'serial']), data)
    if code == 0:
        print PREFIX, b'Unable To Communicate With Registration Server'
        return False
    else:
        if code == 304:
            print PREFIX, b'Device already registered'
            return True
        if code == 200:
            print PREFIX, b'Device Registered Successfully'
            return True
        print PREFIX, b"Registration Failed, Error: %d - '%s'" % (code, response)
        return False


def send_request(target, data):
    try:
        request = urllib2.Request(target, urllib.urlencode(data))
        request.add_header(b'User-Agent', b'ctznOSX %s' % version)
        opener = urllib2.build_opener()
        response = opener.open(request)
        response_object = (response.getcode(), response)
    except urllib2.HTTPError as e:
        if e.code == 307:
            print PREFIX, b'This device needs to be registered'
            for line in str(e.headers).splitlines():
                if b'Location' in line:
                    new_target = line.split(b': ', 1)[1]
                    response_object = send_request(new_target, data)

        else:
            response_object = (
             e.code, e.read())
    except urllib2.URLError as e:
        response_object = (0, 'Connection Refused')

    return response_object