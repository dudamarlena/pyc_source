# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wok_hooks/misc.py
# Compiled at: 2014-10-05 10:58:48
import logging as log, json

class Configuration(dict):

    def __init__(self, path, **kwargs):
        dict.__init__(self)
        self.path = path
        self.update(kwargs)
        self.load()

    def load(self):
        try:
            with open(self.path, 'rb') as (file_handler):
                self.update(json.loads(file_handler.read().decode('utf-8')))
                file_handler.close()
        except IOError:
            log.debug('No such configuration file: %s' % self.path)

    def save(self):
        with open(self.path, 'wb+') as (file_handler):
            file_handler.write(json.dumps(self))
            file_handler.close()