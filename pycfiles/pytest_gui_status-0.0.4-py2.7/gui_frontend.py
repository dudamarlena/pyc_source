# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pytest_gui_status\status_gui\gui_frontend.py
# Compiled at: 2016-01-13 15:25:21
import htmlPy, os, sys
from PyQt4.QtGui import QApplication
import PyQt4.QtCore as QtCore
from gui_backend import Controller

def main():
    if len(sys.argv) > 1:
        dir_name_raw = sys.argv[1]
    else:
        dir_name_raw = '.'
    dir_name = os.path.abspath(dir_name_raw)
    app = htmlPy.AppGUI(title=('{dir_name} - Test Status').format(dir_name=dir_name), developer_mode=True, width=150, height=80)
    app.window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    screen_geo = QApplication.desktop().availableGeometry()
    screen_topright = screen_geo.topRight()
    app.x_pos = screen_topright.x() - 20 - app.width
    app.y_pos = screen_topright.y() + 20
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.static_path = os.path.join(BASE_DIR, 'static/')
    app.template_path = os.path.join(BASE_DIR, 'tmpl/')
    app.dir_name = dir_name
    app_backend = Controller(app)
    app.bind(app_backend)
    app_backend.redraw()
    app.start()


if __name__ == '__main__':
    main()