# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\source\Tools\BasePara.py
# Compiled at: 2019-04-14 12:07:49
# Size of source mod 2**32: 2271 bytes
from PyQt5.QtCore import Qt, QSettings, pyqtSignal, QObject, QFile, QIODevice, QTextStream
from PyQt5.QtGui import QColor, QBrush, QPen
import os, sys
from os.path import dirname, abspath, basename, join
ROOT_PATH = abspath(dirname(sys.argv[0])).replace('\\', '/')
R = 0
G = 1
B = 2
Y = 3
K = 4
W = 5
S = 6
COLOR = {R: QColor(Qt.red), G: QColor(Qt.green), 
 B: QColor(Qt.blue), Y: QColor(Qt.darkYellow), 
 K: QColor(Qt.black), W: QColor(Qt.white), 
 S: QColor(Qt.blue)}
PEN = {R: QPen(Qt.red), G: QPen(Qt.green), 
 B: QPen(Qt.blue), Y: QPen(Qt.darkYellow), 
 K: QPen(Qt.black), W: QPen(Qt.white), 
 S: QPen(Qt.blue)}
BRUSH = {R: QBrush(COLOR[R]), G: QBrush(COLOR[G]), 
 B: QBrush(COLOR[B]), Y: QBrush(COLOR[Y]), 
 K: QBrush(COLOR[K]), W: QBrush(COLOR[W]), 
 S: QBrush(COLOR[S])}
config_path = join(os.getcwd(), 'Config')
if os.path.exists(config_path) is False:
    os.mkdir(config_path)
DB_PATH = join(config_path, 'upload.db')
graphics_path = join(config_path, 'graphics.json')
setting_path = join(config_path, 'settings.ini')
error_log_path = join(config_path, 'log.txt')
tmp_folder = './Printer'
tmp_file = './Printer/tmp.html'
html_tmplate = ':/src/tmp.html'
css_tmplate = ':/src/bootstrap.min.css'

def create_printer_tmp():

    def copyFile(filePath):
        file = QFile(filePath)
        if file.exists() is False:
            import resource_rc
        file.open(QIODevice.ReadWrite)
        fileName = filePath.split('/')[(-1)]
        cp_to_path = os.path.join(tmp_folder, fileName)
        file.copy(cp_to_path)
        file.close()

    if os.path.exists(tmp_folder) is False:
        os.mkdir(tmp_folder)
        copyFile(html_tmplate)
        copyFile(css_tmplate)


create_printer_tmp()
mw = None
settings = None

class _Signals(QObject):
    show_error_msg_signal = pyqtSignal(str)


Signals = _Signals()