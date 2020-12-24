# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shellout.py
# Compiled at: 2009-03-28 19:21:38
"""
shellout provides an OO-like interface to running shell commands.

Example::
    import shellout as so
    print so.echo("hello, world")
"""
import sys

class ShellOutArg(object):

    def __init__(self, cmd_string, arg_name):
        self._cmd_string = cmd_string
        self._arg = None
        if len(arg_name) == 1:
            self._arg_name = ' -' + arg_name
            self._longopt = False
        else:
            self._arg_name = ' --' + arg_name
            self._longopt = True
        self._called = False
        return

    def __getattr__(self, x):
        cmd = self._cmd_string + self._arg_name
        if self._arg:
            if self._longopt:
                cmd += '='
            else:
                cmd += ' '
            cmd += '"%s"' % self._arg
        return self.__class__(cmd, x)

    def __getitem__(self, arg):
        self._arg = arg
        self._called = True
        return self

    def __call__(self, *args):
        import commands
        cmd = self._cmd_string + self._arg_name
        if self._arg:
            if self._longopt:
                cmd += '='
            else:
                cmd += ' '
            cmd += '"%s"' % self._arg
        if len(args) > 0:
            cmd += ' ' + (' ').join([ '"%s"' % x for x in args ])
        return commands.getoutput(cmd)


class ShellOutCommand(object):
    _soa = ShellOutArg

    def __init__(self, cmd):
        self._cmd = cmd

    def __getattr__(self, x):
        return self._soa(self._cmd, x)

    def __call__(self, *args):
        import commands
        to_run = self._cmd + ' ' + (' ').join([ '"%s"' % x for x in args ])
        results = commands.getstatusoutput(to_run)
        if results[0] != 0:
            raise OSError(results)
        return results[1]


class ShellOutModule(object):
    __doc__ = sys.modules[__name__].__doc__

    def __init__(self):
        self._soc = ShellOutCommand
        self._soa = ShellOutArg

    def __getattr__(self, x):
        return self._soc(x)


sys.modules[__name__] = ShellOutModule()