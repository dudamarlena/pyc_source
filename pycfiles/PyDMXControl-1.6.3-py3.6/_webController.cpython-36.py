# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcowley/PycharmProjects/PyDMXControl/PyDMXControl/web/_webController.py
# Compiled at: 2019-06-26 14:48:17
# Size of source mod 2**32: 3862 bytes
"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""
import builtins, logging
from os import path
from threading import Thread
from time import sleep
from typing import Dict, Callable
from flask import Flask
from ._routes import routes
from .. import DMXMINWAIT
from ..utils.timing import TimedEvents
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class WebController:

    def __init__(self, controller: 'Controller', *, callbacks: Dict[(str, Callable)]=None, timed_events: Dict[(str, TimedEvents)]=None, host: str='0.0.0.0', port: int=8080):
        self._WebController__thread = None
        self._WebController__host = host
        self._WebController__port = port
        self._WebController__app = Flask('PyDMXControl Web Controller')
        self._WebController__app.template_folder = path.dirname(__file__) + '/templates'
        self._WebController__app.static_url_path = '/static'
        self._WebController__app.static_folder = path.dirname(__file__) + '/static'
        self._WebController__app.register_blueprint(routes)
        self._WebController__app.parent = self
        self.controller = controller
        self.callbacks = {} if callbacks is None else callbacks
        self._WebController__default_callbacks()
        self._WebController__check_callbacks()
        self.timed_events = {} if timed_events is None else timed_events

        @self._WebController__app.context_processor
        def variables():
            return dict(
             {'controller':self.controller,  'callbacks':self.callbacks,  'timed_events':self.timed_events,  'web_resource':WebController.web_resource}, **)

        self._WebController__running = False
        self.run()

    @staticmethod
    def filemtime(file: str) -> int:
        try:
            return path.getmtime(file)
        except Exception:
            return 0

    @staticmethod
    def web_resource(file: str) -> str:
        return '{}?v={:.0f}'.format(file, WebController.filemtime(path.dirname(__file__) + file))

    def __default_callbacks(self):
        if 'all_on' not in self.callbacks:
            self.callbacks['all_on'] = self.controller.all_on
        else:
            if 'all_off' not in self.callbacks:
                self.callbacks['all_off'] = self.controller.all_off
            if 'all_locate' not in self.callbacks:
                self.callbacks['all_locate'] = self.controller.all_locate

    def __check_callbacks(self):
        for key in self.callbacks.keys():
            if not self.callbacks[key] or not callable(self.callbacks[key]):
                del self.callbacks[key]

    def __run(self):
        has_run = False
        self._WebController__running = True
        while self._WebController__running:
            if not has_run:
                self._WebController__app.run(host=(self._WebController__host), port=(self._WebController__port))
                has_run = True
            sleep(DMXMINWAIT)

    def run(self):
        if not self._WebController__running:
            self._WebController__thread = Thread(target=(self._WebController__run))
            self._WebController__thread.daemon = True
            self._WebController__thread.start()
            print('Started web controller: http://{}:{}'.format(self._WebController__host, self._WebController__port))

    def stop(self):
        self._WebController__running = False