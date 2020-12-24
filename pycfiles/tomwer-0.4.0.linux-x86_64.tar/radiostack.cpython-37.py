# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/app/radiostack.py
# Compiled at: 2020-01-24 07:42:12
# Size of source mod 2**32: 1901 bytes
import logging, sys, os
from silx.gui import qt
import argparse
from tomwer.gui.utils.splashscreen import getMainSplashScreen
from tomwer.gui.stacks import RadioStack
from tomwer.gui import icons
import signal
logging.basicConfig()
_logger = logging.getLogger(__name__)

def getinputinfo():
    return 'tomwer radiostack [scanDir]'


def addFolderAndSubFolder(stack, path):
    stack.addLeafScan(path)
    for f in os.listdir(path):
        _path = os.path.join(path, f)
        if os.path.isdir(_path) is True:
            addFolderAndSubFolder(stack, _path)


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.quit()


def main(argv):
    global app
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root_dir',
      help='Root dir to browse and to extract all radio under it.')
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
    widget = RadioStack()
    widget.setWindowIcon(icons.getQIcon('tomwer'))
    options.root_dir = options.root_dir.rstrip(os.path.sep)
    addFolderAndSubFolder(stack=widget, path=(options.root_dir))
    splash.finish(widget)
    widget.show()
    app.exec_()


if __name__ == '__main__':
    main(sys.argv)