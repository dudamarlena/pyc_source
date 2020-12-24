# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/orangecontrib/tomwer/test/test_dump_widget_canvas.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 2381 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '28/01/2019'
import logging, unittest
from orangecontrib.tomwer.test.utils import OrangeWorflowTest
from tomwer.gui.qtapplicationmanager import QApplicationManager
from tomwer.test.utils import skip_gui_test
logging.disable(logging.INFO)
app = QApplicationManager()

@unittest.skipIf((skip_gui_test()), reason='skip gui test')
class TestDumpWidgets(OrangeWorflowTest):
    __doc__ = '\n    simply create orange widgets in the orange canvas to make instances\n    of those are made correctly\n    '

    def testTimer(self):
        timer_node = self.addWidget('orangecontrib.tomwer.widgets.control.TimerOW.TimerOW')
        self.processOrangeEventsStack()
        timer_widget = self.getWidgetForNode(timer_node)
        self.assertTrue(timer_widget is not None)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestDumpWidgets,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')