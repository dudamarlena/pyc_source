# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/emulator/timer.py
# Compiled at: 2018-09-18 06:58:30
import emulator.paho.mqtt.publish, emulator.paho.mqtt.subscribe
from emulator.functions import generate_alive_messages
from emulator.common import update_selected_devices
import time, json, os
log_file = 'log.log'
hostname = 'localhost'
DEBUG = True
devices_file = ''

def Log(log):
    if DEBUG == True:
        with open(log_file, 'a') as (logFp):
            logFp.write(log + '\n')


def stub_event_thread_loop(args):
    devices_file = os.path.dirname(os.path.realpath(__file__)) + '/../' + args
    while True:
        selected_devices = json.load(open(devices_file))
        for d in range(len(selected_devices)):
            device = selected_devices[d]
            if device['power_source'] == 'battery':
                dtime = device['time']
                dwakeup = float(device['wakeup_interval'])
                if time.time() - dtime > dwakeup:
                    topic, report = generate_alive_messages(device)
                    Log('handler : ' + str(topic) + ' : ' + str(report))
                    emulator.paho.mqtt.publish.single(topic, json.dumps(report), hostname=hostname)
                    device['time'] = time.time()
                    update_selected_devices(devices_file, selected_devices, device, device['id'])
                time.sleep(0.5)