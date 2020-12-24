# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ice/control/controls/tree/tree.py
# Compiled at: 2010-08-27 06:32:04
from zc.resourcelibrary import need
from zope.component import queryUtility
from ice.control.repl.interfaces import IDispatcher

class Pagelet:

    def update(self):
        need('ice.control.tree.css')
        need('ice.control.tree.js')
        if queryUtility(IDispatcher) is not None:
            need('ice.control.repl.css')
            need('ice.control.repl.js')
        self.content = self.context.get_content()
        return