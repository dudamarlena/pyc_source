# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/component/tree_listeners.py
# Compiled at: 2013-04-04 15:36:37
from muntjac.test.server.component.abstract_listener_methods_test import AbstractListenerMethodsTest
from muntjac.ui.tree import Tree, ExpandEvent, IExpandListener, CollapseEvent, ICollapseListener
from muntjac.event.item_click_event import ItemClickEvent, IItemClickListener

class TreeListeners(AbstractListenerMethodsTest):

    def testExpandListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Tree, ExpandEvent, IExpandListener)

    def testItemClickListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Tree, ItemClickEvent, IItemClickListener)

    def testCollapseListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Tree, CollapseEvent, ICollapseListener)