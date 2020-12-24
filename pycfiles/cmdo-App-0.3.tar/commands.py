# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/cmdmessenger/commands.py
# Compiled at: 2015-01-27 21:12:20
__doc__ = '\n'
from . import params

class InvalidCommand(Exception):
    pass


def validate(cmd):
    if isinstance(cmd, (list, tuple)):
        return [ validate(c) for c in cmd ]
    if 'params' in cmd:
        for p in cmd['params']:
            if p not in params.types:
                raise InvalidCommand('Command %s unknown param %s' % (cmd, p))

    if 'name' in cmd:
        if 'id' not in cmd:
            raise InvalidCommand('Command %s missing id' % cmd)
    if 'id' in cmd:
        if 'name' not in cmd:
            raise InvalidCommand('Command %s missing name' % cmd)
    return True


class Callback(object):
    """
    Callbacks are called when a command message is received from the arduino
    """

    def __init__(self, func=None, types=None):
        if func is None:
            raise Exception('Callback func must be defined')
        self.types = types
        if types is None:
            self.nargs = 0
        else:
            self.nargs = len(self.types)
        self.func = func
        return

    def __call__(self, *args):
        if self.nargs == 0:
            self.func()
        else:
            if len(args) != self.nargs:
                raise ValueError('Invalid number of arguments %s != %s' % (
                 len(args), self.nargs))
            self.func(*[ t(a) for t, a in zip(self.types, args) ])


def make_callback(callback):
    if isinstance(callback, Callback):
        return callback
    if isinstance(callback, dict):
        return Callback(callback['function'], callback['params'])
    return Callback(func=callback)


def make_command(send=None, cmd_id=None, types=None):

    def cmd(*args):
        send(cmd_id, *[ params.types[t]['to'](a) for t, a in zip(types, args) ])


class Namespace(object):

    def __init__(self, commands, send):
        for cmd in commands:
            if 'name' in cmd:
                setattr(cmd['name'], make_command(send, cmd['id'], cmd['params']))