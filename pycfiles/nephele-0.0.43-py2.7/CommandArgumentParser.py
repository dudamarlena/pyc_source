# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/nephele/CommandArgumentParser.py
# Compiled at: 2017-03-08 10:01:39
import argparse, cmd, shlex
from SilentException import SilentException

class VAction(argparse.Action):

    def __call__(self, parser, args, values, option_string=None):
        if values == None:
            values = '1'
        try:
            values = int(values)
        except ValueError:
            values = values.count('v') + 1

        setattr(args, self.dest, values)
        return


class CommandArgumentParser(argparse.ArgumentParser):

    def __init__(self, command=None):
        argparse.ArgumentParser.__init__(self, prog=command)

    def exit(self, status=0, message=None):
        if None == message:
            raise SilentException()
        else:
            raise Exception(message)
        return

    def error(self, message):
        raise Exception(message)

    def parse_args(self, commandLine):
        if isinstance(commandLine, basestring):
            commandLine = shlex.split(commandLine)
        return super(CommandArgumentParser, self).parse_args(commandLine)