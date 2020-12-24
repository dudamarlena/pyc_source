# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/titan/devicemgmt.py
# Compiled at: 2014-10-17 04:08:57
from __future__ import unicode_literals
import datetime, json
from os import environ
from sys import exit
from os.path import join
from titan import __version__ as version, http
from titan.tools import system as s
import urllib2, urllib, httplib, json
from config import titanConfig
TITAN_PATH = environ.get(b'TITAN_PATH') or b'/var/lib/titan/'
TITAN_CONFIG = join(b'/etc/', b'titan.conf')
CONFIG = titanConfig(TITAN_CONFIG, TITAN_PATH)
software = s.sw_details()
hardware = s.hw_details()
TOKEN = {b'token': CONFIG[b'reporting'][b'token']}
data = {}
data[b'serial'] = hardware[b'serial_number']

def status():
    PREFIX = b'[ Manager::Status ] '
    print PREFIX, b'Checking status for remote server'
    code, resp = http.request(b'%s/api/status/%s' % (CONFIG[b'reporting'][b'target'], data[b'serial']))
    if code == 0:
        print PREFIX, b'Unable To Communicate With Registration Server'
        return False
    if code == 200:
        print PREFIX, b'Device is registered with', CONFIG[b'reporting'][b'target']
        device = json.loads(resp)
        print b''
        print b'Remote ID: %s' % device[b'id']
        print b'Serial: %s' % device[b'serial']
        print b'This device is a %s %s with an %s @ %s and %s of memory running %s' % (device[b'make'], device[b'model'], device[b'cpu_type'], device[b'cpu_speed'], device[b'physical_memory'], device[b'os_version'])
    else:
        print PREFIX, b'Device is not registered'


def unregister():
    PREFIX = b'[ Manager::Unregister ] '
    print PREFIX, b'Checking status for remote server'
    code, resp = http.request(b'%s/api/unregister/%s' % (CONFIG[b'reporting'][b'target'], data[b'serial']), type=b'delete')
    if code == 0:
        print PREFIX, b'Unable To Communicate With Registration Server'
        return False
    if code == 410:
        print PREFIX, b'Unregistered Successfully'
    elif code == 404:
        print PREFIX, b'Device not registered'
    else:
        print PREFIX, b'Error'


def register():
    PREFIX = b'[ Manager::Register ] '
    print PREFIX, b'Attempting to register device with remote server'
    data[b'uuid'] = hardware[b'hardware_uuid']
    data[b'make'] = hardware[b'machine_make']
    data[b'model'] = hardware[b'model_short']
    data[b'cpu_type'] = hardware[b'cpu_type']
    data[b'cpu_speed'] = hardware[b'cpu_speed']
    data[b'physical_memory'] = hardware[b'physical_memory']
    data[b'os_version'] = software[b'os_version']
    data[b'os_build'] = software[b'os_build']
    code, resp = send_request(b'%s/api/status/%s' % (CONFIG[b'reporting'][b'target'], data[b'serial']), data)
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
        print PREFIX, b"Registration Failed, Error: %d - '%s'" % (code, resp)
        return False


def send_request(target, data):
    return http.request(target, data)