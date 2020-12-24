# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/component/popup_view_listeners.py
# Compiled at: 2013-04-04 15:36:37
from muntjac.test.server.component.abstract_listener_methods_test import AbstractListenerMethodsTest
from muntjac.ui.popup_view import PopupView, PopupVisibilityEvent, IPopupVisibilityListener
from muntjac.ui.label import Label

class PopupViewListeners(AbstractListenerMethodsTest):

    def testPopupVisibilityListenerAddGetRemove(self):
        self._testListenerAddGetRemove(PopupView, PopupVisibilityEvent, IPopupVisibilityListener, PopupView('', Label()))