# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/app/samplemoved.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 1861 bytes
import logging, sys
from silx.gui import qt
import argparse
from tomwer.gui.utils.splashscreen import getMainSplashScreen
from tomwer.gui import icons
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.gui.samplemoved import SampleMovedWidget
import os, signal
logging.basicConfig()
_logger = logging.getLogger(__name__)

def getinputinfo():
    return 'tomwer samplemoved [scanDir]'


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.quit()


def main(argv):
    global app
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scan_path',
      help='Data file to show (h5 file, edf files, spec files)')
    parser.add_argument('--debug',
      dest='debug',
      action='store_true',
      default=False,
      help='Set logging system in debug mode')
    options = parser.parse_args(argv[1:])
    app = qt.QApplication.instance() or qt.QApplication([])
    qt.QLocale.setDefault(qt.QLocale.c())
    signal.signal(signal.SIGINT, sigintHandler)
    sys.excepthook = qt.exceptionHandler
    timer = qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda : None)
    splash = getMainSplashScreen()
    widget = SampleMovedWidget()
    widget.setWindowIcon(icons.getQIcon('tomwer'))
    options.scan_path = options.scan_path.rstrip(os.path.sep)
    scan = ScanFactory.create_scan_object(options.scan_path)
    rawSlices = scan.getProjectionsUrl()
    widget.setImages(rawSlices)
    splash.finish(widget)
    widget.show()
    app.exec_()


if __name__ == '__main__':
    main(sys.argv)