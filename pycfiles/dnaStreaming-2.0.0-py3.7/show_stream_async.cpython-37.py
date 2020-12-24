# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/dnaStreaming/demo/show_stream_async.py
# Compiled at: 2020-05-12 03:20:35
# Size of source mod 2**32: 1026 bytes
import os
from time import sleep
from dnaStreaming.listener import Listener
listener = Listener()
quiet_demo = os.getenv('QUIET_DEMO', 'false') == 'true'
max_secs = 5
print(('\n[ACTIVITY] Receiving messages (ASYNC) for {} seconds...\n[0]'.format(max_secs)), end='')

def callback(message, subscription_id):
    callback.counter += 1
    if not quiet_demo:
        if message['action'] != 'del':
            print('[INFO] [MSG] [{}]: AN: {}, TITLE: {}'.format(callback.counter, message['an'], message['title']))
        else:
            print('[INFO] [MSG] [{}]: AN: {}, *** DELETE ***'.format(callback.counter, message['an']))
    elif callback.counter % 10 == 0:
        print(('[{}]'.format(callback.counter)), end='')
    else:
        print('.', end='')
    return True


callback.counter = 0
future = listener.listen_async(callback)
for count in range(0, max_secs):
    sleep(1)

if future.running():
    future.cancel()
print('stop receiving messages')