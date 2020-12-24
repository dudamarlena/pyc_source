# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snafulib/connectors/messaging.py
# Compiled at: 2018-07-01 01:56:00
# Size of source mod 2**32: 1171 bytes
import kombu, threading, time, os, configparser
gcb = None

def initinternal(function, configpath):
    global gcb
    connecturl = None
    if not configpath:
        configpath = 'snafu.ini'
    if not function:
        function = 'snafu'
    if os.path.isfile(configpath):
        config = configparser.ConfigParser()
        config.read(configpath)
        if function in config and 'connector.messaging' in config[function]:
            connecturl = config[function]['connector.messaging']
    if not connecturl:
        return
    print('(messaging:connecting)')
    connection = kombu.Connection(connecturl)
    connection.connect()
    print('(messaging:connected)')
    queue = connection.SimpleQueue('sslq')
    while True:
        try:
            message = queue.get(block=True, timeout=20)
        except:
            print('(messaging:pass)')
        else:
            print('(messaging:received {})'.format(message.payload))
            message.ack()
            response = gcb(function, event='{}')

    queue.close()


def init(cb, function=None, configpath=None):
    global gcb
    gcb = cb
    t = threading.Thread(target=initinternal, daemon=True, args=(function, configpath))
    t.start()