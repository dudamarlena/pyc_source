# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snafulib/connectors/cron.py
# Compiled at: 2018-07-01 01:56:00
# Size of source mod 2**32: 754 bytes
import threading, time, os, configparser
gcb = None

def initinternal(function, configpath):
    global gcb
    connectconfig = None
    if not configpath:
        configpath = 'snafu.ini'
    if not function:
        function = 'snafu'
    if os.path.isfile(configpath):
        config = configparser.ConfigParser()
        config.read(configpath)
        if function in config and 'connector.cron' in config[function]:
            connectconfig = int(config[function]['connector.cron'])
    if connectconfig:
        while True:
            time.sleep(connectconfig)
            response = gcb(function, event='{}')


def init(cb, function=None, configpath=None):
    global gcb
    gcb = cb
    t = threading.Thread(target=initinternal, daemon=True, args=(function, configpath))
    t.start()