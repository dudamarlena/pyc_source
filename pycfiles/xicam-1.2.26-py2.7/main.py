# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicamlauncher\main.py
# Compiled at: 2018-08-27 17:21:07
import os, sys
from PySide import QtGui, QtCore
if sys.platform == 'win32':
    sys.stdout = open(os.path.join(os.path.expanduser('~'), 'out.log'), 'w')
    sys.stderr = open(os.path.join(os.path.expanduser('~'), 'err.log'), 'w')
from splash import SplashScreen

def main():
    sys.path.append(os.path.join(os.getcwd(), 'lib/python2.7/lib-dynload'))
    try:
        d = QtCore.QDir(__file__)
        d.cdUp()
        d.cdUp()
        d.setCurrent(d.path())
        print 'QApp root:', QtCore.QDir().current()
    except NameError:
        print 'Could not set QApp root.'

    for path in sys.path:
        print 'path:', path

    import xicam
    app = QtGui.QApplication(sys.argv)
    pixmap = QtGui.QPixmap('xicam/gui/splash.gif')
    print 'CWD:', os.getcwd()
    if True:
        splash = SplashScreen(pixmap, f=QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.SplashScreen)
        splash.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        splash.setMask(pixmap.mask())
        splash.show()
        splash.raise_()
        splash.activateWindow()
        app.setActiveWindow(splash)
    else:
        import xicam
        from xicam import xglobals
        xglobals.window = xicam.xicamwindow.MyMainWindow(app)
        xglobals.window.ui.show()
        xglobals.window.ui.raise_()
        xglobals.window.ui.activateWindow()
        app.setActiveWindow(xglobals.window.ui)
    app.processEvents()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()