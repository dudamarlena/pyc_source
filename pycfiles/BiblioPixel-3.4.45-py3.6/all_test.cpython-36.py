# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/all_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1569 bytes
import os, unittest, BiblioPixelAnimations
from .import_all import import_all
from bibliopixel.util import log
import pytest

class TestAll(unittest.TestCase):

    def _test(self, root, name, blacklist):
        _, failures = import_all(root, name, blacklist)
        log.printer('*** Failed to load modules:')
        log.printer('  ', end='')
        (log.printer)(*[name for name, tb in failures], **{'sep': '\n  '})
        for name, tb in failures:
            log.printer('*** FAILED MODULE', name)
            log.printer()
            log.printer(tb)
            log.printer()

        self.assertTrue(not failures)

    @pytest.mark.filterwarnings('ignore:DeprecationWarning')
    def test_bp(self):
        self._test(BP_ROOT, BP_NAME, BP_BLACKLIST)

    @pytest.mark.filterwarnings('ignore:DeprecationWarning')
    def test_bpa(self):
        self._test(BPA_ROOT, BPA_NAME, BPA_BLACKLIST)


BP_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
BP_NAME = 'bibliopixel'
BP_BLACKLIST = ['bibliopixel.drivers.PiWS281X']
BPA_ROOT = os.path.dirname(os.path.dirname(BiblioPixelAnimations.__file__))
BPA_NAME = 'BiblioPixelAnimations'
BPA_BLACKLIST = [
 'BiblioPixelAnimations.cube.spectrum',
 'BiblioPixelAnimations.cube.spectrum.system_eq',
 'BiblioPixelAnimations.matrix.ScreenGrab',
 'BiblioPixelAnimations.matrix.kimotion',
 'BiblioPixelAnimations.matrix.opencv_video',
 'BiblioPixelAnimations.matrix.spectrum',
 'BiblioPixelAnimations.matrix.spectrum.system_eq',
 'BiblioPixelAnimations.receivers.GenericNetworkReceiver']