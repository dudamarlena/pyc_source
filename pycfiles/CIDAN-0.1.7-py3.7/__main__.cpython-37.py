# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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