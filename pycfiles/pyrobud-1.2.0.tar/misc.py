# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/robots/helpers/misc.py
# Compiled at: 2015-01-26 11:58:05
from collections import deque

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    enums['values'] = enums.values
    enums['keys'] = enums.keys
    return type('Enum', (), enums)


class valuefilter:
    MAX_LENGTH = 10

    def __init__(self, maxlen=MAX_LENGTH):
        self._vals = deque(maxlen=maxlen)
        self.lastval = 0.0
        self.dirty = True

    def append(self, val):
        self.dirty = True
        self._vals.append(val)

    def get(self):
        if self.dirty:
            self.lastval = sum(self._vals) / len(self._vals)
            self.dirty = False
        return self.lastval


import logging, logging.handlers

def enable_logger_print():

    def _logger_str(self):
        s = ''
        if self.parent is not None:
            s = _logger_str(self.parent)
        s += '\n%s\n' % self.name
        for name, value in self.__dict__.items():
            if name == 'parent':
                value = value and value.name or 'None'
            if name == 'level':
                value = '%s (%s)' % (value, logging.getLevelName(value))
            s += '    %s = %s\n' % (name, value)

        return s

    def _handler_repr(handlername):

        def __repr__(self):
            s = '\n\t%s\n' % handlername
            for name, value in self.__dict__.items():
                if name == 'level':
                    value = '%s (%s)' % (value, logging.getLevelName(value))
                s += '\t    %s = %s\n' % (name, value)

            s += '\t'
            return s

        return __repr__

    def _formatter_repr(self):
        s = ''
        for name, value in self.__dict__.items():
            s += '\n\t\t%s = %s' % (name, value)

        return s

    def _manager_repr(self):
        s = ''
        for name, value in self.__dict__.items():
            if name == 'root':
                value = value.name
            if name == 'loggerDict':
                value = _logger_list()
                name = 'loggerDict keys'
            s += '\n        %s = %s' % (name, value)

        return s

    def _filter_repr(self):
        return self.name

    def _logger_list():
        return sorted([ name for name in logging.Logger.manager.loggerDict ])

    for name in dir():
        if name.endswith('Handler'):
            logging.__dict__[name].__repr__ = _handler_repr(name)

    for name in dir(logging):
        if name.endswith('Handler'):
            logging.__dict__[name].__repr__ = _handler_repr(name)

    for name in dir(logging.handlers):
        if name.endswith('Handler'):
            logging.handlers.__dict__[name].__repr__ = _handler_repr(name)

    logging.Logger.__str__ = _logger_str
    logging.Formatter.__repr__ = _formatter_repr
    logging.Filter.__repr__ = _filter_repr
    logging.Manager.__repr__ = _manager_repr