# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/util/test/test_ui/test_ui.py
# Compiled at: 2019-08-19 15:09:30
"""Unit tests for UILoadable decorator"""
from __future__ import absolute_import
import os.path, unittest
from taurus.external.qt import Qt
from taurus.qt.qtgui.util.ui import UILoadable
from taurus.qt.qtgui.test import BaseWidgetTestCase
from .mywidget3 import MyWidget3

class UILoadableTestCase(unittest.TestCase):
    """
    Test cases for UILoadable decorator
    """

    @UILoadable
    class MyWidget1(Qt.QWidget):

        def __init__(self, parent=None):
            Qt.QWidget.__init__(self, parent)
            self.loadUi()
            self.my_button.setText('This is MY1 button')

    @UILoadable(with_ui='ui')
    class MyWidget2(Qt.QWidget):

        def __init__(self, parent=None):
            Qt.QWidget.__init__(self, parent)
            path = os.path.join(os.path.dirname(__file__), 'ui', 'mywidget2')
            self.loadUi(filename='mywidget2_custom.ui', path=path)
            self.ui.my_button.setText('This is MY2 button')

    def setUp(self):
        app = Qt.QApplication.instance()
        if app is None:
            app = Qt.QApplication([])
        self.__app = app
        return

    def test_uiloadable_default(self):
        """Test UILoadable with default arguments"""
        widget = self.MyWidget1()
        self.assertEquals(widget.my_button.text(), 'This is MY1 button', 'button text differs from expected')

    def test_uiloadable_customized(self):
        """Test UILoadable with customized filename and path"""
        widget = self.MyWidget2()
        self.assertTrue(hasattr(widget, 'ui'), "widget doesn't have 'ui' member")
        self.assertTrue(hasattr(widget.ui, 'my_button'), "widget.ui doesn't have a 'my_button' member")
        self.assertFalse(hasattr(widget, 'my_button'), 'widget has a my_button member')
        self.assertEquals(widget.ui.my_button.text(), 'This is MY2 button', 'button text differs from expected')


class Bug151_TestCase(BaseWidgetTestCase, unittest.TestCase):
    """Test for bug 151: https://sourceforge.net/p/tauruslib/tickets/151/"""

    def test_bug151(self):
        """Check inheritance of UILoadable classes across packages (bug #151)
        """

        class Bug151_Widget(MyWidget3):
            pass

        try:
            Bug151_Widget()
        except:
            self.fail('Inheriting from UILoadable from another package fails')


def main():
    unittest.main()


if __name__ == '__main__':
    main()