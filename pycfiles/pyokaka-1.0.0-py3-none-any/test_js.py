# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyojo\tests\browser\test_js.py
# Compiled at: 2013-06-08 11:02:02
__doc__ = ' Tests for the pyojo.js package.\n'
from base import *
from pyojo.js import dijit

def _layout():
    b = dijit.layout.BorderContainer('MiPanel', 'base')
    b.panel('top', 'menubar', content='top')
    b.panel('center', 'main', content='center')
    b.panel('leading', 'sidebar', splitter=True, content='leading', style='padding:0px; margin:0px; width:200px')
    b.panel('bottom', 'status', content='bottom', style='background-color:rgb(239, 239, 239); overflow:hidden;')
    acc = dijit.layout.AccordionContainer('accordion', 'sidebar')
    for i in range(1, 9):
        acc.panel('side%s' % i, 'Side %s' % i)

    tabs = dijit.layout.TabContainer('tabs', 'main')
    for i in range(1, 9):
        tabs.panel('tab%s' % i, 'Tab %s' % i)

    return (
     b, tabs, acc, b.resize())


class Javascript_Generation(pyojoTest):

    def test_Var(self):
        """ js.Var variable assignations.
        """
        block = js.Var('number', 1, False)
        self.code(block)
        self.checkIf('number', 1)
        self.checkIf('number==1')
        self.checkIf("number==='1'", False)


class Javascript_Widgets(pyojoTest):

    def test_Alert(self):
        """ Alert dijit dialog.
        """
        block = js.Alert(pyojo.__version__, 'TESTING')
        self.code(block)
        self.find_id(block.name)
        self.find_id(block.name.replace('dialog', 'btn'))


class Javascript_Dijits(pyojoTest):
    console = False

    def test_layout(self):
        """ Test Layout.
        """
        b = dijit.layout.BorderContainer('MiPanel', 'base')
        b.panel('top', 'menubar', content='top')
        b.panel('center', 'main', content='center')
        b.panel('leading', 'sidebar', splitter=True, content='leading', style='padding:0px; margin:0px; width:200px')
        b.panel('bottom', 'status', content='bottom', style='background-color:rgb(239, 239, 239); overflow:hidden;')
        acc = dijit.layout.AccordionContainer('accordion', 'sidebar')
        for i in range(1, 9):
            acc.panel('side%s' % i, 'Side %s' % i)

        tabs = dijit.layout.TabContainer('tabs', 'main')
        for i in range(1, 9):
            tabs.panel('tab%s' % i, 'Tab %s' % i)

        self.code(b, tabs, acc, b.resize())
        self.find_id('MiPanel')
        self.find_id('menubar')
        self.find_id('main')
        self.find_id('sidebar')
        self.find_id('status')
        self.find_id('side8')
        self.find_id('tab8')


if __name__ == '__main__':
    print '-' * 79 + '\nTesting pyojo version %s' % pyojo.__version__
    try:
        unittest.main()
    except SystemExit as inst:
        if inst.args[0] is True:
            raise