# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\symlinks\repos\boilerplate_dcc_pyside_widget\boilerplate_dcc_pyside_widget\lib\third_party\pysideuic\Compiler\indenter.py
# Compiled at: 2015-08-04 11:44:30
indentwidth = 4
_indenter = None

class _IndentedCodeWriter(object):

    def __init__(self, output):
        self.level = 0
        self.output = output

    def indent(self):
        self.level += 1

    def dedent(self):
        self.level -= 1

    def write(self, line):
        if line.strip():
            if indentwidth > 0:
                indent = ' ' * indentwidth
                line = line.replace('\t', indent)
            else:
                indent = '\t'
            self.output.write('%s%s\n' % (indent * self.level, line))
        else:
            self.output.write('\n')


def createCodeIndenter(output):
    global _indenter
    _indenter = _IndentedCodeWriter(output)


def getIndenter():
    return _indenter


def write_code(string):
    _indenter.write(string)