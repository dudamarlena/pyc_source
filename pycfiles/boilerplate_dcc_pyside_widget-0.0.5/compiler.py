# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\symlinks\repos\boilerplate_dcc_pyside_widget\boilerplate_dcc_pyside_widget\lib\third_party\pysideuic\Compiler\compiler.py
# Compiled at: 2015-08-04 11:44:30
import sys
from pysideuic.properties import Properties
from pysideuic.uiparser import UIParser
from pysideuic.Compiler import qtproxies
from pysideuic.Compiler.indenter import createCodeIndenter, getIndenter, write_code
from pysideuic.Compiler.qobjectcreator import CompilerCreatorPolicy
from pysideuic.Compiler.misc import write_import

class UICompiler(UIParser):

    def __init__(self):
        UIParser.__init__(self, qtproxies.QtCore, qtproxies.QtGui, CompilerCreatorPolicy())

    def reset(self):
        qtproxies.i18n_strings = []
        UIParser.reset(self)

    def setContext(self, context):
        qtproxies.i18n_context = context

    def createToplevelWidget(self, classname, widgetname):
        indenter = getIndenter()
        indenter.level = 0
        indenter.write('from PySide import QtCore, QtGui')
        indenter.write('')
        indenter.write('class Ui_%s(object):' % self.uiname)
        indenter.indent()
        indenter.write('def setupUi(self, %s):' % widgetname)
        indenter.indent()
        w = self.factory.createQObject(classname, widgetname, (), is_attribute=False, no_instantiation=True)
        w.baseclass = classname
        w.uiclass = 'Ui_%s' % self.uiname
        return w

    def setDelayedProps(self):
        write_code('')
        write_code('self.retranslateUi(%s)' % self.toplevelWidget)
        UIParser.setDelayedProps(self)

    def finalize(self):
        indenter = getIndenter()
        indenter.level = 1
        indenter.write('')
        indenter.write('def retranslateUi(self, %s):' % self.toplevelWidget)
        indenter.indent()
        if qtproxies.i18n_strings:
            for s in qtproxies.i18n_strings:
                indenter.write(s)

        else:
            indenter.write('pass')
        indenter.dedent()
        indenter.dedent()
        self._resources = self.resources

    def compileUi(self, input_stream, output_stream, from_imports):
        createCodeIndenter(output_stream)
        w = self.parse(input_stream)
        indenter = getIndenter()
        indenter.write('')
        self.factory._cpolicy._writeOutImports()
        for res in self._resources:
            write_import(res, from_imports)

        return {'widgetname': str(w), 'uiclass': w.uiclass, 
           'baseclass': w.baseclass}