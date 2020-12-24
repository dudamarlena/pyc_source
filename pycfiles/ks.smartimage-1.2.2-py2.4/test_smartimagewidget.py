# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/smartimage/tests/test_smartimagewidget.py
# Compiled at: 2008-12-23 17:55:57
import unittest
from zope.app.testing.placelesssetup import PlacelessSetup
from zope.app.form.browser.tests import support
from ks.smartimage.smartimageschema.smartimagewidget import ObjectWidget
from zope.schema import Text
from zope.app.form.browser.widget import SimpleInputWidget
from zope.interface import Interface, implements
from zope.publisher.browser import TestRequest
from zope.app.form.interfaces import ConversionError
from zope.app.form.interfaces import WidgetInputError, MissingInputError

class BrowserWidgetTest(PlacelessSetup, support.VerifyResults, unittest.TestCase):
    __module__ = __name__
    _FieldFactory = Text
    _WidgetFactory = None

    def setUpContent(self, desc='', title='Foo Title'):

        class ITestContent(Interface):
            __module__ = __name__
            foo = self._FieldFactory(title=title, description=desc)

        class TestObject:
            __module__ = __name__
            implements(ITestContent)

        self.content = TestObject()
        field = ITestContent['foo']
        field = field.bind(self.content)
        request = TestRequest(HTTP_ACCEPT_LANGUAGE='ru')
        request.form['field.foo'] = 'Foo Value'
        self._widget = self._WidgetFactory(field, request)

    def setUp(self):
        super(BrowserWidgetTest, self).setUp()
        self.setUpContent()


class TestWidget(SimpleInputWidget):
    __module__ = __name__

    def _toFieldValue(self, v):
        if v == 'barf!':
            raise ConversionError('ralph')
        return v or None


class TestObjectWidget(BrowserWidgetTest):
    __module__ = __name__
    _WidgetFactory = TestWidget

    def test_getInputValue(self):
        self.assertEqual(self._widget.getInputValue(), 'Foo Value')
        self._widget.request.form['field.foo'] = (1, 2)
        self.assertRaises(WidgetInputError, self._widget.getInputValue)
        self._widget.request.form['field.foo'] = 'barf!'
        self.assertRaises(ConversionError, self._widget.getInputValue)
        del self._widget.request.form['field.foo']
        self._widget.context.required = True
        self.assertRaises(MissingInputError, self._widget.getInputValue)
        self._widget.context.required = False
        self._widget.request.form['field.foo'] = ''
        self.assertEqual(self._widget.getInputValue(), None)
        return

    def test_applyChanges(self):
        self.assertEqual(self._widget.applyChanges(self.content), True)


def test_suite():
    return unittest.TestSuite((unittest.makeSuite(TestObjectWidget),))


if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite())