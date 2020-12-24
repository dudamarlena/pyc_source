# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pdfs/Commands/Command.py
# Compiled at: 2017-08-14 16:20:11
# Size of source mod 2**32: 1073 bytes


class Registry(type):

    def __new__(meta, name, bases, namespace):
        cls = type.__new__(meta, name, bases, namespace)
        if not hasattr(meta, 'commands'):
            meta.commands = []
        else:
            meta.commands.append(cls)
        return cls


class Command(metaclass=Registry):

    def __init_subclass__(cls):
        if not hasattr(cls, 'set_args') or not callable(cls.set_args):
            raise AttributeError('Command class needs set_args()')
        else:
            if not hasattr(cls, 'run') or not callable(cls.run):
                raise AttributeError('Command class needs run()')
            if not hasattr(cls, 'command') or not isinstance(cls.command, str):
                raise AttributeError('Command class needs command attribute')
            if not hasattr(cls, 'help') or not isinstance(cls.help, str):
                raise AttributeError('Command class needs help attribute')

    def args(self, subparsers):
        self.sp = subparsers.add_parser((self.command), help=(self.help))
        self.set_args(self.sp)
        self.sp.set_defaults(func=(self.run))