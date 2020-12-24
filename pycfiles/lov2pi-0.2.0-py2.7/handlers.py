# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/lov2pi/handlers.py
# Compiled at: 2015-09-25 13:37:58
import subprocess

def gpio_handler(data):
    if data['command'] == 'set_direction':
        print data['direction']
        print data['pin']
        return 'ok'
    if data['command'] == 'read_value':
        print data['pin']
    elif data['command'] == 'set_value':
        print data['pin']
        print data['value']
    else:
        return 'error'


def pwm_handler(command):
    print command


def camera_handler(command):
    print command


def ssh_handler(data):
    return subprocess.check_output(data['command'], shell=True)