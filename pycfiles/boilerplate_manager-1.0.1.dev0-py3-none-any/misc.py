# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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