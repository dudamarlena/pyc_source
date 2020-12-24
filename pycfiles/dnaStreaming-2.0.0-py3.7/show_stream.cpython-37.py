# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/dnaStreaming/demo/show_stream.py
# Compiled at: 2020-05-12 03:20:35
# Size of source mod 2**32: 795 bytes
import os
from dnaStreaming.listener import Listener
listener = Listener()
quiet_demo = os.getenv('QUIET_DEMO', 'false') == 'true'
print('\n[ACTIVITY] Receiving messages (SYNC)...\n[0]', end='')

def callback(message, subscription_id, file_handle=None):
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
listener.listen(callback)