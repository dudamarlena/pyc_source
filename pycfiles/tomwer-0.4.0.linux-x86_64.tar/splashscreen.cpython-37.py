# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/utils/splashscreen.py
# Compiled at: 2020-01-08 09:31:39
# Size of source mod 2**32: 1857 bytes
__authors__ = [
 'H. Payno', 'T. Vincent']
__license__ = 'MIT'
__date__ = '04/01/2018'
try:
    from silx.gui import qt
except ImportError:
    raise ImportError("Can't found silx modules")

from tomwer.gui import icons
import tomwer.version

def getMainSplashScreen():
    pixmap = icons.getQPixmap('tomwer')
    splash = qt.QSplashScreen(pixmap)
    splash.show()
    splash.raise_()
    _version = tomwer.version.version
    text = 'version ' + str(_version)
    splash.showMessage(text, qt.Qt.AlignLeft | qt.Qt.AlignBottom, qt.Qt.white)
    return splash