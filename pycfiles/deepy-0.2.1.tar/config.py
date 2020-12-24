# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/conf/config.py
# Compiled at: 2016-04-20 00:05:45


class GeneralConfig(object):

    def __init__(self, logger=None):
        """
        Create a general config
        """
        object.__setattr__(self, 'attrs', {})
        object.__setattr__(self, 'used_parameters', set())
        object.__setattr__(self, 'undefined_parameters', set())
        object.__setattr__(self, 'logger', logger)

    def __getattr__(self, key):
        self.used_parameters.add(key)
        if key not in self.attrs:
            self.undefined_parameters.add(key)
            return
        else:
            return self.attrs[key]
            return

    def __setattr__(self, key, value):
        self.attrs[key] = value

    def get(self, key, default=None):
        key = getattr(self, key)
        if key != None:
            return key
        else:
            return default
            return

    def merge(self, config):
        for k in config.attrs:
            setattr(self, k, getattr(config, k))

        return self

    def report(self):
        """
        Report usage of training parameters.
        """
        if self.logger:
            self.logger.info('accessed parameters:')
            for key in self.used_parameters:
                self.logger.info(' - %s %s' % (key, '(undefined)' if key in self.undefined_parameters else ''))