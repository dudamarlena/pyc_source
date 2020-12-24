# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/event_router.py
# Compiled at: 2013-04-04 15:36:37
from unittest import TestCase
from muntjac.ui.text_field import TextField
from muntjac.data.property import IValueChangeListener

class TestEventRouter(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self._innerListenerCalls = 0

    def testAddInEventListener(self):
        tf = TextField()

        class Outer(IValueChangeListener):

            def __init__(self, test, tf):
                self._test = test
                self._tf = tf

            def valueChange(self, event):

                class Inner(IValueChangeListener):

                    def __init__(self, test):
                        self._test = test

                    def valueChange(self, event):
                        self._test._innerListenerCalls += 1
                        print 'The inner listener was called'

                self._tf.addListener(Inner(self._test), IValueChangeListener)

        tf.addListener(Outer(self, tf), IValueChangeListener)
        tf.setValue('abc')
        tf.setValue('def')
        tf.setValue('ghi')
        self.assertEqual(self._innerListenerCalls, 3)