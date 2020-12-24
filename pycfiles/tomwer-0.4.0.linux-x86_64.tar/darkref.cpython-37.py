# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/app/darkref.py
# Compiled at: 2020-01-23 05:18:24
# Size of source mod 2**32: 2522 bytes
import argparse, logging, os, signal, sys
from silx.gui import qt
from tomwer.gui import icons
from tomwer.gui.reconstruction.darkref.darkrefwidget import DarkRefWidget
from tomwer.synctools.ftseries import _QDKRFRP
from tomwer.gui.utils.splashscreen import getMainSplashScreen
logging.basicConfig()
_logger = logging.getLogger(__name__)

class _DarkRefWidgetRunnable(DarkRefWidget):
    sigScanReady = qt.Signal(str)

    def __init__(self, dir, parent=None):
        self._DarkRefWidgetRunnable__darkref_rp = _QDKRFRP()
        DarkRefWidget.__init__(self, parent=parent, reconsparams=(self._DarkRefWidgetRunnable__darkref_rp))
        assert os.path.isdir(dir)
        self.dir = dir
        buttonExec = qt.QPushButton('execute', parent=self)
        buttonExec.setAutoDefault(True)
        self._forceSync = True
        self.layout().addWidget(buttonExec)
        buttonExec.pressed.connect(self._process)
        self.setWindowIcon(icons.getQIcon('tomwer'))

    def _process(self):
        self.process(scanID=(self.dir))


def getinputinfo():
    return 'tomwer darkref [scanDir]'


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
    if options.debug:
        logging.root.setLevel(logging.DEBUG)
    app = qt.QApplication.instance() or qt.QApplication([])
    qt.QLocale.setDefault(qt.QLocale.c())
    signal.signal(signal.SIGINT, sigintHandler)
    sys.excepthook = qt.exceptionHandler
    timer = qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda : None)
    splash = getMainSplashScreen()
    options.scan_path = options.scan_path.rstrip(os.path.sep)
    widget = _DarkRefWidgetRunnable(options.scan_path)
    splash.finish(widget)
    widget.show()
    app.exec_()


if __name__ == '__main__':
    main(sys.argv)