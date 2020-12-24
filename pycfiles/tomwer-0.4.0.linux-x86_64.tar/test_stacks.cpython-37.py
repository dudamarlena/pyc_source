# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/test/test_stacks.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 6969 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '22/01/2017'
from tomwer.gui.stackplot import ImageFromFile
from tomwer.gui.stacks import SliceStack, RadioStack
from tomwer.test.utils import UtilsTest
from silx.gui import qt
import unittest, logging, time
from tomwer.gui.qtapplicationmanager import QApplicationManager
from tomwer.test.utils import skip_gui_test
import weakref
_qapp = QApplicationManager()
logging.disable(logging.INFO)

@unittest.skipIf((skip_gui_test()), reason='skip gui test')
class TestSliceStack(unittest.TestCase):
    __doc__ = ' unit test for the :class:_ImageStack widget'

    def setUp(self):
        unittest.TestCase.setUp(self)
        self._widget = SliceStack()
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)

    def tearDown(self):
        self._widget.close()
        unittest.TestCase.tearDown(self)

    def test(self):
        """Make sur the addLeaf and clear functions are working"""
        self._widget.setLoadingMode('load when show requested')
        folder = UtilsTest.getDataset('D2_H2_T2_h_')
        self.assertTrue(self._widget._viewer.getActiveImage() is None)
        self.assertTrue(len(self._widget._scans) is 0)
        self._widget.addLeafScan(folder)
        self.assertTrue(len(self._widget._scans) is 1)
        time.sleep(0.3)
        _qapp.processEvents()
        self.assertTrue(self._widget._viewer.getActiveImage() is not None)
        self._widget.clear()
        self.assertTrue(len(self._widget._scans) is 0)
        self.assertTrue(self._widget._viewer.getActiveImage() is None)
        self._widget.addLeafScan(folder)
        self.assertTrue(len(self._widget._scans) is 1)
        time.sleep(0.3)
        _qapp.processEvents()
        self.assertTrue(self._widget._viewer.getActiveImage() is not None)


@unittest.skipIf((skip_gui_test()), reason='skip gui test')
class TestRadioStack(unittest.TestCase):
    __doc__ = 'Test for the RadioStack'

    def setUp(self):
        unittest.TestCase.setUp(self)
        self._widget = RadioStack()
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.spinBox = weakref.ref(self._widget._viewer._qspinbox)
        self.slider = weakref.ref(self._widget._viewer._qslider)

    def tearDown(self):
        self._widget.close()
        unittest.TestCase.tearDown(self)

    def _waitImages(self):
        _qapp.processEvents()
        time.sleep(0.2)
        _qapp.processEvents()

    def testASAPMode(self):
        self._widget.setLoadingMode('load ASAP')
        folder = UtilsTest.getDataset('D2_H2_T2_h_')
        self._widget.setForceSync(True)
        self._widget.addLeafScan(folder)
        self._waitImages()
        self.assertTrue(self._getStatsLoadedImage(self._widget._viewer.images) == (3605,
                                                                                   0,
                                                                                   0))
        self.spinBox().setValue(20)
        self._waitImages()
        self.assertTrue(self._getStatsLoadedImage(self._widget._viewer.images) == (3605,
                                                                                   0,
                                                                                   0))
        self.slider().setValue(10)
        _qapp.processEvents()
        self.assertTrue(self._getStatsLoadedImage(self._widget._viewer.images) == (3605,
                                                                                   0,
                                                                                   0))

    def testLazyLoadingMode(self):
        self._widget.setLoadingMode('lazy loading')
        folder = UtilsTest.getDataset('D2_H2_T2_h_')
        self._widget.addLeafScan(folder)
        self._waitImages()
        self.assertTrue(self._getStatsLoadedImage(self._widget._viewer.images) == (1,
                                                                                   0,
                                                                                   3604))
        self.spinBox().setValue(20)
        self._waitImages()
        self.assertTrue(self._getStatsLoadedImage(self._widget._viewer.images) == (1,
                                                                                   0,
                                                                                   3604))
        self.slider().setValue(10)
        self._waitImages()
        self.assertTrue(self._getStatsLoadedImage(self._widget._viewer.images) == (1,
                                                                                   0,
                                                                                   3604))
        self.spinBox().editingFinished.emit()
        self._waitImages()
        self.assertTrue(self._getStatsLoadedImage(self._widget._viewer.images) == (2,
                                                                                   0,
                                                                                   3603))

    def testOnShowLoading(self):
        self._widget.setLoadingMode('load when show requested')
        folder = UtilsTest.getDataset('D2_H2_T2_h_')
        self._widget.addLeafScan(folder)
        self._waitImages()
        self.assertTrue(self._getStatsLoadedImage(self._widget._viewer.images) == (1,
                                                                                   0,
                                                                                   3604))
        self.spinBox().setValue(20)
        self._waitImages()
        self.assertTrue(self._getStatsLoadedImage(self._widget._viewer.images) == (2,
                                                                                   0,
                                                                                   3603))
        self.slider().setValue(10)
        self._waitImages()
        self.assertTrue(self._getStatsLoadedImage(self._widget._viewer.images) == (3,
                                                                                   0,
                                                                                   3602))

    def _getStatsLoadedImage(self, images):
        """

        :param images:
        :return: nLoaded, NLoading, NNotLoaded
        """
        nLoaded = nLoading = nNotLoaded = 0
        for imgIndex, img in images._images.items():
            assert isinstance(img, ImageFromFile)
            nLoaded += int(img._status == 'loaded')
            nLoading += int(img._status == 'loading')
            nNotLoaded += int(img._status == 'not loaded')

        return (
         nLoaded, nLoading, nNotLoaded)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestSliceStack, TestRadioStack):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')