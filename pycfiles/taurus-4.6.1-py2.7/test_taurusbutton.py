# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/button/test/test_taurusbutton.py
# Compiled at: 2019-08-19 15:09:29
"""Unit tests for taurus.button"""
import unittest
from taurus.test import getResourcePath
from taurus.qt.qtgui.test import BaseWidgetTestCase, GenericWidgetTestCase
from taurus.qt.qtgui.button import TaurusCommandButton
skip, skipmsg = False, None
try:
    from PyTango import CommunicationFailed
    from taurus.core.tango.starter import ProcessStarter
except:
    skip = True
    skipmsg = 'tango-dependent test'

class TaurusCommandButtonTest(GenericWidgetTestCase, unittest.TestCase):
    _klass = TaurusCommandButton
    _modelnames = ['sys/tg_test/1', None, 'sys/database/2', '']


@unittest.skipIf(skip, skipmsg)
class TaurusCommandButtonTest2(BaseWidgetTestCase, unittest.TestCase):
    _klass = TaurusCommandButton
    initkwargs = dict(command='TimeoutCmd')

    def setUp(self):
        """
        Requisites:
         - instantiate the widget
         - make sure that the the timeout server is ready
        """
        BaseWidgetTestCase.setUp(self)
        timeoutExec = getResourcePath('taurus.qt.qtgui.button.test.res', 'Timeout')
        self._starter = ProcessStarter(timeoutExec, 'Timeout/unittest')
        devname = 'unittests/timeout/temp-1'
        self._starter.addNewDevice(devname, klass='Timeout')
        self._starter.startDs()
        self._widget.setModel(devname)

    def tearDown(self):
        """Stop the timeout server and undo changes to the database"""
        self._widget.setModel(None)
        self._starter.cleanDb(force=True)
        return

    def testTimeOutError(self):
        """Check that the timeout property works"""
        self._widget.setParameters([0.2])
        self._widget.setTimeout(10)
        ret = self._widget._onClicked()
        msg = 'expected return None when timeout >> command response time'
        self.assertIsNone(ret, msg)
        self._widget.setTimeout(0.1)
        self.assertRaises(CommunicationFailed, self._widget._onClicked)


if __name__ == '__main__':
    unittest.main()