# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/emulator/common.py
# Compiled at: 2018-09-18 06:58:30
import json
from threading import Lock
log_file = 'log.log'
DEBUG = False
mutex = Lock()

def Log(log):
    if DEBUG == True:
        with open(log_file, 'a') as (logFp):
            logFp.write(log + '\n')


def update_selected_devices(devices_file, selected_devices, req, device_id):
    dejsonified_prop = req
    found = False
    mutex.acquire()
    if len(selected_devices) > 0:
        for i in range(len(selected_devices)):
            try:
                if device_id == selected_devices[i].get('id'):
                    selected_devices.pop(i)
                    selected_devices.append(dejsonified_prop)
                    found = True
                    break
            except KeyError:
                Log('update_selected_devices : KeyError! : ' + str(device_id))

    if found == False or len(selected_devices) <= 0:
        selected_devices.append(dejsonified_prop)
    with open(devices_file, 'w+') as (jsonfile):
        json.dump(selected_devices, jsonfile)
    jsonfile.close()
    mutex.release()
    return selected_devices