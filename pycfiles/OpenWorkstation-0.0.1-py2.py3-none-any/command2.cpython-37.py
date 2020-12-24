# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/l0/ss9rqt5j7xbg0x2bpvmjx_k40000gp/T/pip-install-n2xwwglt/workstation/workstation/robot2/command2.py
# Compiled at: 2019-09-24 08:15:55
# Size of source mod 2**32: 848 bytes


class Command(object):

    def __init__(self, do=None, setup=None, description=None):
        assert callable(do)
        self.setup = setup
        self.do = do
        self.description = description

    def __call__(self):
        if self.setup:
            self.setup()
        self.do()

    def __str__(self):
        return self.description or ''


class Macro(object):

    def __init__(self, description):
        self.description = description
        self._commands = []

    def add(self, command):
        if not isinstance(command, Command):
            raise TypeError('Expected object of type Command. Got "{}"'.format(type(command).__name__))
        self._commands.append(command)

    def do(self):
        for command in self._commands:
            command.do()

    __call__ = do