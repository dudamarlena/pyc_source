# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wymypy/plugins/cisco.py
# Compiled at: 2013-12-01 15:54:27
from flask import make_response
from string import Template

class Cisco(object):
    has_panel = False
    button_index = 100
    button_label = ''

    def __init__(self, mpd, config):
        self.config = config
        self.mpd = mpd

    def index(self):
        resp = make_response(Template('<CiscoIPPhoneMenu>\n<Title>WyMyPy</Title>\n<Prompt>Play Music NOW !</Prompt>\n<MenuItem>\n    <Name>Play - Pause</Name>\n    <URL>http://$server/plugin/cisco/playpause</URL>\n</MenuItem>\n<MenuItem>\n    <Name>Stop</Name>\n    <URL>http://$server/plugin/cisco/stop</URL>\n</MenuItem>\n<MenuItem>\n    <Name>Volume Up</Name>\n    <URL>http://$server/plugin/cisco/volup</URL>\n</MenuItem>\n<MenuItem>\n    <Name>Volume Down</Name>\n    <URL>http://$server/plugin/cisco/voldown</URL>\n</MenuItem>\n<MenuItem>\n    <Name>Next</Name>\n    <URL>http://$server/plugin/cisco/next</URL>\n</MenuItem>\n<MenuItem>\n    <Name>Previous</Name>\n    <URL>http://$server/plugin/cisco/prev</URL>\n</MenuItem>\n</CiscoIPPhoneMenu>').substitute(server=config.SERVER_NAME), 200)
        resp.headers['Content-type'] = 'text/xml'
        resp.headers['Connection'] = 'close'
        resp.headers['Expires'] = '-1'
        return resp

    def playpause(self):
        self.mpd.pause()
        return self.index()

    def stop(self):
        self.mpd.stop()
        return self.index()

    def next(self):
        self.mpd.next()
        return self.index()

    def prev(self):
        self.mpd.prev()
        return self.index()

    def volup(self):
        self.mpd.volumeUp()
        return self.index()

    def voldown(self):
        self.mpd.volumeDown()
        return self.index()