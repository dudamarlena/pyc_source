# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/externals/pysideuic/Compiler/misc.py
# Compiled at: 2020-05-03 00:26:03
# Size of source mod 2**32: 1542 bytes
from pysideuic.Compiler.indenter import write_code

def write_import(module_name, from_imports):
    if from_imports:
        write_code('from . import %s' % module_name)
    else:
        write_code('import %s' % module_name)


def moduleMember(module, name):
    if module:
        return '%s.%s' % (module, name)
    else:
        return name


class Literal(object):
    __doc__ = 'Literal(string) -> new literal\n\n    string will not be quoted when put into an argument list'

    def __init__(self, string):
        self.string = string

    def __str__(self):
        return self.string

    def __or__(self, r_op):
        return Literal('%s|%s' % (self, r_op))