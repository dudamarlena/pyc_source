# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Lib\CommandLine\Arguments.py
# Compiled at: 2005-04-13 18:41:04
__doc__ = '\nClasses that support advanced arg processing for command-line scripts\n\nCopyright 2004 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
from CommandLineUtil import ArgumentError
REQUIRED = 1
OPTIONAL = 2
ZERO_OR_MORE = 3
ONE_OR_MORE = 4

class Argument:
    __module__ = __name__

    def __init__(self, name, description, validationFunc=None):
        self.name = name
        self.description = description
        self.validationFunc = validationFunc or (lambda x: x)
        return


class RequiredArgument(Argument):
    __module__ = __name__
    requirements = REQUIRED

    def gen_command_line(self):
        return self.name

    def validate(self, cmd, args):
        if not len(args):
            raise ArgumentError(cmd, "missing required argument '%s'" % self.name)
        return (self.validationFunc(args[0]), args[1:])


class OptionalArgument(Argument):
    __module__ = __name__
    requirements = OPTIONAL

    def gen_command_line(self):
        return '[%s]' % self.name

    def validate(self, cmd, args):
        if len(args):
            return (self.validationFunc(args[0]), args[1:])
        return (None, [])
        return


class ZeroOrMoreArgument(Argument):
    __module__ = __name__
    requirements = ZERO_OR_MORE

    def gen_command_line(self):
        return '[%s]...' % self.name

    def validate(self, cmd, args):
        eaten = map(lambda x, f=self.validationFunc: f(x), args)
        return (
         eaten, [])


class OneOrMoreArgument(Argument):
    __module__ = __name__
    requirements = ONE_OR_MORE

    def gen_command_line(self):
        return '%s [%s]...' % (self.name, self.name)

    def validate(self, cmd, args):
        if not len(args):
            raise ArgumentError(cmd, "missing required argument '%s'" % self.name)
        eaten = map(lambda x, f=self.validationFunc: f(x), args)
        return (
         eaten, [])