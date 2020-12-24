# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\symlinks\repos\boilerplate_dcc_pyside_widget\boilerplate_dcc_pyside_widget\lib\third_party\pysideuic\Compiler\misc.py
# Compiled at: 2015-08-04 11:44:30
from pysideuic.Compiler.indenter import write_code

def write_import(module_name, from_imports):
    if from_imports:
        write_code('from . import %s' % module_name)
    else:
        write_code('import %s' % module_name)


def moduleMember(module, name):
    if module:
        return '%s.%s' % (module, name)
    return name


class Literal(object):
    """Literal(string) -> new literal

    string will not be quoted when put into an argument list"""

    def __init__(self, string):
        self.string = string

    def __str__(self):
        return self.string

    def __or__(self, r_op):
        return Literal('%s|%s' % (self, r_op))