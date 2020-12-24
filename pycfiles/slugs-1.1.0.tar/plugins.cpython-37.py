# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/peter/slugs/slugs/plugins.py
# Compiled at: 2018-03-15 13:29:23
# Size of source mod 2**32: 2613 bytes
from cherrypy.process import plugins
import os

class FileMonitoringPlugin(plugins.SimplePlugin):

    def __init__(self, bus, path, callback):
        plugins.SimplePlugin.__init__(self, bus)
        self._callback = callback
        self._path = None
        self._t = 0
        self.path = path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        if os.path.exists(value):
            self._path = value
        else:
            raise ValueError("Monitored file '{}' must be an existing file.".format(value))

    def start(self):
        self.bus.log('Starting file monitoring plugin for file: {}'.format(self._path))
        self.bus.subscribe('main', self.check_path)

    def stop(self):
        self.bus.log('Stopping file monitoring plugin for file: {}'.format(self._path))
        self.bus.unsubscribe('main', self.check_path)

    def check_path(self):
        t = os.path.getmtime(self.path)
        if t > self._t:
            self._t = t
            self.update_data()

    def update_data(self):
        self.bus.log('Monitored file ({}) updated. Reloading data.'.format(self._path))
        data = []
        with open(self._path, 'r') as (f):
            for line in f:
                line = line.strip()
                if line == '':
                    continue
                if line[0] == '#':
                    continue
                entry = line.split(',')
                if len(entry) == 2:
                    data.append([entry[0].strip(), entry[1].strip()])
                else:
                    self.bus.log('Error parsing monitored file ({}). Halting data reload.'.format(self._path))
                    return

        self._callback(data)