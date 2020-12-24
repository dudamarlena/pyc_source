# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/component/abstract_text_field_listeners.py
# Compiled at: 2013-04-04 15:36:37
from muntjac.test.server.component.abstract_listener_methods_test import AbstractListenerMethodsTest
from muntjac.ui.text_field import TextField
from muntjac.event.field_events import TextChangeEvent, ITextChangeListener, FocusEvent, IFocusListener, BlurEvent, IBlurListener

class TestAbstractTextFieldListeners(AbstractListenerMethodsTest):

    def testTextChangeListenerAddGetRemove(self):
        self._testListenerAddGetRemove(TextField, TextChangeEvent, ITextChangeListener)

    def testFocusListenerAddGetRemove(self):
        self._testListenerAddGetRemove(TextField, FocusEvent, IFocusListener)

    def testBlurListenerAddGetRemove(self):
        self._testListenerAddGetRemove(TextField, BlurEvent, IBlurListener)