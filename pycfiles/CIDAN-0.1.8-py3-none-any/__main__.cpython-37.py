# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/__main__.py
# Compiled at: 2020-04-29 15:32:03
# Size of source mod 2**32: 660 bytes
from CIDAN.GUI import MainWindow
from PySide2.QtWidgets import QApplication
import sys, logging
LEVELS = {'debug':logging.DEBUG, 
 'info':logging.INFO, 
 'warning':logging.WARNING, 
 'error':logging.ERROR, 
 'critical':logging.CRITICAL}
if len(sys.argv) > 1:
    LOG_FILENAME = 'log.out'
    level_name = sys.argv[1]
    level = LEVELS.get(level_name, logging.NOTSET)
    logging.basicConfig(filename=LOG_FILENAME, level=level)
    logger = logging.getLogger('CIDAN')
    logger.debug('Program started')
app = QApplication([])
app.setApplicationName('CIDAN')
widget = MainWindow.MainWindow()
sys.exit(app.exec_())