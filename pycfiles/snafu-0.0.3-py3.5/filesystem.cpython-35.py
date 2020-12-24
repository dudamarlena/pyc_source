# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snafulib/connectors/filesystem.py
# Compiled at: 2018-07-01 01:56:00
# Size of source mod 2**32: 1216 bytes
import pyinotify, threading, os, configparser
gcb = None
gf = None

class EventHandler(pyinotify.ProcessEvent):

    def process_IN_CREATE(self, event):
        global gcb
        event = {'file': event.pathname, 'action': 'create'}
        gcb(gf, event=event)

    def process_IN_DELETE(self, event):
        event = {'file': event.pathname, 'action': 'delete'}
        gcb(gf, event=event)


def initinternal(function, configpath):
    gf = function
    connecturl = None
    if not configpath:
        configpath = 'snafu.ini'
    if not function:
        function = 'snafu'
    if os.path.isfile(configpath):
        config = configparser.ConfigParser()
        config.read(configpath)
        if function in config and 'connector.filesystem' in config[function]:
            connecturl = config[function]['connector.filesystem']
    if connecturl:
        wm = pyinotify.WatchManager()
        handler = EventHandler()
        notifier = pyinotify.Notifier(wm, handler)
        mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE
        wdd = wm.add_watch(connecturl, mask, rec=True)
        notifier.loop()


def init(cb, function=None, configpath=None):
    global gcb
    gcb = cb
    t = threading.Thread(target=initinternal, daemon=True, args=(function, configpath))
    t.start()